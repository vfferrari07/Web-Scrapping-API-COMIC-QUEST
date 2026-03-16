import requests
from bs4 import BeautifulSoup
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def buscar_anuncios(url, seletor_div, seletor_titulo, seletor_link):
    try:
        logging.info(f'Acessando {url}')
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        anuncios = []
        for anuncio in soup.select(seletor_div):
            titulo_tag = anuncio.select_one(seletor_titulo)
            link_tag = anuncio.select_one(seletor_link)
            titulo = titulo_tag.get_text(strip=True) if titulo_tag else 'Sem título'
            link = link_tag['href'] if link_tag and link_tag.has_attr('href') else None
            anuncios.append({'titulo': titulo, 'link': link})
        logging.info(f'Encontrados {len(anuncios)} anúncios em {url}')
        return anuncios
    except Exception as e:
        logging.error(f'Erro ao acessar {url}: {e}')
        return []

def exportar_json(anuncios, arquivo):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(anuncios, f, ensure_ascii=False, indent=2)
    logging.info(f'Exportado para {arquivo}')

if __name__ == '__main__':
    # Scraping de produtos do Estante Virtual
    sites = [
        {
            'url': 'https://www.estantevirtual.com.br/',
            'seletor_div': 'div.card-product',
            'seletor_titulo': 'h2.card-product-title',
            'seletor_link': 'a.card-product-link',
        },
    ]
    todos_produtos = []
    for site in sites:
        produtos = buscar_anuncios(
            site['url'],
            site['seletor_div'],
            site['seletor_titulo'],
            site['seletor_link']
        )
        todos_produtos.extend(produtos)
    exportar_json(todos_produtos, 'produtos_estantevirtual.json')
    for produto in todos_produtos:
        print(produto)
