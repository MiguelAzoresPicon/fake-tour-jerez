from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('reviews.db') as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            comment TEXT
        )''')
        con.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        name = request.form['name']
        comment = request.form['comment']
        with sqlite3.connect('reviews.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO reviews (name, comment) VALUES (?, ?)", (name, comment))
            con.commit()
        return redirect('/gracias')
    return render_template('review.html')

@app.route('/gracias')
def gracias():
    return render_template('gracias.html')

@app.route('/ver')
def ver():
    with sqlite3.connect('reviews.db') as con:
        cur = con.cursor()
        cur.execute("SELECT name, comment FROM reviews")
        reviews = cur.fetchall()
    return render_template('ver.html', reviews=reviews)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
