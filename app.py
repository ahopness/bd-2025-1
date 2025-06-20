from flask import Flask, render_template, session
app = Flask(__name__)
app.secret_key = 'segredo'

import pymysql
from config import *
from utils import *

from account import *
from championship import *

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
            """)
            esportes = cursor.fetchall()

            usuario = None
            if 'user_id' in session:
                cursor.execute(f"""
                    SELECT id_usuario, nome, email 
                    FROM usuarios 
                    WHERE id_usuario = '{session['user_id']}';
                """)
                usuario = cursor.fetchone()

        return render_template('home.html.jinja', campeonatos=campeonatos, usuario=usuario, esportes=esportes)
    except Exception as e:
        home_connection.rollback()
        return f"Internal Server Error: {str(e)}", 500
    finally:
        if home_connection.open:
            home_connection.close()

@app.get('/campeonato/<nome>')
def dashboard_get(nome):
    usuario = None
    if 'user_id' in session:
        try:
            dashboard_connection = pymysql.connect(**DB_CONFIG)
            with dashboard_connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(f"""
                    SELECT id_usuario, nome, email 
                    FROM usuarios 
                    WHERE id_usuario = '{session['user_id']}';
                """)
                usuario = cursor.fetchone()
        except:
            pass
        finally:
            if dashboard_connection.open:
                dashboard_connection.close()
    
    return render_template('dashboard.html.jinja', titulo=nome, usuario=usuario)

if __name__ == '__main__':
    app.run(debug=True)
