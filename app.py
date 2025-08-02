from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, Fake Tour Jerez!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
