# use this file to run the python flask
# in terminal run python my_flask.py
# in browser copy and paste this: http://127.0.0.1:5000
# have to make sure flask is installed (pip install flask)

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


