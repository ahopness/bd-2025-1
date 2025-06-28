from flask import request, session, redirect, url_for, jsonify
from markupsafe import escape
import re

from app import app

import pymysql
from config import *

@app.put('/time')
def time_criar():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Você precisa estar logado para criar um time'})
    
    id_campeonato = request.form.get('id_campeonato')
    nome = request.form.get('nome')
    url_logo = request.form.get('url_logo')

    if not id_campeonato or not nome or not url_logo:
        return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios'})

    if re.match(r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$', url_logo) is None:
        return jsonify({'success': False, 'message': 'URL invalida'})

    try:
        criar_time_connection = pymysql.connect(**DB_CONFIG)
        with criar_time_connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(f"""
                SELECT id_usuario FROM campeonatos 
                WHERE id_campeonato = '{escape(id_campeonato)}';
            """)
            campeonato = cursor.fetchone()
            
            if not campeonato:
                return jsonify({'success': False, 'message': 'Campeonato não encontrado'})
            
            if str(campeonato['id_usuario']) != str(session['user_id']):
                return jsonify({'success': False, 'message': 'Você só pode criar times nos seus próprios campeonatos'})
            
            cursor.execute(f"""
                SELECT id_time FROM times WHERE id_campeonato = '{id_campeonato}' AND nome = '{nome}';
            """)
            if cursor.fetchone():
                return jsonify({'success': False, 'message': 'Ja tem um time com este nome'})
            
            cursor.execute(f"""
                INSERT INTO 
                    times (id_campeonato, nome, url_logo) 
                VALUES 
                    ('{escape(id_campeonato)}', 
                    '{escape(nome)}', 
                    '{escape(url_logo)}');
            """)
            criar_time_connection.commit()
            
            return jsonify({'success': True, 'message': 'Time criado com sucesso'})
            
    except Exception as e:
        criar_time_connection.rollback()
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})
    finally:
        if criar_time_connection.open:
            criar_time_connection.close()

@app.delete('/time')
def time_deletar():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Você precisa estar logado para deletar um time'})
    
    id_time = request.form.get('id_time')

    try:
        time_deletar_connection = pymysql.connect(**DB_CONFIG)
        with time_deletar_connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(f"""
                SELECT t.id_time, c.id_usuario 
                FROM times t
                INNER JOIN campeonatos c ON c.id_campeonato = t.id_campeonato
                WHERE t.id_time = '{escape(id_time)}';
            """)
            time_atual = cursor.fetchone()
            
            if not time_atual:
                return jsonify({'success': False, 'message': 'Time não encontrado'})
            
            if str(time_atual['id_usuario']) != str(session['user_id']):
                return jsonify({'success': False, 'message': 'Você só pode deletar times dos seus próprios campeonatos'})
            
            cursor.execute(f"""
                DELETE FROM times 
                WHERE id_time = '{escape(id_time)}';
            """)
            time_deletar_connection.commit()

            return jsonify({'success': True, 'message': 'Time deletado com sucesso'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})
    finally:
        if time_deletar_connection.open:
            time_deletar_connection.close()

@app.patch('/time')
def time_editar():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Você precisa estar logado para editar um time'})
    
    id_time = request.form.get('id_time')
    id_campeonato = request.form.get('id_campeonato')
    nome = request.form.get('nome')
    url_logo = request.form.get('url_logo')
    
    if not id_time or not id_campeonato or not nome or not url_logo:
        return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios'})
    
    try:
        editar_time_connection = pymysql.connect(**DB_CONFIG)
        with editar_time_connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(f"""
                SELECT t.id_time, c.id_usuario 
                FROM times t
                INNER JOIN campeonatos c ON c.id_campeonato = t.id_campeonato
                WHERE t.id_time = '{escape(id_time)}' AND t.id_campeonato = '{escape(id_campeonato)}';
            """)
            time_atual = cursor.fetchone()
            
            if not time_atual:
                return jsonify({'success': False, 'message': 'Time não encontrado'})
            
            if str(time_atual['id_usuario']) != str(session['user_id']):
                return jsonify({'success': False, 'message': 'Você só pode editar times dos seus próprios campeonatos'})
            
            cursor.execute(f"""
                SELECT id_time FROM times 
                WHERE id_campeonato = '{escape(id_campeonato)}' 
                AND nome = '{escape(nome)}' 
                AND id_time != '{escape(id_time)}';
            """)
            if cursor.fetchone():
                return jsonify({'success': False, 'message': 'Já existe um time com este nome neste campeonato'})
            
            cursor.execute(f"""
                UPDATE times 
                SET nome = '{escape(nome)}', url_logo = '{escape(url_logo)}'
                WHERE id_time = '{escape(id_time)}';
            """)
            editar_time_connection.commit()
            
            return jsonify({'success': True, 'message': 'Time editado com sucesso'})
            
    except Exception as e:
        editar_time_connection.rollback()
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})
    finally:
        if editar_time_connection.open:
            editar_time_connection.close()