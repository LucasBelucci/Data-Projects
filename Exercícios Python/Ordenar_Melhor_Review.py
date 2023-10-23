# tuples = [[123, 1], [234, 4], [123, 6], [345, 5]]
# final = [[123, 3.5], [234, 4], [345, 5]]

def separa_tup(tup):
    lista = []
    review = []
    repeticoes = []

    for i in tup:
        index = 0
        if len(lista) == 0:
            lista.append(i[0])
            review.append(i[1])
            repeticoes.append(1)
            continue
        if i[0] in lista:
            index = lista.index(i[0])
            new_value = (review[index] + i[1])
            review[index] = new_value
            repeticoes[index] = repeticoes[index] + 1
        else:
            lista.append(i[0])
            review.append(i[1])
            repeticoes.append(1)
    return lista, review, repeticoes


def add_tuple(review, lista, repeticoes):
    lista_final = []
    for i in range(len(review)):
        lista_final.append(tuple([lista[i], review[i]/repeticoes[i]]))
    encontra_maior(lista_final)
    return lista_final


def encontra_maior(tup):
    tup.sort(key=lambda a: a[1], reverse=True)
    return tup


def teste(tup):

    if len(tup) == 0:
        return 'Lista vazia'

    lista, review, repeticoes = separa_tup(tup)
    lista_final = add_tuple(review, lista, repeticoes)

    if lista_final == 'Lista vazia':
        return 'Lista vazia'
    else:
        return lista_final[0]


tup0 = [[123, 4]]
tup1 = [[123, 4], [222, 5], [342, 3], [123, 5], [222, 2], [123, 9]]
tup2 = [[123, 4], [222, 5], [342, 3]]
tup3 = []
tup4 = [[123, 4], [123, 4], [123, 4], [123, 4],
        [123, 4], [123, 4], [123, 4], [123, 4]]
tup5 = [[123, 4], [222, 5], [222, 5],  [123, 5], [222, 2], [123, 9]]
tup6 = [[123, 4], [222, 5], [342, 3], [555, 5], [888, 2], [999, 9]]
tup7 = [[123, 4], [222, 15], [342, 3], [123, 5], [222, 2], [123, 9]]


if teste(tup0) == (123, 4.0):
    print('Passou no Teste 0')
else:
    print('Reprovado Teste 0')

if teste(tup1) == (123, 6.0):
    print('Passou no Teste 1')
else:
    print('Reprovou Teste 1')

if teste(tup2) == (222, 5.0):
    print('Passou no Teste 2')
else:
    print('Reprovou Teste 2')

if teste(tup3) == 'Lista vazia':
    print('Passou no Teste 3')
else:
    print('Reprovou no Teste 3')

if teste(tup4) == (123, 4.0):
    print('Passou no Teste 4')
else:
    print('Reprovou no Teste 4')

if teste(tup5) == (123, 6.0):
    print('Passou no Teste 5')
else:
    print('Reprovou no Teste 5')

if teste(tup6) == (999, 9.0):
    print('Passou no Teste 6')
else:
    print('Reprovou no Teste 6')

if teste(tup7) == (222, 8.5):
    print('Passou no Teste 7')
else:
    print('Reprovou no Teste 7')
