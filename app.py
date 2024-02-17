from flask import Flask
# Importe os Blueprints dos seus controladores
from controllers.devocionais_controller import devocionais_bp
from controllers.versiculos_controller import versiculos_bp
from controllers.whatsapp_controller import whatsapp_bp
from controllers.transactions_controller import transactions_bp

app = Flask(__name__)

# Registra os Blueprints com a aplicação Flask
app.register_blueprint(devocionais_bp)
app.register_blueprint(versiculos_bp)
app.register_blueprint(whatsapp_bp)
app.register_blueprint(transactions_bp)

if __name__ == '__main__':
    app.run(debug=True)
