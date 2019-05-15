import sqlite3
from config import Config


from flask import Flask,render_template, g
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db
def init_db():
    ''' crea las tablas de la db'''
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

app = Flask (__name__)
app.config.from_object(Config)

@app.route ('/')
def index ():
    for user in query_db("SELECT * FROM usuarios WHERE username = 'admin';"):
        print(user["name"])
    return render_template("home.html")

@app.route ('/home.html')
def home ():

    return render_template("home.html")

@app.route ('/galeria.html')
def galeria ():
    return render_template("galeria.html")

if __name__ == '__main__':
    app.run(debug=True)

