import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import io
import boto3
from dotenv import load_dotenv
from utils.audio_generation import generate_audio, create_audio_mix, upload_audio_to_cloudflare_r2


# Carrega as variáveis de ambiente
load_dotenv()

# Configuração do cliente S3 para Cloudflare R2
s3 = boto3.client(
    service_name="s3",
    endpoint_url=os.getenv("CLOUDFLARE_R2_S3_API_URL"),
    aws_access_key_id=os.getenv("CLOUDFLARE_R2_S3_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("CLOUDFLARE_R2_S3_SECRET_ACCESS_KEY"),
    region_name="auto"  # ou sua região específica, se necessário
)

class ReligiousContentService:

    @staticmethod
    def get_content_from_url(type='versiculo_do_dia'):
        base_url = "https://www.bibliaon.com"
        url = f"{base_url}/{type}/"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lança um erro para respostas de falha
            soup = BeautifulSoup(response.text, 'html.parser')
            return ReligiousContentService.parse_content(soup, type)
        except requests.RequestException as e:
            return {'error': f"Erro ao acessar a página: {e}"}

    @staticmethod
    def parse_content(soup, type):
        result = {}
        if type in ['versiculo_do_dia', 'salmo_do_dia']:
            content_selector = 'destaque' if type == 'versiculo_do_dia' else None
            result = {
                'titulo': soup.find('h2', class_='v_title').text.strip(),
                'data': soup.find('h4', class_='v_date').text.strip(),
                'conteudo': soup.find('p', class_=content_selector).text.strip(),
                'referencia': soup.find('p', class_='destaque').find('a').get('href').strip() if type == 'versiculo_do_dia' else soup.find('div', id='salmo_hoje').find('a').get('href').strip()
            }
        elif type in ['devocional_diario', 'palavra_do_dia']:
            corpo_textos = [p.text for p in soup.select('.articlebody p')[:-1]]
            result = {
                'mes': soup.find('span', class_='devcal-month').text.strip(),
                'dia': soup.find('span', class_='devday-number').text.strip(),
                'dia_semana': soup.find('span', class_='devday-txt').text.strip(),
                'titulo': soup.find('h3', class_='dev-title').text.strip(),
                'conteudo': ' '.join(corpo_textos),
                'oracao': soup.select('.articlebody p')[-1].text.strip()
            }
        return result

    @staticmethod
    def generate_verse(generate_audio_flag=True):
        content = ReligiousContentService.get_content_from_url(type='versiculo_do_dia')
        return ReligiousContentService.generate_content_audio(content, 'verse', generate_audio_flag)

    @staticmethod
    def generate_devotional(generate_audio_flag=True):
        content = ReligiousContentService.get_content_from_url(type='devocional_diario')
        return ReligiousContentService.generate_content_audio(content, 'devotional', generate_audio_flag)

    @staticmethod
    def generate_content_audio(content, type, generate_audio_flag):
        if 'conteudo' in content and generate_audio_flag:
            text = content['conteudo']
            audio_url = ReligiousContentService.save_audio_to_cloudflare_r2(text, type)
            content['audio_url'] = audio_url
        return content

    @staticmethod
    def generate_verse_audio(generate_audio_flag=True):
            content = ReligiousContentService.get_content_from_url(type='versiculo_do_dia')
            if generate_audio_flag:
                audio_segment = generate_audio(content['conteudo'])
                mixed_audio_path = create_audio_mix(audio_segment, 'path/to/your/background.mp3')
                public_url = upload_audio_to_cloudflare_r2(mixed_audio_path)
                content['audio_url'] = public_url
            return content

    @staticmethod
    def generate_devotional_audio(generate_audio_flag=True):
            content = ReligiousContentService.get_content_from_url(type='devocional_diario')
            if generate_audio_flag:
                audio_segment = generate_audio(content['conteudo'])
                mixed_audio_path = create_audio_mix(audio_segment, 'path/to/your/background.mp3')
                public_url = upload_audio_to_cloudflare_r2(mixed_audio_path)
                content['audio_url'] = public_url
            return content