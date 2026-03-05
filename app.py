from flask import Flask, render_template, redirect, flash
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "secretkey123"

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

@app.route('/')
def index():
    db = get_db_connection()
    cursor = db.cursor()                            
    cursor.execute("SELECT * FROM slots")
    slots = cursor.fetchall()
    return render_template("index.html", slots=slots)


@app.route('/book/<int:id>')
def book(id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT status FROM slots WHERE id=%s", (id,))
    status = cursor.fetchone()

    if status and status[0] == "Available":
        cursor.execute("UPDATE slots SET status='Booked' WHERE id=%s", (id,))
        db.commit()
        flash("Slot booked successfully!")
    else:
        flash("Slot already booked.")

    return redirect('/')

@app.route('/cancel/<int:id>')
def cancel(id):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("UPDATE slots SET status='Available' WHERE id=%s", (id,))
    db.commit()

    flash("Slot cancelled successfully!")

    return redirect('/')

@app.route('/booked')
def booked():
    db = get_db_connection()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM slots WHERE status='Booked'")
    slots = cursor.fetchall()

    return render_template("booked_slots.html", slots=slots)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)