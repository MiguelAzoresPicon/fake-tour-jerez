from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Inicializar o crear la base de datos si no existe
def init_db():
    with sqlite3.connect('reviews.db') as con:
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                comment TEXT,
                rating INTEGER CHECK(rating BETWEEN 1 AND 5),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        con.commit()

# Ruta principal: muestra y procesa el formulario y las reseñas
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Recoger datos del formulario
        name = request.form.get('name', '').strip()
        comment = request.form.get('comment', '').strip()
        try:
            rating = int(request.form.get('rating', '5'))
        except ValueError:
            rating = 5
        # Insertar en la base de datos
        with sqlite3.connect('reviews.db') as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO reviews (name, comment, rating) VALUES (?, ?, ?)",
                (name, comment, rating)
            )
            con.commit()
        return redirect('/')

    # GET: obtener las 5 últimas reseñas
    with sqlite3.connect('reviews.db') as con:
        cur = con.cursor()
        cur.execute(
            'SELECT name, comment, rating FROM reviews ORDER BY created_at DESC LIMIT 5'
        )
        reviews = cur.fetchall()

    return render_template('index.html', reviews=reviews)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
