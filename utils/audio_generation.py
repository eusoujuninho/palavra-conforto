import os
import io
from dotenv import load_dotenv
from pydub import AudioSegment
from datetime import datetime
import boto3

# Carrega as variáveis de ambiente
load_dotenv()

# Supondo que esta função esteja corretamente definida
from elevenlabs import generate

# Variáveis de ambiente para o Cloudflare R2
CLOUDFLARE_R2_S3_API_URL = os.getenv("CLOUDFLARE_R2_S3_API_URL")
CLOUDFLARE_R2_S3_ACCESS_KEY_ID = os.getenv("CLOUDFLARE_R2_S3_ACCESS_KEY_ID")
CLOUDFLARE_R2_S3_SECRET_ACCESS_KEY = os.getenv("CLOUDFLARE_R2_S3_SECRET_ACCESS_KEY")
CLOUDFLARE_R2_BUCKET_NAME = os.getenv("CLOUDFLARE_R2_BUCKET_NAME")
CLOUDFLARE_R2_BUCKET_PUBLIC_URL = os.getenv("CLOUDFLARE_R2_BUCKET_PUBLIC_URL")

elevenlabs_api_key = "2fc40447ad9f632ac733d8dd930f1035"

def generate_chunk_audio(text_chunk, voice="EXAVITQu4vr4xnSDxMaL", model="eleven_multilingual_v2"):
    audio_bytes = generate(text=text_chunk, api_key=elevenlabs_api_key, voice=voice, model=model)
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
    return audio_segment

def generate_audio(text, voice="EXAVITQu4vr4xnSDxMaL", model="eleven_multilingual_v2", max_chunk_size=500):
    # Esta função agora retorna diretamente o AudioSegment sem necessidade de text_chunks
    return generate_chunk_audio(text, voice, model)

def create_audio_mix(audio_segment, background_filename, output_directory="audios/results"):
    background = AudioSegment.from_file(background_filename).fade_in(3000)
    mixed_audio = background.overlay(audio_segment)
    mixed_filename = f"mixed_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
    os.makedirs(output_directory, exist_ok=True)
    mixed_filepath = os.path.join(output_directory, mixed_filename)
    mixed_audio.export(mixed_filepath, format="mp3")
    return mixed_filepath

def upload_audio_to_cloudflare_r2(file_path):
    s3 = boto3.client(
        service_name="s3",
        endpoint_url=CLOUDFLARE_R2_S3_API_URL,
        aws_access_key_id=CLOUDFLARE_R2_S3_ACCESS_KEY_ID,
        aws_secret_access_key=CLOUDFLARE_R2_S3_SECRET_ACCESS_KEY,
        region_name="auto"
    )
    filename = os.path.basename(file_path)
    with open(file_path, "rb") as file:
        s3.upload_fileobj(file, CLOUDFLARE_R2_BUCKET_NAME, filename)
    return os.path.join(CLOUDFLARE_R2_BUCKET_PUBLIC_URL, filename)

# Exemplo de uso:
# text = "Seu texto aqui."
# voice_audio_segment = generate_audio(text)
# mixed_audio_path = create_audio_mix(voice_audio_segment, 'path/to/your/background.mp3')
# public_url = upload_audio_to_cloudflare_r2(mixed_audio_path)
# print(public_url)
