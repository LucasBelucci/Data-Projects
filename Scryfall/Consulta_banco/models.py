from app import db


class Tarefas(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tarefa = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.String(500))
    prioridade = db.Column(db.String(50))
    completa = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name
