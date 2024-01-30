import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash
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

cursor.execute("DROP DATABASE IF EXISTS `AGENDA`;")

cursor.execute("CREATE DATABASE `AGENDA`;")

cursor.execute("USE `AGENDA`;")

# criando tabelas
# 2 tabelas = usuários e tarefas

TABLES = {}
TABLES['Tarefas'] = ('''
        CREATE TABLE `TAREFAS`(
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `tarefa`varchar(120) NOT NULL,
            `descricao` varchar(500),
            `prioridade` varchar(50),
            `completa` boolean DEFAULT 0,   
            PRIMARY KEY(`id`)    
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

# TABLES['Tarefas'] = ('''
#        CREATE TABLE `tarefas` (
#        `id` int(11) NOT NULL AUTO_INCREMENT,
#        `tarefa` varchar(50) NOT NULL,
#        `data` datetime NOT NULL DEFAULT ('0000-00-00 00:00:00'),
#        `duracao` float(10),
#        PRIMARY KEY (`id`)
#        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
    CREATE TABLE `USUARIOS` (
        `nome` varchar(20) NOT NULL,
        `nickname` varchar(8) NOT NULL,
        `senha` varchar(100) NOT NULL,
        PRIMARY KEY (`nickname`)    
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

# inserindo usuarios

usuarios_sql = 'INSERT INTO USUARIOS(nome, nickname, senha) VALUES (%s, %s, %s)'

usuarios = [
    ('Lucas Belucci', 'Lucas', generate_password_hash('1234').decode('utf-8')),
    ('Pedro', 'Pedro', generate_password_hash('abcd').decode('utf-8'))
]

cursor.executemany(usuarios_sql, usuarios)

cursor.execute('SELECT * FROM AGENDA.usuarios')
print(' ------------ Usuários: ------------')
for user in cursor.fetchall():
    print(user[1])

print('Inserindo tarefas')
# inserindo tasks
task_sql = 'INSERT INTO TAREFAS (tarefa, descricao, prioridade, completa) VALUES (%s, %s, %s, %s)'
# date = [('2023-10-25 19:30:00'), ('2023-10-28 07:00:00'), ('2023-10-30 13:30:00'),
#        ('2023-11-02 07:00:00'), ('2023-12-25 01:00:00'), ('2023-12-31 23:00:00')]
# formated_date = [date[0].strptime('%Y-%m-%d %H:%M:%S'), date[1].strftime('%Y-%m-%d %H:%M:%S'), date[2].strftime(
#    '%Y-%m-%d %H:%M:%S'), date[3].strftime('%Y-%m-%d %H:%M:%S'), date[4].strftime('%Y-%m-%d %H:%M:%S'), date[5].strftime('%Y-%m-%d %H:%M:%S')]

tasks = [
    ('Magic', 'Jogar magic as quartas', 'Média', 0),
    ('Passeio', 'Dar uma volta para conhecer a cidade', 'Baixa', 1),
    ('Entrevista', 'Preparação para a entrevista', 'Alta', 0),
    ('Viagem', 'Preparação para a viagem do final de semana', 'Média', 1),
    ('Natal', 'Procurar locais para passar o Natal', 'Alta', 0),
    ('Ano Novo', 'Acertar o local para a virada do ano', 'Baixa', 0)
]

'''
tasks = [
    ('Magic', datetime(2023, 10, 25, 19, 30, 0), '04'),
    ('Passeio', datetime(2023, 10, 28, 7, 00, 0), '42'),
    ('Entrevista', datetime(2023, 10, 30, 13, 30, 0), '2.5'),
    ('Viagem', datetime(2023, 11, 2, 7, 00, 0), '12'),
    ('Natal', datetime(2023, 12, 25, 1, 00, 0), '15'),
    ('Ano Novo', datetime(2023, 12, 31, 23, 00, 0), '05')
]
'''

cursor.executemany(task_sql, tasks)

cursor.execute('SELECT * FROM AGENDA.TAREFAS')
print('------------ Tasks: ------------')

for tarefa in cursor.fetchall():
    print('id ----- tarefa ----- descricao ----- prioridade ----- completa ')
    print(tarefa)

# Realizando o commit
conn.commit()

# Finalizando as instâncias
cursor.close()
conn.close()
