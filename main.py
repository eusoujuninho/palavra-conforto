from flask import Flask, jsonify, request
import sqlite3
from services.web_scraper_service import get_content_from_url
from services.whatsapp_service import sendWhatsappMessage
from utils.audio_generation import generate_audio, create_audio_mix
from utils.file_handling import save_file

app = Flask(__name__)

# Função para inicializar o banco de dados
def init_db():
    conn = sqlite3.connect('devocionais.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS devocionais
    (id INTEGER PRIMARY KEY, titulo TEXT, conteudo TEXT, audio_file_path TEXT);
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS versiculos
    (id INTEGER PRIMARY KEY, titulo TEXT, conteudo TEXT, audio_file_path TEXT);
    ''')
    conn.commit()
    conn.close()

# Função para inserir dados no banco de dados e retornar o ID
def insert_data(tabela, titulo, conteudo, audio_file_path):
    conn = sqlite3.connect('devocionais.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {tabela} (titulo, conteudo, audio_file_path) VALUES (?, ?, ?)",
                   (titulo, conteudo, audio_file_path))
    data_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return data_id

@app.route('/')
def index():
    return 'API Flask funcionando!'

@app.route('/devocional', methods=['GET'])
def devocional():
    types = request.args.get('types', 'conteudo')
    types_list = types.split(',')
    
    devocional_diario = get_content_from_url('devocional_diario')
    titulo = devocional_diario['original']['titulo']
    conteudo = devocional_diario['original']['conteudo']
    audio = generate_audio(conteudo)
    voice_audio_file = save_file(audio, directory='audios/voices')
    bg_music = 'audios/bgs/01.mp3'
    audio_result = create_audio_mix(voice_audio_file, bg_music)
    
    # Insere os dados no banco de dados e obtém o ID
    devocional_id = insert_data('devocionais', titulo, conteudo, audio_result)
    
    response = {'id': devocional_id}
    for type in types_list:
        if type == 'versiculo':
            response['versiculo'] = titulo
        elif type == 'conteudo':
            response['conteudo'] = conteudo
        elif type == 'audio':
            response['audio_result'] = audio_result
    
    return jsonify(response)

@app.route('/versiculo', methods=['GET'])
def versiculo():
    types = request.args.get('types', 'conteudo')
    types_list = types.split(',')
    
    versiculo_do_dia = get_content_from_url('versiculo_do_dia')
    titulo = versiculo_do_dia['original']['titulo']
    conteudo = versiculo_do_dia['original']['conteudo']
    audio = generate_audio(conteudo)
    voice_audio_file = save_file(audio, directory='audios/voices')
    bg_music = 'audios/bgs/01.mp3'
    audio_result = create_audio_mix(voice_audio_file, bg_music)
    
    # Insere os dados no banco de dados e obtém o ID
    versiculo_id = insert_data('versiculos', titulo, conteudo, audio_result)
    
    response = {'id': versiculo_id}
    for type in types_list:
        if type == 'versiculo':
            response['versiculo'] = titulo
        elif type == 'conteudo':
            response['conteudo'] = conteudo
        elif type == 'audio':
            response['audio_result'] = audio_result
    
    return jsonify(response)

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    id = data.get('id')
    tipo = data.get('tipo')
    numero = data.get('numero')

    tabela = 'devocionais' if tipo == 'devocional' else 'versiculos'

    conn = sqlite3.connect('devocionais.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {tabela} WHERE id = ?", (id,))
    item = cursor.fetchone()

    if item:
        texto_para_envio = f"{item['titulo']}\n\n{item['conteudo']}"

        # Envia a mensagem via WhatsApp
        sendWhatsappMessage(f"{numero}@s.whatsapp.net", texto_para_envio)

        return jsonify({"success": True, "message": "Mensagem enviada com sucesso."}), 200
    else:
        return jsonify({"error": "Item não encontrado."}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
