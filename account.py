from flask import request, session, redirect, url_for, jsonify

from app import app

import pymysql
from config import *

@app.post('/login')
def login_post():
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    if not email or not senha:
        return jsonify({'success': False, 'message': 'Email e senha são obrigatórios'})
    
    try:
        login_connection = pymysql.connect(**DB_CONFIG)
        with login_connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(f"""
                SELECT id_usuario, nome, email, senha 
                FROM usuarios 
                WHERE email = '{email}';
            """)
            usuario = cursor.fetchone()
            
            if usuario and usuario['senha'] == senha:
                session['user_id'] = usuario['id_usuario']
                session['user_name'] = usuario['nome']
                session['user_email'] = usuario['email']
                return jsonify({'success': True, 'message': 'Login realizado com sucesso'})
            else:
                return jsonify({'success': False, 'message': 'Email ou senha incorretos'})
                
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})
    finally:
        if login_connection.open:
            login_connection.close()

@app.post('/signin')
def signin_post():
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    if not nome or not email or not senha:
        return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios'})
    
    try:
        signin_connection = pymysql.connect(**DB_CONFIG)
        with signin_connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(f"""
                SELECT id_usuario FROM usuarios WHERE email = '{email}';
            """)
            if cursor.fetchone():
                return jsonify({'success': False, 'message': 'Este email já está cadastrado'})
            
            cursor.execute(f"""
                INSERT INTO usuarios (nome, email, senha) 
                VALUES ('{nome}', '{email}', '{senha}');
            """)
            signin_connection.commit()
            
            session['user_id'] = cursor.lastrowid
            session['user_name'] = nome
            session['user_email'] = email
            
            return jsonify({'success': True, 'message': 'Cadastro realizado com sucesso'})
            
    except Exception as e:
        signin_connection.rollback()
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})
    finally:
        if signin_connection.open:
            signin_connection.close()

@app.post('/logout')
def logout_post():
    session.clear()
    return redirect(url_for('home_get'))