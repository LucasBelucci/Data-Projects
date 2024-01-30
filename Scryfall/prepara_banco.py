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
