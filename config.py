import pymysql.cursors

from app import app
app.secret_key = 'segredo'

XAMPP_DB = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'gestor_campeonatos',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

DB_CONFIG = XAMPP_DB
