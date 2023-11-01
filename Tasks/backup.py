'''
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

app = Flask(__name__)

app.config.from_pyfile('config.py')

# db = SQLAlchemy(app)

db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='admin'
)

cursor = db.cursor()


@app.route('/', methods=['GET'])
def get_tasks():
    cursor.execute("SELECT * FROM AGENDA.TAREFAS ORDER BY id ASC")
    tasks = [{'id': id, 'tarefa': tarefa, 'descricao': descricao, 'prioridade': prioridade,
              'completa': completa} for (id, tarefa, descricao, prioridade, completa) in cursor]
    # return jsonify({'tasks': tasks})
    return render_template('lista.html', tasks=tasks)


@app.route('/criar', methods=['GET', 'POST'])
def create_task():

    tarefa = request.form['tarefa']
    descricao = request.form['descricao']
    prioridade = request.form['prioridade']
    completa = request.form['completa']
    task = (tarefa, descricao, prioridade, completa)
    novo_jogo = "INSERT INTO TAREFAS (tarefa, descricao, prioridade, completa) VALUES (%s, %s, %s, %s)"
    cursor.executemany(novo_jogo, task)

    return redirect(url_for('get_tasks'))


if __name__ == '__main__':
    app.run(debug=True)
'''
