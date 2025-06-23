from flask import request, session, jsonify
from markupsafe import escape

from app import app

import pymysql
from config import *

@app.put('/campeonato')
def campeonato_criar():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Você precisa estar logado para criar um campeonato'})
    
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    url_logo = request.form.get('url_logo')
    esporte = request.form.get('esporte')
    data_inicio = request.form.get('data_inicio')
    data_fim = request.form.get('data_fim')
    
    if not nome or not descricao or not url_logo or not esporte or not data_inicio or not data_fim:
        return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios'})
    
    try:
        criar_campeonato_connection = pymysql.connect(**DB_CONFIG)
        with criar_campeonato_connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(f"""
                SELECT id_campeonato FROM campeonatos WHERE nome = '{nome}';
            """)
            if cursor.fetchone():
                return jsonify({'success': False, 'message': 'Ja tem um campeonato com este nome'})
            
            cursor.execute(f"""
                INSERT INTO 
                    campeonatos (id_usuario, nome, descricao, url_logo, id_esporte, data_inicio, data_fim) 
                VALUES 
                    ('{escape(session['user_id'])}', 
                    '{escape(nome)}', 
                    '{escape(descricao)}', 
                    '{escape(url_logo)}', 
                    (SELECT id_esporte FROM esportes WHERE nome = '{escape(esporte)}'), 
                    '{escape(data_inicio)}', 
                    '{escape(data_fim)}');
            """)
            criar_campeonato_connection.commit()
            
            return jsonify({'success': True, 'message': 'Campeonato criado com sucesso'})
            
    except Exception as e:
        criar_campeonato_connection.rollback()
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})
    finally:
        if criar_campeonato_connection.open:
            criar_campeonato_connection.close()

@app.delete('/campeonato')
def campeonato_deletar():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Você precisa estar logado para deletar um campeonato'})
    
    id_campeonato = request.form.get('id_campeonato')

    try:
        campeonato_deletar_connection = pymysql.connect(**DB_CONFIG)
        with campeonato_deletar_connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(f"""
                SELECT id_usuario FROM campeonatos 
                WHERE id_campeonato = '{escape(id_campeonato)}';
            """)
            campeonato_atual = cursor.fetchone()
            
            if not campeonato_atual:
                return jsonify({'success': False, 'message': 'Campeonato não encontrado'})
            
            if str(campeonato_atual['id_usuario']) != str(session['user_id']):
                return jsonify({'success': False, 'message': 'Você só pode deletar seus próprios campeonatos'})
            
            cursor.execute(f"""
                DELETE FROM campeonatos
                WHERE id_campeonato = '{escape(id_campeonato)}';
            """)
            campeonato_deletar_connection.commit()

            return jsonify({'success': True, 'message': 'Campeonato deletado com sucesso'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})
    finally:
        if campeonato_deletar_connection.open:
            campeonato_deletar_connection.close()

@app.patch('/campeonato')
def campeonato_editar():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Você precisa estar logado para alterar um campeonato'})
    
    id_campeonato = request.form.get('id_campeonato')
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    url_logo = request.form.get('url_logo')
    esporte = request.form.get('esporte')
    data_inicio = request.form.get('data_inicio')
    data_fim = request.form.get('data_fim')
    
    if not id_campeonato or not nome or not descricao or not url_logo or not esporte or not data_inicio or not data_fim:
        return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios'})
    
    try:
        alterar_campeonato_connection = pymysql.connect(**DB_CONFIG)
        with alterar_campeonato_connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(f"""
                SELECT id_campeonato, id_usuario FROM campeonatos 
                WHERE id_campeonato = '{escape(id_campeonato)}';
            """)
            campeonato_atual = cursor.fetchone()
            
            if not campeonato_atual:
                return jsonify({'success': False, 'message': 'Campeonato não encontrado'})
            
            if str(campeonato_atual['id_usuario']) != str(session['user_id']):
                return jsonify({'success': False, 'message': 'Você só pode alterar seus próprios campeonatos'})
            
            cursor.execute(f"""
                SELECT id_campeonato FROM campeonatos 
                WHERE nome = '{escape(nome)}' AND id_campeonato != '{escape(id_campeonato)}';
            """)
            if cursor.fetchone():
                return jsonify({'success': False, 'message': 'Já existe um campeonato com este nome'})
            
            cursor.execute(f"""
                UPDATE campeonatos 
                SET nome = '{escape(nome)}', 
                    descricao = '{escape(descricao)}', 
                    url_logo = '{escape(url_logo)}', 
                    id_esporte = (SELECT id_esporte FROM esportes WHERE nome = '{escape(esporte)}'), 
                    data_inicio = '{escape(data_inicio)}', 
                    data_fim = '{escape(data_fim)}'
                WHERE id_campeonato = '{escape(id_campeonato)}';
            """)
            alterar_campeonato_connection.commit()
            
            return jsonify({'success': True, 'message': 'Campeonato alterado com sucesso'})
            
    except Exception as e:
        alterar_campeonato_connection.rollback()
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})
    finally:
        if alterar_campeonato_connection.open:
            alterar_campeonato_connection.close()