import requests
from bs4 import BeautifulSoup

def get_content_from_url(type='versiculo_do_dia'):
    # Obtém o conteúdo de uma URL específica (hipotético)
    url = f"https://www.bibliaon.com/{type}/"
    response = requests.get(url)
    result = {}
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        if type in ['versiculo_do_dia', 'salmo_do_dia']:
            content_selector = 'destaque' if type == 'versiculo_do_dia' else None
            result['original'] = {
                'titulo': soup.find('h2', class_='v_title').text.strip(),
                'data': soup.find('h4', class_='v_date').text.strip(),
                'conteudo': soup.find('p', class_=content_selector).text.strip(),
                'referencia': soup.find('p', class_='destaque').find('a').get('href').strip()
                if type == 'versiculo_do_dia' else soup.find('div', id='salmo_hoje').find('a').get('href').strip()
            }
        elif type in ['devocional_diario', 'palavra_do_dia']:
            corpo_textos = [p.text for p in soup.select('.articlebody p')[:-1]]
            result['original'] = {
                'mes': soup.find('span', class_='devcal-month').text.strip(),
                'dia': soup.find('span', class_='devday-number').text.strip(),
                'dia_semana': soup.find('span', class_='devday-txt').text.strip(),
                'titulo': soup.find('h3', class_='dev-title').text.strip(),
                'conteudo': ' '.join(corpo_textos),
                'oracao': soup.select('.articlebody p')[-1].text.strip()
            }
    else:
        result['erro'] = "Erro ao acessar a página."
    return result