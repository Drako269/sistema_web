import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="sistema_web",
        user="postgres",  # Cambia por tu usuario de PostgreSQL
        password="123456",  # Cambia por tu contraseña de PostgreSQL
        host="localhost"
    )