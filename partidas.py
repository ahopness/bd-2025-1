from flask import request, session, redirect, url_for, jsonify
from markupsafe import escape

from app import app

import pymysql
from config import *

@app.post('/partida')
def partida_criar():
    id_campeonato = request.form.get('id_campeonato')
    rodada = request.form.get('rodada')
    data_hora = request.form.get('data_hora')
    time_a = request.form.get('time_a')
    placar_time_a = request.form.get('placar_time_a')
    time_b = request.form.get('time_b')
    placar_time_b = request.form.get('placar_time_b')

    if not rodada or not data_hora or not data_hora or not time_a or not placar_time_a or not time_b or not placar_time_b:
        return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios'})

    try:
        criar_partida_connection = pymysql.connect(**DB_CONFIG)
        with criar_partida_connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(f"""
                INSERT INTO 
                    partidas (id_campeonato, rodada, data_hora, id_time_a, placar_time_a, id_time_b, placar_time_b) 
                VALUES 
                    ('{escape(id_campeonato)}', 
                    '{escape(rodada)}', 
                    '{escape(data_hora)}', 
                    (SELECT id_time FROM times WHERE nome = '{escape(time_a)}'), 
                    '{escape(placar_time_a)}', 
                    (SELECT id_time FROM times WHERE nome = '{escape(time_b)}'), 
                    '{escape(placar_time_b)}');
            """)
            criar_partida_connection.commit()
            
            return jsonify({'success': True, 'message': 'Partida criada com sucesso'})
            
    except Exception as e:
        criar_partida_connection.rollback()
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})
    finally:
        if criar_partida_connection.open:
            criar_partida_connection.close()

@app.delete('/partida')
def partida_deletar():
    id_partida = request.form.get('id_partida')

    try:
        partida_deletar_connection = pymysql.connect(**DB_CONFIG)
        with partida_deletar_connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(f"""
                DELETE FROM partidas
                WHERE id_partida = '{escape(id_partida)}';
            """)
            partida_deletar_connection.commit()

            return jsonify({'success': True, 'message': 'Partida deletada com sucesso'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})
    finally:
        if partida_deletar_connection.open:
            partida_deletar_connection.close()