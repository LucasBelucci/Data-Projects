import mysql.connector

db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='admin'
)
cursor = db.cursor()

cursor.execute('USE tarefas')


def get_tasks():
    cursor.execute("SELECT id, task, done FROM tasks")
    return [{'id': id, 'task': task, 'done': done} for (id, task, done) in cursor]


def create_task(task):
    cursor.execute(
        "INSERT INTO tasks (task, done) VALUES (%s, %s)", (task, False))
    db.commit()
    return cursor.lastrowid


def update_task(task_id, done):
    cursor.execute("UPDATE tasks SET done = %s WHERE id = %s", (done, task_id))
    db.commit()


def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    db.commit()
