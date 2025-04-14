@echo off

:: 1. Actualizar pip
echo Actualizando pip...
python -m pip install --upgrade pip

:: 2. Instalar dependencias desde requirements.txt
echo Instalando dependencias...
pip install -r requirements.txt

:: 3. Crear la base de datos PostgreSQL
echo Creando la base de datos PostgreSQL...
psql -U postgres -c "CREATE DATABASE sistema_web;" || echo La base de datos 'safeweb' ya existe.

:: 5. Crear tablas en la base de datos
echo Creando tablas en la base de datos...
psql -U postgres -d sistema_web -c "
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS devices (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    mac_address VARCHAR(17) UNIQUE NOT NULL,
    ip_address VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS blocked_sites (
    id SERIAL PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    risk_level VARCHAR(50),
    blocked BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS activity_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    site_url VARCHAR(255),
    access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"

echo Configuración completada. ¡El sistema está listo para usar!