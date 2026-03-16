from fastapi import FastAPI
from typing import List
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Função de scraping adaptada

def buscar_produtos_estantevirtual():
    url = 'https://www.estantevirtual.com.br/'
    seletor_div = 'div.card-product'
    seletor_titulo = 'h2.card-product-title'
    seletor_link = 'a.card-product-link'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        produtos = []
        for produto in soup.select(seletor_div):
            titulo_tag = produto.select_one(seletor_titulo)
            link_tag = produto.select_one(seletor_link)
            titulo = titulo_tag.get_text(strip=True) if titulo_tag else 'Sem título'
            link = link_tag['href'] if link_tag and link_tag.has_attr('href') else None
            produtos.append({'titulo': titulo, 'link': link})
        return produtos
    except Exception as e:
        return []

@app.get('/produtos', response_model=List[dict])
def get_produtos():
    return buscar_produtos_estantevirtual()
