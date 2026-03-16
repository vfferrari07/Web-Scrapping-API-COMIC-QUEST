from fastapi import FastAPI
from typing import List
import requests
from bs4 import BeautifulSoup

app = FastAPI()

    url = 'https://www.estantevirtual.com.br/'
    produtos = []
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.select('div.card-product')
        for card in cards:
            titulo_elem = card.select_one('h2.card-product-title')
            link_elem = card.select_one('a.card-product-link')
            titulo = titulo_elem.get_text(strip=True) if titulo_elem else 'Sem título'
            link = link_elem['href'] if link_elem and link_elem.has_attr('href') else None
            produtos.append({'titulo': titulo, 'link': link})
    except Exception as e:
        pass
    return produtos

@app.get('/produtos', response_model=List[dict])
def get_produtos():
    return buscar_produtos_estantevirtual()

@app.get("/")
def root():
    return {"message": "API de Web Scraping Estante Virtual (Selenium). Use /produtos para buscar livros."}
