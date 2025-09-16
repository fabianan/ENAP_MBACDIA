"""
scraper.py
Script para realizar web scraping no site https://quotes.toscrape.com/
Coleta: citação (quote), autor e tags.
Salva os dados em um arquivo JSON 'quotes.json' no mesmo diretório do script.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import os


def scrape_quotes():
    """
    Função principal para extrair citações, autores e tags do site quotes.toscrape.com.
    Retorna:
        list: Lista de dicionários com os dados coletados.
    """
    base_url = "https://quotes.toscrape.com"
    quotes_data = []

    # Configurações do navegador (modo headless = sem abrir janela gráfica)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar sem abrir janela
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )

    # Inicializa o driver do Chrome
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(base_url)

    while True:
        try:
            # Aguarda a presença de todos os elementos de citações na página
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "quote"))
            )

            # Localiza todos os blocos de citação
            quotes_elements = driver.find_elements(By.CLASS_NAME, "quote")

            # Extrai dados de cada citação
            for q in quotes_elements:
                text = q.find_element(By.CLASS_NAME, "text").text
                author = q.find_element(By.CLASS_NAME, "author").text
                tags_elements = q.find_elements(By.CSS_SELECTOR, ".tags .tag")
                tags = [tag.text for tag in tags_elements]

                quotes_data.append({
                    "quote": text,
                    "author": author,
                    "tags": tags
                })

            # Tenta localizar e clicar no botão "Next" (próxima página)
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, ".next a")
                next_button.click()
            except:
                print("Fim das páginas. Scraping concluído.")
                break

        except Exception as e:
            print(f"Erro ao processar página: {e}")
            break

    driver.quit()
    return quotes_data


if __name__ == "__main__":
    # Executa o scraper
    scraped_data = scrape_quotes()

    # Define caminho absoluto do arquivo JSON no mesmo diretório do script
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório atual do script
    output_path = os.path.join(script_dir, "quotes.json")

    # Salva o resultado em quotes.json
    if scraped_data:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, ensure_ascii=False, indent=4)
        print(f"Dados salvos em {output_path}")
    else:
        print("Nenhum dado foi coletado.")
