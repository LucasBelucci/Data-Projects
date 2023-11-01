from newsapi import NewsApiClient
import json
import pandas as pd
import requests


def News():
    # Definindo os parâmetros para serem passados para a lib
    query_params = {
        'apiKey': 'e93e151696c347639a910ceae2b9e8a7',
        'sortBy': 'top',
        'country': 'br',

    }

    # URL a ser utilizada
    url = 'https://newsapi.org/v2/top-headlines'

    # Request e conversão para json
    res = requests.get(url, params=query_params)
    open_news = res.json()

    # Excluir colunas adicionais, mantendo apenas as que importam
    article = open_news['articles']

    # Criando os vetores para guardar os resultados
    results = []
    fonte = []

    # Percorrendo o arquivo json e armazenando nos vetores corretos
    for ar in article:
        results.append(ar['title'])
        fonte.append(ar['url'])

    # Método de print
    for i in range(len(results)):
        print(f'{i + 1}: {results[i]}')


if __name__ == '__main__':
    News()
