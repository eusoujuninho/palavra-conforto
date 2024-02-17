from flask import Blueprint, jsonify, request
from services.religious_content_service import ReligiousContentService
from utils.audio_generation import generate_audio

# Cria um Blueprint para o conteúdo religioso
religious_content_bp = Blueprint('religious_content', __name__, url_prefix='/religious_content')

@religious_content_bp.route('/generate/verse', methods=['GET'])
def generate_verse():
    # Lê o parâmetro 'generate_audio_flag' da query string e converte para booleano
    generate_audio_flag = request.args.get('generate_audio_flag', 'false').lower() in ('true', '1', 't')
    try:
        verse_content = ReligiousContentService.generate_verse(generate_audio_flag=generate_audio_flag)
        return jsonify(verse_content), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@religious_content_bp.route('/generate/devotional', methods=['GET'])
def generate_devotional():
    # Mesmo procedimento para o devocional
    generate_audio_flag = request.args.get('generate_audio_flag', 'false').lower() in ('true', '1', 't')
    try:
        devotional_content = ReligiousContentService.generate_devotional(generate_audio_flag=generate_audio_flag)
        return jsonify(devotional_content), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500