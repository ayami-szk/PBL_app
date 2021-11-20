"""
import os
from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static')

app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template('contact.html')

import sqlite3
from flask import g

DATABASE = '/path/to/gatabase.db'

def get_db():
    db = getattr(g, '_databese', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_databese', None)
    if db is not None:
        db.close()

if __name__=='__main__':
    #app.run(port=os.environ['PORT'], host='0.0.0.0' )
    app.run(port='11111', host='0.0.0.0' )
"""
# oseti
import oseti

analyzer = oseti.Analyzer()
print(analyzer.analyze('私はとっても幸せ'))
print(analyzer.analyze('私はとっても不幸'))
print(analyzer.analyze('私はお腹いっぱいご飯を食べた'))
