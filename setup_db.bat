@echo off
setlocal
set "MYSQL_CLIENT=C:\AppServ\MySQL\bin\mysql.exe"
if not exist "%MYSQL_CLIENT%" (
  where mysql.exe >nul 2>nul
  if errorlevel 1 (
    echo No se encontro mysql.exe. Instala MySQL o ajusta MYSQL_CLIENT en este archivo.
    pause
    exit /b 1
  )
  set "MYSQL_CLIENT=mysql.exe"
)
echo Se cargara schema.sql en el servidor MySQL local.
echo La contrasena de root se solicita en privado y no se guarda en el proyecto.
"%MYSQL_CLIENT%" --user=root --password < "%~dp0schema.sql"
if errorlevel 1 (
  echo No se pudo cargar la base. Confirma que MySQL este iniciado y que la contrasena sea correcta.
  pause
  exit /b 1
)
echo Base localizacion_itsp creada y preparada.
pause
