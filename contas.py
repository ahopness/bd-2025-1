from flask import request, session, redirect, url_for, jsonify
from markupsafe import escape

from app import app

import pymysql
from config import *

@app.post('/conta_entrar')
def conta_entrar_post():
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    if not email or not senha:
        return jsonify({'success': False, 'message': 'Email e senha são obrigatórios'})
    
    try:
        conta_entrar_connection = pymysql.connect(**DB_CONFIG)
        with conta_entrar_connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(f"""
                SELECT id_usuario, nome, email, senha 
                FROM usuarios 
                WHERE email = '{escape(email)}';
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
        if conta_entrar_connection.open:
            conta_entrar_connection.close()

@app.post('/conta_cadastrar')
def conta_cadastrar_post():
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    if not nome or not email or not senha:
        return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios'})
    
    try:
        conta_cadastrar_connection = pymysql.connect(**DB_CONFIG)
        with conta_cadastrar_connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(f"""
                SELECT id_usuario 
                FROM usuarios 
                WHERE email = '{escape(email)}';
            """)
            if cursor.fetchone():
                return jsonify({'success': False, 'message': 'Este email já está cadastrado'})
            
            cursor.execute(f"""
                INSERT INTO usuarios (nome, email, senha) 
                VALUES ('{escape(nome)}', '{escape(email)}', '{escape(senha)}');
            """)
            conta_cadastrar_connection.commit()
            
            session['user_id'] = cursor.lastrowid
            session['user_name'] = nome
            session['user_email'] = email
            
            return jsonify({'success': True, 'message': 'Cadastro realizado com sucesso'})
            
    except Exception as e:
        conta_cadastrar_connection.rollback()
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})
    finally:
        if conta_cadastrar_connection.open:
            conta_cadastrar_connection.close()

@app.post('/conta_sair')
def conta_sair_post():
    session.clear()
    return redirect(url_for('home_get'))

@app.post('/conta_deletar')
def conta_deletar_post():
    try:
        conta_deletar_connection = pymysql.connect(**DB_CONFIG)
        with conta_deletar_connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(f"""
                DELETE FROM usuarios 
                WHERE id_usuario = '{escape(session['user_id'])}';
            """)
            conta_deletar_connection.commit()

            session.clear()

            return jsonify({'success': True, 'message': 'Conta deletada com sucesso'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})
    finally:
        if conta_deletar_connection.open:
            conta_deletar_connection.close()