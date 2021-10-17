#!/usr/bin/python3

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "hi, this is my start!"

if __name__=="__main__":
    app.run()