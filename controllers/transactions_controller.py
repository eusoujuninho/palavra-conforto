from flask import Blueprint, request, jsonify
from services.hotmart_service import process_hotmart_webhook

transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@transactions_bp.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    platform = data.get('platform')
    
    if platform == 'hotmart':
        result = process_hotmart_webhook(data)
        return jsonify(result), 200
    
    return jsonify({'error': 'Unsupported platform'}), 400
