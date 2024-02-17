from flask import Flask, jsonify
from controllers.religious_content_controller import religious_content_bp

app = Flask(__name__)

# Registra o Blueprint na aplicação
app.register_blueprint(religious_content_bp)

@app.route('/')
def index():
    return jsonify({'message': 'O serviço está funcionando!'})

if __name__ == '__main__':
    app.run(debug=True)
