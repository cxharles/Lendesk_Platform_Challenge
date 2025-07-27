from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)
DATABASE_URL = os.getenv("DATABASE_URL")

@app.route("/ping")
def ping():
    return "pong"

@app.route("/users")
def users():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT 'john', 'doe'")  # Dummy row
    result = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(result)
