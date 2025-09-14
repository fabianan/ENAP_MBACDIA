import requests
from bs4 import BeautifulSoup
import json
import time
import random

def scrape_quotes():
    base_url = "https://quotes.toscrape.com"
    quotes_data = []
    page_num = 1

    # Definir um User-Agent para simular um navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64 ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    while True:
        url = f"{base_url}/page/{page_num}/"
        
        try:
            response = requests.get(url, headers=headers, timeout=10) # Adicionado timeout
            response.raise_for_status() # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar a página {url}: {e}")
            break # Sai do loop em caso de erro de requisição

        soup = BeautifulSoup(response.text, 'html.parser')

        quotes = soup.find_all('div', class_='quote')
        if not quotes:
            print("Nenhuma citação encontrada ou fim das páginas.")
            break

        for quote in quotes:
            try:
                text = quote.find('span', class_='text').text
                author = quote.find('small', class_='author').text
                tags_elements = quote.find('div', class_='tags').find_all('a', class_='tag')
                tags = [tag.text for tag in tags_elements]
                
                quotes_data.append({"quote": text, "author": author, "tags": tags})
            except AttributeError as e:
                print(f"Erro ao extrair dados de uma citação: {e}. Pulando esta citação.")
                continue # Continua para a próxima citação se houver erro na extração
        
        next_button = soup.find('li', class_='next')
        if not next_button:
            print("Botão 'Próximo' não encontrado. Fim do scraping.")
            break
        
        page_num += 1
        
        # Adicionar atraso aleatório para evitar bloqueio
        sleep_time = random.uniform(1, 3) # Atraso entre 1 e 3 segundos
        print(f"Aguardando {sleep_time:.2f} segundos antes da próxima requisição...")
        time.sleep(sleep_time)

    return quotes_data

if __name__ == "__main__":
    scraped_data = scrape_quotes()
    if scraped_data:
        with open('quotes.json', 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, ensure_ascii=False, indent=4)
        print("Dados salvos em quotes.json")
    else:
        print("Nenhum dado foi coletado.")
