from flask import request, session, jsonify

from app import app

import pymysql
from config import *

@app.post('/criar_campeonato')
def criar_campeonato():
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
                INSERT INTO campeonatos (id_usuario, nome, descricao, url_logo, id_esporte, data_inicio, data_fim) 
                VALUES ('{session['user_id']}', '{nome}', '{descricao}', '{url_logo}', (SELECT id_esporte FROM esportes WHERE nome = '{esporte}'), '{data_inicio}', '{data_fim}');
            """)
            criar_campeonato_connection.commit()
            
            return jsonify({'success': True, 'message': 'Campeonato criado com sucesso'})
            
    except Exception as e:
        criar_campeonato_connection.rollback()
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})
    finally:
        if criar_campeonato_connection.open:
            criar_campeonato_connection.close()