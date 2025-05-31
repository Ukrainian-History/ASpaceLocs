import secrets
from flask import Flask, render_template, sessions

# see https://flask.palletsprojects.com/en/stable/quickstart/#sessions for sessions info

app = Flask(__name__)
app.secret_key = secrets.token_hex()

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/locations/<int:locid>')
def get_location(locid):
    return f'[:GET] /locations/{locid}'

@app.route("/<name>")
def welcome(name):
    return render_template("welcome.html", name=name)

if __name__ == '__main__':
    app.run(debug=True)
