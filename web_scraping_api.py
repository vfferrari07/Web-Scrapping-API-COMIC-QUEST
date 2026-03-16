from fastapi import FastAPI
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app = FastAPI()

def buscar_produtos_estantevirtual():
    url = 'https://www.estantevirtual.com.br/'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(3)  # Aguarda carregamento
    produtos = []
    cards = driver.find_elements(By.CSS_SELECTOR, 'div.card-product')
    for card in cards:
        titulo_elem = card.find_element(By.CSS_SELECTOR, 'h2.card-product-title')
        link_elem = card.find_element(By.CSS_SELECTOR, 'a.card-product-link')
        titulo = titulo_elem.text if titulo_elem else 'Sem título'
        link = link_elem.get_attribute('href') if link_elem else None
        produtos.append({'titulo': titulo, 'link': link})
    driver.quit()
    return produtos

@app.get('/produtos', response_model=List[dict])
def get_produtos():
    return buscar_produtos_estantevirtual()

@app.get("/")
def root():
    return {"message": "API de Web Scraping Estante Virtual (Selenium). Use /produtos para buscar livros."}
