from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from database import get_db_connection  # Función para conectar a PostgreSQL
from routes import auth_bp  # Rutas de autenticación (login, register, etc.)
from web_interface import web_bp, start_web_server  # Importa el Blueprint y la función para iniciar el servidor
from traffic_monitor import start_traffic_monitor  # Monitoreo de tráfico
from models import User
import threading

# Crear la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '26995973f'  # Clave secreta para sesiones

# Configurar Flask-Login
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Ruta para iniciar sesión

# Cargar el usuario actual
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Registrar las rutas de autenticación
app.register_blueprint(auth_bp)

# Registrar las rutas de la API web
app.register_blueprint(web_bp)

def main():
    # Crear un hilo para el monitoreo de tráfico
    # traffic_thread = threading.Thread(target=start_traffic_monitor, daemon=True)
    
    # Crear un hilo para el servidor web
    web_thread = threading.Thread(target=lambda: start_web_server(app), daemon=True)

    # print("Iniciando monitoreo de tráfico...")
    # traffic_thread.start()

    print("Iniciando servidor web...")
    web_thread.start()

    # Mantener el programa principal activo mientras los hilos están en ejecución
    try:
        while True:
            pass  # Mantén el programa principal en ejecución
    except KeyboardInterrupt:
        print("Deteniendo el sistema...")

if __name__ == '__main__':
    main()