import os
import io
from dotenv import load_dotenv
from pydub import AudioSegment
import boto3
from datetime import datetime

# Carrega as variáveis de ambiente
load_dotenv()

# Configuração para a geração de áudio
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

# Configuração do cliente S3 para Cloudflare R2
s3 = boto3.client(
    service_name="s3",
    endpoint_url=os.getenv("CLOUDFLARE_R2_S3_API_URL"),
    aws_access_key_id=os.getenv("CLOUDFLARE_R2_S3_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("CLOUDFLARE_R2_S3_SECRET_ACCESS_KEY"),
    region_name="auto"
)

# Suponha que esta função esteja corretamente definida
from elevenlabs import generate

def generate_audio(text, voice="EXAVITQu4vr4xnSDxMaL", model="eleven_multilingual_v2"):
    audio_bytes = generate(text=text, api_key=elevenlabs_api_key, voice=voice, model=model)
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
    return audio_segment

def create_audio_mix(audio_segment, background_filename, output_directory="audios"):
    background = AudioSegment.from_file(background_filename).fade_in(3000)
    mixed_audio = background.overlay(audio_segment)
    mixed_filename = f"mixed_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
    mixed_filepath = os.path.join(output_directory, mixed_filename)
    os.makedirs(output_directory, exist_ok=True)
    mixed_audio.export(mixed_filepath, format="mp3")
    return mixed_filepath

def upload_audio_to_cloudflare_r2(file_path):
    filename = os.path.basename(file_path)
    with open(file_path, "rb") as file:
        s3.upload_fileobj(file, os.getenv("CLOUDFLARE_R2_BUCKET_NAME"), filename)
    public_url = os.path.join(os.getenv("CLOUDFLARE_R2_BUCKET_PUBLIC_URL"), filename)
    return public_url
