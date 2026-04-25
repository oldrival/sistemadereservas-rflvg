from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = "reservas.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            servicio TEXT NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    mensaje = None
    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        servicio = request.form["servicio"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO reservas (nombre, telefono, servicio, fecha, hora) VALUES (?, ?, ?, ?, ?)",
                  (nombre, telefono, servicio, fecha, hora))
        conn.commit()
        conn.close()
        mensaje = f"¡Reserva confirmada, {nombre}! Te esperamos el {fecha} a las {hora}."

    return render_template("index.html", mensaje=mensaje)

@app.route("/admin")
def admin():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM reservas ORDER BY fecha, hora")
    reservas = c.fetchall()
    conn.close()
    return render_template("admin.html", reservas=reservas)

@app.route("/eliminar/<int:id>")
def eliminar(id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DELETE FROM reservas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5001)