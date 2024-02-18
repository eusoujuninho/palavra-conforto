import requests
from flask import Flask, jsonify
from controllers.religious_content_controller import religious_content_bp

# Cria a aplicação Flask
app = Flask(__name__)

# Registra o Blueprint na aplicação
app.register_blueprint(religious_content_bp)

# Define a porta para a aplicação Flask
port = 8005

if __name__ == '__main__':
    # Inicia o servidor Flask
    app.run(port=port)