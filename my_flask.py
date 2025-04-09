# use this file to run the python flask
# in terminal run python my_flask.py
# in browser copy and paste this: http://127.0.0.1:5000
# have to make sure flask is installed (pip install flask)

from flask import Flask, render_template, redirect, url_for
import subprocess
import sqlite3 # included in standard python distribution
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    con = sqlite3.connect("pacman_score.db", isolation_level=None)
    cur = con.cursor()

    cur.execute(f'DROP TABLE IF EXISTS Leaderboard;')
    con.commit()

    cur.execute(f'CREATE TABLE Leaderboard AS SELECT * FROM Scoreboard ORDER BY total_score DESC;')
    con.commit()

    cur.execute(f'SELECT * FROM Leaderboard LIMIT "3";')
    data = cur.fetchall()

    # Column names
    columns = ["player", "score"]

    # Format data as a list of dictionaries
    formatted_data = [dict(zip(columns, row)) for row in data]

    return render_template("index.html", leaderboard_info=formatted_data)

@app.route("/play")
def play():
    # Launch the Pac-Man game as a separate process
    subprocess.Popen(["python", "test.py"])
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)



