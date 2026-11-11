import os
from functools import wraps

import mysql.connector
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from mysql.connector import Error


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")


def db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE", "localizacion_itsp"),
    )


def query(sql, params=(), one=False):
    connection = db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(sql, params)
        result = cursor.fetchone() if one else cursor.fetchall()
        return result
    finally:
        cursor.close()
        connection.close()


def execute(sql, params=()):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(sql, params)
        connection.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        connection.close()


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


@app.route("/")
def index():
    term = request.args.get("q", "").strip()[:100]
    category = request.args.get("tipo", "todos")
    sql = """SELECT p.id, p.full_name, p.role, p.department, p.subject, p.schedule,
                    p.office, p.room, l.name AS current_location, p.location_status,
                    p.location_updated_at
             FROM personnel p LEFT JOIN locations l ON l.id = p.current_location_id
             WHERE (%s = '' OR p.full_name LIKE %s OR p.department LIKE %s OR p.subject LIKE %s)
               AND (%s = 'todos' OR p.role = %s)
             ORDER BY p.full_name"""
    people = query(sql, (term, f"%{term}%", f"%{term}%", f"%{term}%", category, category))
    return render_template("index.html", people=people, term=term, category=category)


@app.route("/admin/entrar", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        admin_user = os.getenv("ADMIN_USER", "admin")
        admin_password = os.getenv("ADMIN_PASSWORD", "")
        if admin_password and request.form.get("username") == admin_user and request.form.get("password") == admin_password:
            session["is_admin"] = True
            return redirect(url_for("admin_people"))
        flash("Credenciales incorrectas o falta configurar ADMIN_PASSWORD.", "error")
    return render_template("login.html")


@app.route("/admin/salir", methods=["POST"])
def admin_logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/admin")
@admin_required
def admin_people():
    people = query("SELECT id, full_name, role, department FROM personnel ORDER BY full_name")
    locations = query("SELECT id, name FROM locations ORDER BY name")
    edit_id = request.args.get("editar", type=int)
    editing = query("SELECT * FROM personnel WHERE id=%s", (edit_id,), one=True) if edit_id else None
    return render_template("admin.html", people=people, locations=locations, editing=editing)


@app.route("/admin/personal/guardar", methods=["POST"])
@admin_required
def save_person():
    fields = (
        request.form.get("full_name", "").strip(),
        request.form.get("role", "").strip(),
        request.form.get("department", "").strip(),
        request.form.get("subject", "").strip() or None,
        request.form.get("schedule", "").strip() or None,
        request.form.get("office", "").strip() or None,
        request.form.get("room", "").strip() or None,
    )
    if not fields[0] or fields[1] not in ("docente", "administrativo") or not fields[2]:
        flash("Completa nombre, tipo de personal y área.", "error")
        return redirect(url_for("admin_people"))
    person_id = request.form.get("id", "").strip()
    if person_id:
        execute("""UPDATE personnel SET full_name=%s, role=%s, department=%s, subject=%s,
                  schedule=%s, office=%s, room=%s WHERE id=%s""", (*fields, person_id))
    else:
        execute("""INSERT INTO personnel
                  (full_name, role, department, subject, schedule, office, room, location_status)
                  VALUES (%s,%s,%s,%s,%s,%s,%s,'unknown')""", fields)
    flash("Información guardada.", "success")
    return redirect(url_for("admin_people"))


@app.route("/admin/personal/<int:person_id>/eliminar", methods=["POST"])
@admin_required
def delete_person(person_id):
    execute("DELETE FROM personnel WHERE id=%s", (person_id,))
    flash("Registro eliminado.", "success")
    return redirect(url_for("admin_people"))


@app.errorhandler(Error)
def database_error(_error):
    return render_template("error.html"), 503


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1")
