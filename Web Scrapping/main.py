import requests
from bs4 import BeautifulSoup
import csv


def scrape_page(soup, quotes):

    quote_elements = soup.find_all('div', class_='quote')

    for quote_elements in quote_elements:
        text = quote_elements.find('span', class_='text').text

        author = quote_elements.find('small', class_='author').text

        tag_elements = quote_elements.select('.tags .tag')

        tags = []

        for tag_element in tag_elements:
            tags.append(tag_element.text)

        quotes.append(
            {
                'text': text,
                'author': author,
                'tags': ', '.join(tags)
            }
        )


base_url = 'https://quotes.toscrape.com/'


headers = {
    'User-Agent': 'Mozilla Firefox: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0'
}

page = requests.get('https://quotes.toscrape.com/', headers=headers)

soup = BeautifulSoup(page.text, 'html.parser')

quotes = []

scrape_page(soup, quotes)

next_li_element = soup.find('li', class_='next')

while next_li_element is not None:
    next_page_relative_url = next_li_element.find('a', href=True)['href']

    page = requests.get(base_url + next_page_relative_url, headers=headers)

    soup = BeautifulSoup(page.text, 'html.parser')

    scrape_page(soup, quotes)

    next_li_element = soup.find('li', class_='next')

csv_file = open('quotes.csv', 'w', encoding='utf-8', newline='')

writer = csv.writer(csv_file)

writer.writerow(['Text', 'Author', 'Tags'])

for quote in quotes:
    writer.writerow(quote.values())

csv_file.close()
