import requests
from bs4 import BeautifulSoup
import json

def scrape_quotes():
    base_url = "https://quotes.toscrape.com"
    quotes_data = []
    page_num = 1

    while True:
        url = f"{base_url}/page/{page_num}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        quotes = soup.find_all('div', class_='quote')
        if not quotes:
            break

        for quote in quotes:
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            tags_elements = quote.find('div', class_='tags').find_all('a', class_='tag')
            tags = [tag.text for tag in tags_elements]
            
            quotes_data.append({"quote": text, "author": author, "tags": tags})
        
        next_button = soup.find('li', class_='next')
        if not next_button:
            break
        
        page_num += 1

    return quotes_data

if __name__ == "__main__":
    scraped_data = scrape_quotes()
    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(scraped_data, f, ensure_ascii=False, indent=4)
    print("Dados salvos em quotes.json")


