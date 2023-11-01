import mysql.connector
from mysql.connector import errorcode

# from datetime import datetime

print('Conectado...')

# Conectando ao servidor MySQL

try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='admin',
        # database='Agenda'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)

# Instanciando o cursor no servidor MySQL para execução dos comandos SQL

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `tarefas`;")

cursor.execute("CREATE DATABASE `tarefas`;")

cursor.execute("USE `tarefas`;")

# criando tabelas
# 2 tabelas = usuários e tarefas

TABLES = {}
TABLES['Tarefas'] = ('''
        CREATE TABLE `tasks`(
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `task`varchar(255) NOT NULL,
            `done` boolean NOT NULL DEFAULT 0,   
            PRIMARY KEY(`id`)    
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

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
        print('OK')

print('Inserindo tarefas')
# inserindo tasks
task_sql = 'INSERT INTO tasks (task, done) VALUES (%s, %s)'

tasks = [
    ('Jogar magic as quartas', 0),
    ('Preparação para a entrevista', 0),
    ('Preparação para a viagem do final de semana', 1),
]


cursor.executemany(task_sql, tasks)

cursor.execute('SELECT * FROM AGENDA.TAREFAS')
print('------------ Tasks: ------------')

for tarefa in cursor.fetchall():
    print('id ----- tarefa -----  completa ')
    print(tarefa)

# Realizando o commit
conn.commit()

# Finalizando as instâncias
cursor.close()
conn.close()
