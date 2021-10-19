#!/usr/bin/python3

from os import name
import socket
import whois
from flask import Flask
from flask.templating import render_template
from flask_wtf import FlaskForm
from wtforms.fields.core import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

class DmainInput(FlaskForm):
    Domain = StringField("Enter Domain name:", validators=[DataRequired()])
    Submit = SubmitField("submit")

app.config['SECRET_KEY'] = 'mysuper secret key'

@app.route('/', methods=['GET', 'POST'])
def index():
    Domain = None
    ip = None
    emails = None
    name_server = None
    form = DmainInput()
    if form.validate_on_submit():
        Domain = form.Domain.data
        form.Domain.data = ''
        ip = socket.gethostbyname(str(Domain))
        emails = whois.whois(str(Domain))["emails"]
        emails = str(emails).replace("[", "").replace("]", "")
        name_server = whois.whois(str(Domain))["name_servers"]
        name_server = str(name_server).replace("[", "").replace("]", "")
    return render_template('index.html',
    Domain = Domain,
    ip = ip,
    form=form,
    emails = emails,
    name_server = name_server
    )

app.debug = True
app.run()
app.run(debug = True)


if __name__=='__main__':
    app.run()