import requests
from flask import Blueprint, jsonify, request
from services.religious_content_service import ReligiousContentService
from utils.audio_generation import generate_audio
from models.devotional_model import Devotional
from datetime import datetime

# Cria um Blueprint para o conteúdo religioso
religious_content_bp = Blueprint('religious_content', __name__, url_prefix='/religious_content')

@religious_content_bp.route('/generate/verse', methods=['GET'])
def generate_verse():
    try:
        verse_content = ReligiousContentService.generate_verse()
        return jsonify(verse_content), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@religious_content_bp.route('/generate/devotional', methods=['GET'])
def generate_devotional():
        content = ReligiousContentService.get_content_from_url(type='devocional_diario')
        # Criar um novo DevotionalModel
        devotional = Devotional(
            title=content['titulo'],
            content=content['conteudo'],
            language="pt",
            video="",
            audio="",
            prayer=content['oracao'],
            status="PENDING"
        ).save()
        return {'devotional_id': devotional.id, **content}  # Retorna o ID do devocional criado junto com os demais dados do devocional