import os
from pydub import AudioSegment
from pydub.playback import play

# Supondo que estas funções estão definidas ou importadas corretamente
from elevenlabs import generate
from file_handling import concatenate_audio
# Suponha que esta função agora retorna o texto completo se for menor que max_chunk_size
from text_processing import generate_text_chunks

elevenlabs_api_key = "2fc40447ad9f632ac733d8dd930f1035"

def generate_audio_from_chunks(chunks, voice="EXAVITQu4vr4xnSDxMaL", model="eleven_multilingual_v2"):
    # Inicializa uma lista para armazenar os áudios gerados
    audio_chunks = []
    
    # Gera o áudio para cada parte do texto, se necessário
    if len(chunks) == 1:  # Se só tem um chunk, gera o áudio diretamente
        return generate_chunk_audio(chunks[0], voice, model)
    else:
        for chunk in chunks:
            audio_chunk = generate_chunk_audio(chunk, voice, model)
            audio_chunks.append(audio_chunk)
        
        # Concatena os áudios gerados em um único áudio
        final_audio = concatenate_audio(audio_chunks)
        
        return final_audio

def generate_chunk_audio(text_chunk, voice, model):
    # Gera o áudio para uma parte específica do texto
    return generate(text=text_chunk, api_key=elevenlabs_api_key, voice=voice, model=model)

def generate_audio(text, voice="EXAVITQu4vr4xnSDxMaL", model="eleven_multilingual_v2", max_chunk_size=500):
    # Verifica se o texto excede o tamanho máximo para um único chunk
    if len(text) <= max_chunk_size:
        # Gera o áudio diretamente sem dividir em chunks
        return generate_chunk_audio(text, voice, model)
    else:
        # Gera os chunks do texto
        text_chunks = generate_text_chunks(text, max_chunk_size)
        print(text_chunks)
        
        # Gera o áudio a partir dos chunks
        return generate_audio_from_chunks(text_chunks, voice, model)

def create_audio_mix(voice_filename, background_filename, output_directory="audios/results"):
    # Carrega o áudio de fundo e o áudio de voz
    background = AudioSegment.from_file(background_filename).fade_in(3000)
    voice = AudioSegment.from_file(voice_filename).overlay(AudioSegment.silent(duration=5000) + voice, position=0).fade_out(3000)
    
    # Mistura os áudios
    mixed_audio = background.overlay(voice)
    
    # Gera o nome do arquivo misturado
    mixed_filename = f"mixed_{os.path.basename(voice_filename)}"
    
    # Verifica e cria o diretório de saída, se necessário
    os.makedirs(output_directory, exist_ok=True)
    
    # Caminho completo do arquivo mixado
    mixed_filepath = os.path.join(output_directory, mixed_filename)
    
    # Salva o áudio mixado no diretório especificado
    mixed_audio.export(mixed_filepath, format="mp3")
    
    return mixed_filepath
