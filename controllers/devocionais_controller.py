from flask import Blueprint, jsonify, request
from services import devocionais_service

devocionais_bp = Blueprint('devocionais', __name__, url_prefix='/devocionais')

@devocionais_bp.route('/', methods=['GET'])
def get_devocional():
    types = request.args.get('types', 'conteudo')
    response = devocionais_service.get_devocional(types)
    return jsonify(response)
