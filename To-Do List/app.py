from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from database import create_task, get_tasks, update_task, delete_task, db
app = Flask(__name__)

app.config.from_pyfile('config.py')


@app.route('/tasks', methods=['POST'])
def create_new_task():
    data = request.get_json()
    if 'task' in data:
        task = data['task']
        task_id = create_task(task)
        return jsonify({'message': 'Tarefa criada com sucesso', 'task_id': task_id}), 201
    else:
        return jsonify({'error': 'O campo "task" é obrigatório.'}), 400


@app.route('/tasks', methods=['GET'])
def list_tasks():
    tasks = get_tasks()
    return jsonify({'tasks': tasks})


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_tasks(task_id):
    data = request.get_json()
    if 'done' in data:
        done = data['done']
        update_task(task_id, done)
        return jsonify({'message': 'Tarefa atualizada com sucesso!'})
    else:
        return jsonify({'error': 'O campo "done" é obrigatório'}), 400


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def remove_task(task_id):
    delete_task(task_id)
    return jsonify({'message': 'Tarefa deletada com sucesso!'})


if __name__ == '__main__':
    app.run(debug=True)
