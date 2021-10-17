#!/usr/bin/python3

from flask import Flask
from flask.templating import render_template
from flask_wtf import FlaskForm
from wtforms.fields.core import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

class DmainInput(FlaskForm):
    Domain = StringField("Domain", validators=[DataRequired()])
    Submit = SubmitField("submit")

app.config['SECRET_KEY'] = 'mysuper secret key'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = DmainInput()
    return render_template('index.html', form=form)

app.debug = True
app.run()
app.run(debug = True)


if __name__=='__main__':
    app.run()