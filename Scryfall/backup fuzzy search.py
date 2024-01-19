import requests
import csv
import re


def search(query):
    url = 'https://api.scryfall.com/cards/search'
    # url = 'https://api.scryfall.com/cards/named'
    params = {
        'q': query,
    }

    response = requests.get(url, params=params)
    cards = []
    if response.status_code == 200:
        data = response.json()
        cards = data.get('data', [])
        # print('card: ', cards)
        # return data
    else:
        return None
    return cards


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


def save_to_csv(cards, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Set Name', 'Mana Cost',
                      'Type', 'Oracle Text', 'Foil', 'Price (USD)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for card in cards:
            writer.writerow({
                # Access card properties within each card dictionary
                'Name': card.get('name', 'N/A'),
                'Set Name': card.get('set_name', 'N/A'),
                'Mana Cost': card.get('mana_cost', 'N/A'),
                'Type': card.get('type_line', 'N/A'),
                'Oracle Text': card.get('oracle_text', 'N/A'),
                'Foil': get_price(card.get('prices', {}), condition='normal', currency='usd')[0],
                'Price (USD)': get_price(card.get('prices', {}), condition='normal', currency='usd')[1]
            })


def ler_arquivo(arquivo):
    lista = open(arquivo, 'r', encoding='utf-8')
    # print('Lista: ', lista)
    cartas = []
    quantidade = []

    print(f'Antes: {cartas}')

    for linha in lista:
        linha = linha.strip()
        print('Durante: ', re.findall("[^[0-9]\s]", linha))
        # quantidade.append(re.findall('\d', linha))
        # res = [int(i) for i in linha if i.isdigit()]
        temp = re.findall("\d+", linha)
        print(temp)
        # res = list(map(int, temp))
        # quantidade.append(list(map(int, temp)))
        temp = list(map(int, temp)).pop()
        quantidade.append(temp)

        print(quantidade)
        # print(type(res))
        # print('quantidade: ', type(quantidade))
        if quantidade[-1] <= 9:
            cartas.append(re.findall('[^\d]+', linha[2:]).pop())
        else:
            cartas.append(re.findall('[^\d]+', linha[3:]).pop())
        # print(f'Durante: {cartas}')
        # print(f'Durante Quantidade: {quantidade}')

    print(f'Depois: {cartas}')
    print(f'Depois Quantidade: {quantidade}')
    # print(f'Res: ', res)

    lista.close()
    return cartas, quantidade


if __name__ == '__main__':
    arquivo = 'decklist.txt'
    cartas, quantidade = ler_arquivo(arquivo)
    print('Cartas: ', len(cartas))
    print('Quantidade: ', len(quantidade))
    all_results = []

    for i in cartas:
        results = search(i)
        # print(results)
        results = search(i.strip())

        # print('Lendo decklist')

        all_results.extend(results)

    # search_query = input('Enter a MTG card name:')
    # queries = search_query.split(';')
    # results = search(search_query)

    # all_results = []

    # for query in queries:
    #    results = search(query.strip())
    #    all_results.extend(results)

    if all_results:
        csv_filename = 'mtg_card_results.csv'
        save_to_csv(all_results, csv_filename)
        print(f'Search results saved to {csv_filename}')
    else:
        print('No cards found or an error occurred.')

    #######################################
'''
    if results:
        for card in results['data']:
            print(f"Name: {card['name']}")
            print(f"Mana Cost: {card.get('mana_cost', 'N/A')}")
            print(f"Type: {card['type_line']}")
            print(f"Oracle Text: {card.get('oracle_text', 'N/A')}")
            print("\n")
    else:
        print("Card not found or an error occurred.")
'''
