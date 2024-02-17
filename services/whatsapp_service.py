import os
import requests
import json
from dotenv import load_dotenv

class WhatsappService:
    @staticmethod
    def send_message(remoteJid, textMessage):
        # Carrega as variáveis de ambiente do arquivo .env
        load_dotenv()

        # Obtém as variáveis de ambiente
        evolution_api_base_url = os.getenv("EVOLUTION_API_BASE_URL")
        instance_id = os.getenv("INSTANCE_ID")
        api_key = os.getenv("API_KEY")
        
        # URL para a requisição da API
        url = f"{evolution_api_base_url}/message/sendText/{instance_id}"
        
        # Dados a serem enviados na requisição
        data = {
            "number": remoteJid,
            "options": {
                "delay": 1200,
                "presence": "composing"
            },
            "textMessage": {
                "text": textMessage
            }
        }
        
        # Headers para a requisição, incluindo a chave da API
        headers = {
            "Content-Type": "application/json",
            "apikey": api_key  # Adiciona o cabeçalho apikey
        }
        
        # Envia a requisição POST
        response = requests.post(url, data=json.dumps(data), headers=headers)
        
        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            # Retorna a resposta da API
            return response.json()
        else:
            # Retorna um erro se a requisição falhar
            return {"error": "Failed to send the message", "status_code": response.status_code}
