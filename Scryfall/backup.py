import requests
import csv


def search(query, type):
    # url = 'https://api.scryfall.com/cards/search'
    # url = 'https://api.scryfall.com/cards/named?exact=lightning+bolt'
    params = {
        'q': query,
    }
    url = 'https://api.scryfall.com/cards/named?' + type + '=' + query
    # url = 'https://api.scryfall.com/cards/search' + ''
    print(url)
    response = requests.get(url, params=params)
    # print(response.status_code)
    # print(response.text)

    cards = []
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


def save_to_csv(cards, filename):
    with open(filename, 'w', newline='') as csvfile:
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


if __name__ == '__main__':
    search_query = input('Enter a MTG card name:')
    print(f'len: {len(search_query)}')
    print(f'input: {search_query.replace(",","").replace(" ", "+").lower()}')
    separadas = search_query.replace(" ", "+").lower()
    print(len(separadas))

    queries = separadas.split(';')

    # results = search(search_query)
    all_results = []

    for query in queries:
        results = search(query, 'exact')

        all_results.append(results)
        print('RESULTS: ', all_results)

    if all_results:
        csv_filename = 'mtg_card_results.csv'
        save_to_csv(all_results, csv_filename)
        print(f'Search results saved to {csv_filename}')
    else:
        print('No cards found or an error occurred.')
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
