from openai import OpenAI

client = OpenAI(api_key="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")

def generate_image_from_text(text):
    # Gera uma imagem a partir do texto usando a API da OpenAI (hipotético)
    prompt = generate_image_prompt(text)
    # Implemente a geração de imagem com base no prompt
    image_url = "url_da_imagem_gerada"
    return image_url

def generate_image_prompt(text):
    # Cria o prompt criativo para a geração de imagem
    completion = client.chat_completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": text},
            {"role": "system", "content": "Crie um prompt criativo para geração de imagem."},
        ],
    )
    return completion.choices[0].message.content
