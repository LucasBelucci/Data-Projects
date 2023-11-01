import os
from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators


class FormularioTarefa(FlaskForm):
    tarefa = StringField('Nome da Tarefa', [
                         validators.DataRequired(), validators.length(min=1, max=120)])
    descricao = StringField('Descrição da tarefa', [
                            validators.DataRequired(), validators.length(min=0, max=500)])
    prioridade = StringField(
        'Prioridade', [validators.DataRequired(), validators.length(min=0, max=50)])
    salvar = SubmitField('Salvar')


class FormularioUsuario(FlaskForm):
    nickname = StringField(
        'Nickname', [validators.DataRequired(), validators.length(min=1, max=8)])
    senha = PasswordField(
        'Senha', [validators.DataRequired(), validators.length(min=1, max=100)])
    login = SubmitField('Login')
