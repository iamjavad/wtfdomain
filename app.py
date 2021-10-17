#!/usr/bin/python3

from flask import Flask
from flask.templating import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

app.debug = True
app.run()
app.run(debug = True)


if __name__=='__main__':
    app.run()