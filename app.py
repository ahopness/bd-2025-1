from flask import Flask, render_template, request
app = Flask(__name__)

import pymysql
from config import *

@app.get('/')
def home_get():
    return render_template('index.html')

@app.post('/')
def home_post():
    sql_script = request.form.get('sqlscript', '')
    if not sql_script:
        return render_template('index.html', 
                             error="você não inseriu nada!",
                             sql_script=sql_script)
    
    try:
        connection = pymysql.connect(**DB_CONFIG)
    except Exception as e:
        return render_template('index.html', 
                             error=f"Erro ao conectar com o banco de dados:\n{e}",
                             sql_script=sql_script)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_script)
            
            results = cursor.fetchall()
            connection.commit()
            affected_rows = cursor.rowcount
            return render_template('index.html', 
                                    results=str(results) + 
                                    f" Query executado com sucesso. {affected_rows} entidade(s) afetadas.",
                                    sql_script=sql_script)
                                     
    except Exception as e:
        connection.rollback()
        return render_template('index.html', 
                             error=f"SQL Error: {str(e)}",
                             sql_script=sql_script)
    finally:
        connection.close()

if __name__ == '__main__':
    app.run()
