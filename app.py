from flask import Flask, render_template, session, request
from markupsafe import escape

app = Flask(__name__)
app.secret_key = 'segredo'

import pymysql
from config import *
from utils import *

from contas import *
from campeonatos import *
from times import *
from partidas import *

@app.get('/')
def home_get():
    try:
        home_connection = pymysql.connect(**DB_CONFIG)
    except Exception as e:
        return "Service Unavailable: {str(e)}", 503

    try:
        with home_connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT
                    id_campeonato,
                    id_usuario,
                    nome,
                    url_logo,
                    CASE
                        WHEN data_inicio > CURDATE() THEN 'Em breve'
                        WHEN data_fim < CURDATE() THEN 'Terminou'
                        ELSE 'Em andamento'
                    END AS andamento
                FROM campeonatos
            """)
            campeonatos = cursor.fetchall()

            cursor.execute("""
                SELECT nome
                FROM esportes
                ORDER BY nome ASC
            """)
            esportes = cursor.fetchall()

            usuario = None
            if 'user_id' in session:
                cursor.execute(f"""
                    SELECT id_usuario, nome, email 
                    FROM usuarios 
                    WHERE id_usuario = '{escape(session['user_id'])}';
                """)
                usuario = cursor.fetchone()

        return render_template('home.html.jinja', campeonatos=campeonatos, usuario=usuario, esportes=esportes)
    except Exception as e:
        home_connection.rollback()
        return f"Internal Server Error: {str(e)}", 500
    finally:
        if home_connection.open:
            home_connection.close()

@app.get('/campeonato')
def campeonato_get():
    usuario = None
    id_campeonato = request.args.get('id')
    
    if not id_campeonato:
        return redirect(url_for('home_get'))
        
    try:
        campeonato_connection = pymysql.connect(**DB_CONFIG)
        with campeonato_connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(f"""
                SELECT 
                    campeonatos.id_campeonato, 
                    usuarios.nome AS usuario_nome,
                    usuarios.email AS usuario_email,
                    campeonatos.nome, 
                    campeonatos.descricao,
                    campeonatos.url_logo,
                    esportes.nome AS esporte_nome,
                    campeonatos.data_inicio, 
                    campeonatos.data_fim
                FROM campeonatos
                INNER JOIN esportes
                    ON esportes.id_esporte = campeonatos.id_esporte
                INNER JOIN usuarios
                    ON usuarios.id_usuario = campeonatos.id_usuario
                WHERE 
                    id_campeonato = {escape(id_campeonato)};
            """)
            campeonato = cursor.fetchone()
            
            if not campeonato:
                return "Campeonato não encontrado", 404
            
            cursor.execute(f"""
                SELECT
                    partidas.id_partida,
                    partidas.rodada,
                    partidas.data_hora,
                    time_a.nome AS time_a_nome,
                    time_a.url_logo AS time_a_url_logo,
                    time_b.nome AS time_b_nome,
                    time_b.url_logo AS time_b_url_logo,
                    partidas.placar_time_a AS time_a_placar,
                    partidas.placar_time_b AS time_b_placar
                FROM partidas
                INNER JOIN times time_a
                    ON time_a.id_time = partidas.id_time_a
                INNER JOIN times time_b
                    ON time_b.id_time = partidas.id_time_b
                WHERE partidas.id_campeonato = {escape(id_campeonato)}
                ORDER BY partidas.data_hora ASC;
            """)
            partidas = cursor.fetchall()

            cursor.execute(f"""
                SELECT
                    times.id_time,
                    times.nome, 
                    times.url_logo,
                    COALESCE(pontuacao_time_a.total_a, 0) + COALESCE(pontuacao_time_b.total_b, 0) as pontuacao_total
                FROM times
                LEFT JOIN (
                    SELECT id_time_a, SUM(placar_time_a) as total_a
                    FROM partidas
                    WHERE id_campeonato = {escape(id_campeonato)}
                    GROUP BY id_time_a
                ) pontuacao_time_a 
                    ON times.id_time = pontuacao_time_a.id_time_a
                LEFT JOIN (
                    SELECT id_time_b, SUM(placar_time_b) as total_b
                    FROM partidas
                    WHERE id_campeonato = {escape(id_campeonato)}
                    GROUP BY id_time_b
                ) pontuacao_time_b 
                    ON times.id_time = pontuacao_time_b.id_time_b
                WHERE times.id_campeonato = {escape(id_campeonato)}
                ORDER BY pontuacao_total DESC;
            """)
            times = cursor.fetchall()

            if 'user_id' in session:
                cursor.execute(f"""
                    SELECT id_usuario, nome, email
                    FROM usuarios 
                    WHERE id_usuario = {escape(session['user_id'])};
                """)
                usuario = cursor.fetchone()
                
        return render_template('campeonato.html.jinja', 
                             campeonato=campeonato,
                             times=times,
                             partidas=partidas,
                             usuario=usuario)
    except Exception as e:
        return f"Internal Server Error: {str(e)}", 500
    finally:
        if campeonato_connection.open:
            campeonato_connection.close()

if __name__ == '__main__':
    app.run(debug=True)
