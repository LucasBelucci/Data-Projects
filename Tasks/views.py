from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from app import app, db
from models import Tarefas, Usuarios
from helpers import FormularioTarefa, FormularioUsuario
from flask_bcrypt import check_password_hash


@app.route('/')
def index():
    tasks = Tarefas.query.order_by(Tarefas.id)
    print(request.method)
    return render_template('lista.html', tasks=tasks)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioTarefa()
    return render_template('novo.html', titulo='Nova Tarefa', form=form)


@app.route('/criar', methods=['POST', 'GET'])
def criar():
    form = FormularioTarefa(request.form)
    print('form: ', form)
    # if not form.validate_on_submit():
    #    return redirect(url_for('novo'))

    tarefa = form.tarefa.data
    descricao = form.descricao.data
    prioridade = form.prioridade.data

    # tarefa = request.form.get('tarefa')
    # descricao = request.form.get('descricao')
    # prioridade = request.form.get('prioridade')

    task = Tarefas.query.filter_by(tarefa=tarefa).first()

    if task:
        flash('Tarefa já existente!')
        return redirect(url_for('index'))

    nova_tarefa = Tarefas(tarefa=tarefa, descricao=descricao,
                          prioridade=prioridade)
    db.session.add(nova_tarefa)
    db.session.commit()

    # print(request.method)
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    tarefa = Tarefas.query.filter_by(id=id).first()
    form = FormularioTarefa()
    form.tarefa.data = tarefa.nome
    form.descricao.data = tarefa.descricao
    form.prioridade.data = tarefa.prioridade
    tarefa.completa = 1
    return render_template('editar.html', id=id, form=form)


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, form=form)


@app.route('/autentica', methods=['POST', ])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)
    if usuario and senha:
        session['usuario_logado'] = usuario.nickname
        flash(usuario.nickname + ' logado com sucesso')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        flash('Usuário não logado!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))
