from flask import Flask, g
import sqlite3
from flask_sqlalchemy import SQLAlchemy

# configuration
DATABASE = 'C:/Users/114/Desktop/TODOlist/backend-python-test/alayatodo.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
DATABASE_URI = 'sqlite:////Users/114/Desktop/TODOlist/backend-python-test/alayatodo.db'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = dict_factory
    return conn

#??
@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


import alayatodo.views
import alayatodo.models