# Ubica ITSP

Prototipo web para consultar personal docente y administrativo dentro del Instituto Tecnológico Superior de Pánuco. Usa Flask/Python, HTML/CSS y MySQL.

## Requisitos

- Python 3.10 o posterior
- MySQL 8 o compatible

## Preparar MySQL

En esta PC, MySQL está instalado en `C:\AppServ\MySQL`. Inicia el servicio `mysql8` si está detenido y ejecuta `setup_db.bat` desde el proyecto. Si Windows deniega el inicio, abre PowerShell como administrador y ejecuta `Start-Service mysql8`. El script pide la contraseña de `root` directamente en la consola y carga el esquema y registros ficticios de muestra. Si MySQL no está en AppServ, ajusta la ruta de `mysql.exe` al inicio del archivo.

También puedes cargar el esquema desde una consola MySQL:

```sql
SOURCE schema.sql;
```

Los registros de demostración son inventados y deben sustituirse antes de usar el directorio como fuente institucional.

## Ejecutar en Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:MYSQL_HOST = "127.0.0.1"
$env:MYSQL_USER = "root"
$env:MYSQL_PASSWORD = "tu-clave"
$env:MYSQL_DATABASE = "localizacion_itsp"
$env:FLASK_SECRET_KEY = "una-clave-larga-y-aleatoria"
$env:ADMIN_USER = "admin"
$env:ADMIN_PASSWORD = "otra-clave-larga-y-aleatoria"
py app.py
```

Si prefieres no dejar la contraseña escrita en el historial de PowerShell, usa un prompt oculto antes de iniciar Flask:

```powershell
$secure = Read-Host "Contraseña de MySQL" -AsSecureString
$env:MYSQL_PASSWORD = [System.Net.NetworkCredential]::new("", $secure).Password
& 'C:\Users\rod45\AppData\Local\Programs\Python\Python313\python.exe' .\app.py
```

Abre `http://127.0.0.1:5000`. El acceso de administración está en `/admin`; las credenciales se establecen con variables de entorno. No configures el servidor para exponerlo fuera de la red de desarrollo sin agregar las medidas de seguridad y despliegue requeridas.

## Alcance del prototipo

- Consulta y búsqueda de docentes y personal administrativo por nombre, área o materia.
- Fichas con datos institucionales y estados distintos para ubicación disponible, no disponible y fuera del plantel confirmado.
- Administración básica de registros de personal; la ubicación no puede cambiarse desde el formulario.
- La base incluye espacios y personal ficticios para mostrar la interfaz.
- **La detección por Wi-Fi no está conectada.** El documento del proyecto deja pendiente confirmar la viabilidad, los permisos y el acceso a la infraestructura de red del ITSP. Para actualizar ubicaciones automáticamente hace falta implementar una fuente de eventos confiable y conectarla a `personnel.current_location_id`, `location_status` y `location_updated_at`. El prototipo no usa GPS ni registra desplazamientos.
