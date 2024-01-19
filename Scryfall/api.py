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

# def separador(name):
    # if '//' in name:
        # return

# def search_type_card(cards, quantity):


def pips(cards, quantity):
    U = 0  # Blue
    W = 0  # White
    B = 0  # Black
    R = 0  # Red
    G = 0  # Green
    C = 0  # Generic
    ramp = 0  # Number of cheap ramp spells (cmc = 2 or less)
    draw = 0  # Number of cheap draw spells (cmc = 2 or less)
    total = 0
    mdfc = 0

    land = 0
    adventure = 0
    lista = []
    i = 0

    cheap_draw = ['draw a card', 'draw two cards', 'draw three cards', 'draws cards',
                  'draws two cards', 'draws three cards', 'look', 'put', 'your hand']

    cheap_ramp = ['add', 'search your library for a basic land card',
                  'enchanted land is tapped adds an additional', 'put a creature card with from your hand onto the battlefield', 'enchanted land is tapped',
                  'adds an additional', 'Search your library']

    non_creature = ['Instant', 'Sorcery', 'Enchantment', 'Artifact', 'Land']

    # print(len(cards))
    # print(cards)
    for card in cards:
        # print(card.get('name'))
        oracle = card.get('oracle_text')
        # print(card)
        # print(f'oracle: ', oracle)
        # print(f'type: ', card.get('type_line'))
        cost = card.get('mana_cost')
        # price = get_price(card.get('prices', {}), condition='normal', currency='usd')[1]
        if cost == None:
            if any(x in card.get('layout') for x in ['transform', 'mdfc']):
                # print(f'mdfc: {card.get("name")} ')
                mdfc += quantity[i]

            if any(x in card.get("type_line") for x in ['Battle']):
                # print(f'Battle encontrada')

                if any(x in card.get('type_line') for x in non_creature):
                    # print('BATTLE NON-CREATURE')
                    # print(f'{card.get("card_faces")}')
                    # print(type(card.get("card_faces")))
                    # print('CHEGUEI AQUI')
                    # print(f'CMC {card.get("cmc")}')
                    if card.get("cmc") <= 2:
                        lista = card.get('card_faces')

                        if any(x in lista[0]['oracle_text'] for x in cheap_ramp):
                            # print(f'Encontrei um non-creature cheap ramp {i} {quantity[i]} x {card.get("name")}')
                            ramp += quantity[i]
                            # print('ramp: ', ramp)

                        elif any(x in lista[0]['oracle_text'] for x in cheap_draw):
                            # print(f'Encontrei um non-creature cheap draw {quantity[i]} x {card.get("name")}')
                            ramp += quantity[i]
                            # print('draw: ', draw)

            if any(x in card.get("type_line") for x in ['Land']):
                # print(f'mdfc do tipo land: {card.get("name")}')
                if any(x in card.get('type_line') for x in non_creature):
                    if card.get("cmc") <= 2:
                        lista = card.get('card_faces')

                        if any(x in lista[0]['oracle_text'] for x in cheap_ramp):
                            ramp += quantity[i]
                            land += quantity[i]

                        if any(x in lista[0]['oracle_text'] for x in cheap_draw):
                            draw += quantity[i]
                            land += quantity[i]

            if any(x in card.get("type_line") for x in ['Adventure']):
                # print(f'Adventure encontrada')
                if any(x in card.get('type_line') for x in non_creature):
                    if card.get("cmc") <= 2:
                        lista = card.get('card_faces')

                        if any(x in lista[0]['oracle_text'] for x in cheap_ramp):
                            ramp += quantity[i]
                            adventure += quantity[i]

                        if any(x in lista[0]['oracle_text'] for x in cheap_draw):
                            draw += quantity[i]
                            adventure += quantity[i]

            # print(f'PULEI {card.get("name")}')
            i += 1
            continue

        U += cost.count('U')*quantity[i]
        W += cost.count('W')*quantity[i]
        B += cost.count('B')*quantity[i]
        R += cost.count('R')*quantity[i]
        G += cost.count('G')*quantity[i]
        C += cost.count('C')*quantity[i]
        total += card.get('cmc')*quantity[i]
        # print('cost: ', cost)
        # print('total cmc: ', card.get('cmc'))
        # print('quantity: ', quantity)
        # print('quantity: ', quantity[i])

        # RAMP
        oracle_creature = ['Add {U}', 'Add {W}', 'Add {B}', 'Add {F}', 'Add {G}', 'Add {C}', 'Search',
                           'your library', 'land', 'basic', 'put a creature card with from your hand onto the battlefield']
        # print(card.get('name'))
        # print(f'ACHEI {card.get("name")}')
        # print(f'ACHEI {card.get("layout")}')
        if 'modal_dfc' in card.get('layout'):
            # print('MDFC/Battle ENCONTRADA')
            mdfc += quantity[i]
            # print('mdfc: ', mdfc)

        if 'Creature' in card.get('type_line'):
            # print('ACHEI')
            # print(f'ACHEI {card.get("type_line")}')
            if card.get('cmc') <= 2:
                # print('PASSEI NO CREATURE CMC')
                if any(x in card.get('oracle_text') for x in oracle_creature):
                    # print(f'Encontrei uma creature cheap ramp {quantity[i]} x {card.get("name")}')
                    ramp += quantity[i]
                    # print('ramp: ', ramp)

        if any(x in card.get('type_line') for x in non_creature):
            # print('CHEGUEI AQUI')
            # print(f'ACHEI {card.get("type_line")}')
            if card.get('cmc') <= 2:
                if any(x in card.get('oracle_text') for x in cheap_ramp):

                    # print(f'Localizei um non-creature cheap ramp {quantity[i]} x {card.get("name")}')
                    ramp += quantity[i]
                    # print('ramp: ', ramp)

        # DRAW

        oracle_creature_draw = ["draw a card", "draw two cards",
                                "draw three cards", "draws cards", "draws two cards", "draws three cards", 'look', 'put', 'your hand']

        if 'Creature' in card.get('type_line'):
            # print('ACHEI DRAW')
            if card.get('cmc') <= 2:
                # print('PASSEI NO CREATURE CMC DRAW')
                if any(x in card.get('oracle_text') for x in oracle_creature_draw):
                    # print('Encontrei uma creature cheap draw')
                    draw += quantity[i]
                    # print('draw creature: ', draw)

        non_creature = ['Instant', 'Sorcery', 'Battle', 'Enchantment']
        oracle_non_creature_draw = ["draw a card", "draw two cards",
                                    "draw three cards", "draws cards", "draws two cards", "draws three cards", 'look', 'put', 'your hand']

        if any(x in card.get('type_line') for x in non_creature):
            if card.get('cmc') <= 2:
                if any(x in card.get('oracle_text') for x in oracle_non_creature_draw):
                    # print('Encontrei um non-creature cheap draw')
                    draw += quantity[i]
                    # print('draw non-creature: ', draw)

        i = i + 1
        # print(i)

    # print('total final: ', total)
    # print(f'mdfc: {mdfc}\nramp final: {ramp}\ndraw final: {draw}')

    # NÃO TA CONTANDO ATRAXA E 3 RAMPS NÃO IDENTIFICADOS
    # CONTANDO BOSEIJU COMO CHEAP RAMP
    # ORACLE DAS BATALHAS NÃO ESTÁ SENDO SALVO NO CSV

    return U, W, B, R, G, C, total, ramp, draw


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

    arquivo = 'decklist.txt'
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
        # print(len(all_results))
    # for i in all_results:
        # print("LAYOUT: ", i.get('layout'))
        # print("NAME: ", i.get('name'))

        # print(f'{i.get("name")}: {i.get("mana_cost")}')
        # counter = collections.Counter()
        # counter = collections.Counter(i.get('mana_cost'))
        # print('Counter: ', counter.total)
        # print('total: ', collections.Counter(all_results))
        # print(all_results)
    U, W, B, R, G, C, total, n_ramp, n_draw = pips(all_results, quantidade)

    # print(f'TOTAL DE DRAW {n_draw} E RAMP {n_ramp} = {n_draw + n_ramp}')
    soma = n_draw + n_ramp
    # queries = separadas.split(';')

    # results = search(search_query)
    # all_results = []

    # for query in queries:
    #    results = search(query, 'exact')

    #    all_results.append(results)
    #    print('RESULTS: ', all_results)

    if all_results:
        # print(f'U: {U}, W: {W}, B: {B}, R: {R}, G: {G}, C: {C}')
        # print(
        #    f"Porcentagens:\nU:{round(U/(U+W+B+R+G)*100,2)}%\nW:{round(W/(U+W+B+R+G)*100, 2)}%\nB:{round(B/(U+W+B+R+G)*100,2)}%\nR:{round(R/(U+W+B+R+G)*100,2)}%\nG:{round(G/(U+W+B+R+G)*100,2)}%")
        # print('CMC Total: ', total)
        average_mana = round(total/sum(quantidade), 3)
        # print(f'Valor CMC Médio: ', average_mana)

        csv_filename = 'mtg_card_results.csv'
        save_to_csv(all_results, csv_filename, quantidade)
        print(
            # f'Numero de lands: {19.59 + 1.90*average_mana - 0.28*(n_ramp+n_draw)}')
            f'Numero de lands: {19.59 + 1.90*average_mana - 0.28*soma}')
        # 23.657700000000002
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

# Number of lands, counting MDFCs partially = 19.59 + 1.90 * average mana value – 0.28 *  + 0.27 * companion count.

'''
The number of cheap card draw spells. I defined a "cheap card draw spell" as a nonland card with mana value two or less whose lowercase 
Oracle text contains "draw a card", "draw two cards", "draw three cards", "draws cards", "draws two cards" or "draws three cards", but
not "{4}", "Blood token" and/or "investigate." Additionally, if it's a creature, then its Oracle text also needs to contain "when" and "
enters." A noncreature spell with mana value two or less and the words "look", "library", "put" and "your hand" but not "pay " or "pays"
also counts as a "cheap card draw spell." Finally, any spell that cycles for one mana also classifies as a "cheap card draw spell".
This lengthy definition means that the likes of Brainstorm, Faithless Looting, Deadly Dispute, Omen of the Sea, Growth Spiral, 
Drannith Stinger, Expressive Iteration, Manamorphose, Ice-Fang Coatl, etcetera are included, but Augur of Bolas, Trail of Crumbs,
Esper Sentinel, Fateful Absence, Ledger Shredder, Edgewall Innkeeper, Improbable Alliance, Ox of Agonas, Bloodtithe Harvester, Shark Typhoon,
Hydroid Krasis or Ravenous Squirrel are not.

The number of cheap mana ramp spells. I defined a "cheap mana ramp spell" as a nonland card with mana value two or less that is not already 
a "cheap card draw spell" and whose oracle text contains "add ", but not "add its ability", "add a lore counter" or, in case of a creature, "dies."
This includes Llanowar Elves, Skirk Prospector, Springleaf Drum, Lotus Cobra, Dark Ritual, etcetera, but not Ranger Class, Tangled Florahedron,
Shambling Ghast or Manamorphose. A nonland card with mana value two or less that is not already a "cheap card draw spell" was also classified as a
"cheap mana ramp spell" if its Oracle text contained either of the following three options: first, "search" and "your library" and ("land" or "basic")
but not "sacrifice." Second, "enchanted land is tapped" and "adds an additional." Third, "put a creature card with" and "from your hand onto the
battlefield." This includes Sylvan Scrying, Wolfwillow Haven and Aether Vial, but not Crop Rotation.


'''


# Fonte: https://www.channelfireball.com/article/How-Many-Lands-Do-You-Need-in-Your-Deck-An-Updated-Analysis/cd1c1a24-d439-4a8e-b369-b936edb0b38a/
