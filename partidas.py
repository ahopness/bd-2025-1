from flask import request, session, redirect, url_for, jsonify
from markupsafe import escape

from app import app

import pymysql
from config import *

@app.put('/partida')
def partida_criar():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Você precisa estar logado para criar uma partida'})
    
    id_campeonato = request.form.get('id_campeonato')
    rodada = request.form.get('rodada')
    data = request.form.get('data')
    hora = request.form.get('hora')
    time_a = request.form.get('time_a')
    placar_time_a = request.form.get('placar_time_a')
    time_b = request.form.get('time_b')
    placar_time_b = request.form.get('placar_time_b')

    if not id_campeonato or not rodada or not data or not hora or not time_a or not time_b:
        return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios (placares podem ser deixados vazios)'})

    try:
        criar_partida_connection = pymysql.connect(**DB_CONFIG)
        with criar_partida_connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(f"""
                SELECT id_usuario FROM campeonatos 
                WHERE id_campeonato = '{escape(id_campeonato)}';
            """)
            campeonato = cursor.fetchone()
            
            if not campeonato:
                return jsonify({'success': False, 'message': 'Campeonato não encontrado'})
            
            if str(campeonato['id_usuario']) != str(session['user_id']):
                return jsonify({'success': False, 'message': 'Você só pode criar partidas nos seus próprios campeonatos'})
            
            if time_a == time_b:
                return jsonify({'success': False, 'message': 'Um time não pode jogar contra si mesmo'})

            placar_a_value = f"'{escape(placar_time_a)}'" if placar_time_a else "NULL"
            placar_b_value = f"'{escape(placar_time_b)}'" if placar_time_b else "NULL"
            
            cursor.execute(f"""
                INSERT INTO 
                    partidas (id_campeonato, rodada, data, hora, id_time_a, placar_time_a, id_time_b, placar_time_b) 
                VALUES 
                    ('{escape(id_campeonato)}', 
                    '{escape(rodada)}', 
                    '{escape(data)}', 
                    '{escape(hora)}', 
                    (SELECT id_time FROM times WHERE nome = '{escape(time_a)}'), 
                    {placar_a_value}, 
                    (SELECT id_time FROM times WHERE nome = '{escape(time_b)}'), 
                    {placar_b_value});
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
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Você precisa estar logado para deletar uma partida'})
    
    id_partida = request.form.get('id_partida')

    try:
        partida_deletar_connection = pymysql.connect(**DB_CONFIG)
        with partida_deletar_connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(f"""
                SELECT p.id_partida, c.id_usuario 
                FROM partidas p
                INNER JOIN campeonatos c ON c.id_campeonato = p.id_campeonato
                WHERE p.id_partida = '{escape(id_partida)}';
            """)
            partida_atual = cursor.fetchone()
            
            if not partida_atual:
                return jsonify({'success': False, 'message': 'Partida não encontrada'})
            
            if str(partida_atual['id_usuario']) != str(session['user_id']):
                return jsonify({'success': False, 'message': 'Você só pode deletar partidas dos seus próprios campeonatos'})
            
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

@app.patch('/partida')
def partida_editar():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Você precisa estar logado para editar uma partida'})
    
    id_partida = request.form.get('id_partida')
    id_campeonato = request.form.get('id_campeonato')
    rodada = request.form.get('rodada')
    data = request.form.get('data')
    hora = request.form.get('hora')
    time_a = request.form.get('time_a')
    placar_time_a = request.form.get('placar_time_a')
    time_b = request.form.get('time_b')
    placar_time_b = request.form.get('placar_time_b')
    
    if not id_partida or not id_campeonato or not rodada or not data or not hora or not time_a or not time_b:
        return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios (placares podem ser deixados vazios)'})
    
    try:
        editar_partida_connection = pymysql.connect(**DB_CONFIG)
        with editar_partida_connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(f"""
                SELECT p.id_partida, c.id_usuario 
                FROM partidas p
                INNER JOIN campeonatos c ON c.id_campeonato = p.id_campeonato
                WHERE p.id_partida = '{escape(id_partida)}' AND p.id_campeonato = '{escape(id_campeonato)}';
            """)
            partida_atual = cursor.fetchone()
            
            if not partida_atual:
                return jsonify({'success': False, 'message': 'Partida não encontrada'})
            
            if str(partida_atual['id_usuario']) != str(session['user_id']):
                return jsonify({'success': False, 'message': 'Você só pode editar partidas dos seus próprios campeonatos'})
            
            if time_a == time_b:
                return jsonify({'success': False, 'message': 'Um time não pode jogar contra si mesmo'})
            
            placar_a_value = f"'{escape(placar_time_a)}'" if placar_time_a else "NULL"
            placar_b_value = f"'{escape(placar_time_b)}'" if placar_time_b else "NULL"
            
            # Atualizar a partida
            cursor.execute(f"""
                UPDATE partidas 
                SET rodada = '{escape(rodada)}', 
                    data = '{escape(data)}',
                    hora = '{escape(hora)}', 
                    id_time_a = (SELECT id_time FROM times WHERE nome = '{escape(time_a)}'), 
                    placar_time_a = {placar_a_value}, 
                    id_time_b = (SELECT id_time FROM times WHERE nome = '{escape(time_b)}'), 
                    placar_time_b = {placar_b_value}
                WHERE id_partida = '{escape(id_partida)}';
            """)
            editar_partida_connection.commit()
            
            return jsonify({'success': True, 'message': 'Partida editada com sucesso'})
            
    except Exception as e:
        editar_partida_connection.rollback()
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'})
    finally:
        if editar_partida_connection.open:
            editar_partida_connection.close()