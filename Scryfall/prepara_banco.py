import mysql.connector
from mysql.connector import errorcode


print('Conectado...')

# Conectando ao servidor MySQL

try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='admin')

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no usuário ou senha')

    else:
        print(err)


cursor = conn.cursor()
cursor.execute('DROP DATABASE IF EXISTS `DECKS`;')
cursor.execute('CREATE DATABASE `DECKS`;')
cursor.execute('USE `DECKS`;')

TABLES = {}
TABLES['DECKS'] = ('''CREATE TABLE `DECKS`(
                   `id` int(11) NOT NULL AUTO_INCREMENT,
                   `comandante` varchar(120) NOT NULL,
                   `player_name` varchar(120) NOT NULL,
                   `standing` int(11) NOT NULL,
                   `wins` int(11) NOT NULL,
                   `loses` int(11) NOT NULL,
                   `draws` int(11) NOT NULL,
                   `winrate` int(11) NOT NULL,
                   `tournament` varchar(120) NOT NULL,
                   PRIMARY_KEY(`id`)
                   ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['TORNEIOS'] = ('''CREATE TABLE `TORNEIOS`(
                      `id` int(11) NOT NULL AUTO_INCREMENT,
                      `nome` varchar(120) NOT NULL,
                      `size` int(11),
                      `date` datetime NOT NULL DEFAULT ('0000-00-00'),
                      PRIMARY_KEY(`id`)
                      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''CREATE TABLE `USUARIOS`(
                      `nome` varchar(20) NOT NULL,
                      `nickname` varchar(8) NOT NULL,
                      `email` varchar(20) NOT NULL,
                      `senha` varchar(100) NOT NULL,
                      PRIMARY_KEY(`email`)
                      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

# Tabelas e páginas necessárias
# --------------------------------------- ## ------------------------------------------


# DECKS - Salva Name Comandante/ Top 16s/ Entries / Conversion / Colors - TABELA DERIVADA
# Comandantes - Salva Player Name / Standing / Wins / Losses / Draws / Winrate / Tournament - TABELA DECKS
# Tournaments - Salva Name / size / Date - TABELA TORNEIO
# Inside Tournaments - Salva Player Name / Commander / Wins / Losses / Draws / Winrate / Colors - TABELA DECKS (?)


for tabela in TABLES:
    tabela_sql = TABLES[tabela]
    try:
        print('Criando tabela {}:'.format(tabela), end=' ')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Já existe')
        else:
            print(err.msg)
    else:
        print('Tabela criada {}:'.format(tabela), end=' ')
