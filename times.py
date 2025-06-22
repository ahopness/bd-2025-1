from flask import request, session, redirect, url_for, jsonify
from markupsafe import escape

from app import app

import pymysql
from config import *

@app.post('/time_criar')
def time_criar():
    pass