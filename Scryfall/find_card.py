import requests
import csv
import re
import collections


def search(query, type):
    # url = 'https://api.scryfall.com/cards/search'
    # url = 'https://api.scryfall.com/cards/named?exact=lightning+bolt'
    params = {
        'q': query,
    }
    url = 'https://api.scryfall.com/cards/named?' + type + '=' + query
    # url = 'https://api.scryfall.com/cards/search' + ''
    # print(url)
    response = requests.get(url, params=params)
    # print(response.status_code)
    # print(response.text)

    if response.status_code == 200:
        data = response.json()
        # print(data)
        # cards = data.get('data', [])
        # print('card: ', cards)
        return data
    else:
        return None
    # return cards


def get_price(prices, condition='normal', currency='usd'):
    cond = 'nonfoil'
    price_data = prices.get(currency, {})
    if price_data == None:
        cond = 'foil'
        price_data = prices.get('usd_foil', {})
    # print('price_data:', price_data)
    if price_data == None:
        return cond, 'N/A'
    else:
        return cond, price_data
    # return price_data.get(currency, 'N/A')


def ler_arquivo(arquivo):
    lista = open(arquivo, 'r', encoding='utf-8')
    # print('Lista: ', lista)
    cartas = []
    quantidade = []

    # print(f'Antes: {cartas}')

    for linha in lista:
        linha = linha.strip()
        # print('Durante: ', re.findall("[^[0-9]\s]", linha))
        # quantidade.append(re.findall('\d', linha))
        # res = [int(i) for i in linha if i.isdigit()]
        temp = re.findall("\d+", linha)
       # print(temp)
        # res = list(map(int, temp))
        # quantidade.append(list(map(int, temp)))
        # print('temp: ', temp)
        if temp != []:
            # print('Entrei')
            temp = list(map(int, temp)).pop()
            quantidade.append(temp)

            if quantidade[-1] <= 9:
                cartas.append(re.findall('[^\d]+', linha[2:]).pop())
            else:
                cartas.append(re.findall('[^\d]+', linha[3:]).pop())
        else:
            break

        # print(quantidade)
        # print(type(res))
        # print('quantidade: ', type(quantidade))

        # print(f'Durante: {cartas}')
        # print(f'Durante Quantidade: {quantidade}')

    # print(f'Depois: {cartas}')
    # print(f'Depois Quantidade: {quantidade}')
    # print(f'Res: ', res)

    lista.close()
    # print(f'Quantidade final: {quantidade}')
    # print(f'Soma: {sum(quantidade)}')

    return cartas, quantidade


def save_to_csv(cards, filename, quantity):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Quantity', 'Name', 'Set Name', 'Mana Cost',
                      'Type', 'Oracle Text', 'Foil', 'Price (USD)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        lista = []

        for i, card in zip(quantity, cards):
            # print(card['layout'])
            if card['layout'] in ['adventure', 'transform', 'modal_dfc']:
                # print(card['card_faces'])
                # if card['type_line'] is 'Land':

                lista = card['card_faces']
                # print(lista[0]['oracle_text'])
                # print(lista[1]['oracle_text'])
                writer.writerow({
                    # Access card properties within each card dictionary
                    # 'Quantity': quantity,
                    'Quantity': i,
                    'Name': card.get('name', 'N/A'),
                    'Set Name': card.get('set_name', 'N/A'),
                    'Mana Cost': lista[0]['mana_cost'] + ' // ' + lista[1]['mana_cost'],
                    'Type': card.get('type_line', 'N/A'),
                    'Oracle Text': lista[0]['oracle_text'] + ' // ' + lista[1]['oracle_text'],
                    'Foil': get_price(card.get('prices', {}), condition='normal', currency='usd')[0],
                    'Price (USD)': get_price(card.get('prices', {}), condition='normal', currency='usd')[1]
                })
                '''
                lista = card.get('card_faces')
                print(lista)
                '''

            else:
                writer.writerow({
                    # Access card properties within each card dictionary
                    # 'Quantity': quantity,
                    'Quantity': i,
                    'Name': card.get('name', 'N/A'),
                    'Set Name': card.get('set_name', 'N/A'),
                    'Mana Cost': card.get('mana_cost', 'N/A'),
                    'Type': card.get('type_line', 'N/A'),
                    'Oracle Text': card.get('oracle_text', 'N/A'),
                    'Foil': get_price(card.get('prices', {}), condition='normal', currency='usd')[0],
                    'Price (USD)': get_price(card.get('prices', {}), condition='normal', currency='usd')[1]
                })


def pips(cards, quantity):
    # print(len(cards))
    # print(cards)
    for card in cards:
        # print(card.get('name'))
        oracle = card.get('oracle_text')
        lang = card.get('lang')
        print(f'lang: {lang}')
        # print(card)
        # print(f'oracle: ', oracle)
        # print(f'type: ', card.get('type_line'))
        cost = card.get('mana_cost')
        # price = get_price(card.get('prices', {}), condition='normal', currency='usd')[1]


if __name__ == '__main__':
    # search_query = input('Enter a MTG card name:')
    # print(f'len: {len(search_query)}')
    # print(f'input: {search_query.replace(",","").replace(" ", "+").lower()}')
    # separadas = search_query.replace(" ", "+").lower()
    # print(len(separadas))

    U = 0  # Blue
    W = 0  # White
    B = 0  # Black
    R = 0  # Red
    G = 0  # Green
    C = 0  # Generic
    cheap = 0
    mdfc = 0
    total = 0
    ramp = 0
    draw = 0

    arquivo = 'teste.txt'
    cartas, quantidade = ler_arquivo(arquivo)
    # print('Cartas: ', len(cartas))
    # print('Quantidade: ', len(quantidade))
    # print('Soma das cartas: ', sum(quantidade))

    all_results = []

    for i in cartas:
        # print(f'len: {len(search_query)}')
        # print(f'input: {i.replace(",","").replace(" ", "+").lower()}')
        separadas = i.replace(",", "").replace(
            " ", "+").replace("'", "").lower().strip()
        # print(len(separadas))
        results = search(separadas, 'exact')
        # print(results)
        # results = search(i.strip())

        # print('Lendo decklist')

        all_results.append(results)
