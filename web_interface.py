from flask import Blueprint, jsonify, request
from flask_login import login_required
from squid_manager import block_website

# Crea un Blueprint para las rutas de la API web
web_bp = Blueprint('web', __name__)

@web_bp.route('/traffic', methods=['GET'])
@login_required  # Protege esta ruta
def get_traffic():
    traffic_data = {"total_requests": 100, "blocked_requests": 10}
    return jsonify(traffic_data)

@web_bp.route('/block', methods=['POST'])
@login_required  # Protege esta ruta
def block_site():
    domain = request.json.get('domain')
    if domain:
        block_website(domain)
        return jsonify({"message": f"{domain} ha sido bloqueado"}), 200
    return jsonify({"error": "Dominio no proporcionado"}), 400

def start_web_server(app):
    print("Iniciando servidor web...")
    app.run(debug=False, host="0.0.0.0", port=5000)