from flask import Blueprint, jsonify, request
from services import whatsapp_service

whatsapp_bp = Blueprint('whatsapp', __name__, url_prefix='/send')

@whatsapp_bp.route('/', methods=['POST'])
def send_message():
    data = request.json
    response = whatsapp_service.send_message(data)
    return jsonify(response)
