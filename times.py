from flask import request, session, redirect, url_for, jsonify
from markupsafe import escape

from app import app

import pymysql
from config import *

@app.post('/time')
def time_criar():
    id_campeonato = request.form.get('id_campeonato')
    nome = request.form.get('nome')
    url_logo = request.form.get('url_logo')

    if not nome or not url_logo:
        return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios'})

    try:
        criar_time_connection = pymysql.connect(**DB_CONFIG)
        with criar_time_connection.cursor(pymysql.cursors.DictCursor) as cursor:
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
    id_time = request.form.get('id_time')

    try:
        time_deletar_connection = pymysql.connect(**DB_CONFIG)
        with time_deletar_connection.cursor(pymysql.cursors.DictCursor) as cursor:
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