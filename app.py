#!/usr/bin/python3

import os
import whois
import socket
import requests
import nmap3
from flask import Flask
from flask_wtf import FlaskForm
from flask.templating import render_template
from wtforms.fields.core import StringField
from wtforms.fields.simple import SubmitField
from wtforms.form import Form
from wtforms.validators import DataRequired

app = Flask(__name__)

#main field
class DmainInput(FlaskForm):
    Domain = StringField("Enter Domain name or IP address:", validators=[DataRequired()])
    Submit = SubmitField("submit")

app.config['SECRET_KEY'] = 'mysuper secret key'

@app.route('/', methods=['GET', 'POST'])
def index():
    Domain = None
    ip = None
    emails = None
    name_server = None
    registrar = None
    creation_date =None
    expiration_date = None
    country = None
    city = None
    timezone = None
    updated_date =None
    map_link = None
    lat = None
    lon = None

    form = DmainInput()
    if form.validate_on_submit():
        Domain = form.Domain.data
        form.Domain.data = ''
        
        #ip of host
        ip = socket.gethostbyname(str(Domain))
        
        #email information
        emails = whois.whois(str(Domain))["emails"]
        emails = str(emails).replace("[", "").replace("]", "")
        
        #name servers
        name_server = whois.whois(str(Domain))["name_servers"]
        name_server = str(name_server).replace("[", "").replace("]", "")

        #registrar
        registrar = whois.whois(str(Domain))["registrar"]
        registrar = str(registrar).replace("[", "").replace("]", "")

        #creation_date
        creation_date = whois.whois(str(Domain))["creation_date"]
        creation_date = str(creation_date)

        #ip to Location-"http://ip-api.com/json/{query}"
        r = requests.get(f"http://ip-api.com/json/{ip}")
        jsn = r.json()
        country = jsn["country"]
        city = jsn["city"]
        timezone = jsn["timezone"]

        lat = jsn["lat"]
        lon = jsn["lon"]
        map_link = f"https://www.latlong.net/c/?lat={lat}&long={lon}"

        #updated_date
        updated_date = whois.whois(str(Domain))["updated_date"]
        updated_date = str(updated_date)
        
    return render_template('index.html',
    Domain = Domain,
    ip = ip,
    form=form,
    emails = emails,
    name_server = name_server,
    registrar = registrar,
    creation_date = creation_date,
    country = country,
    city = city,
    timezone = timezone,
    updated_date = updated_date,
    map_link = map_link,
    lat = lat,
    lon = lon
    )

#port scanner class
class PortField(FlaskForm):
    Domain = StringField("Domain or IP:", validators=[DataRequired()])
    Submit = SubmitField("start scan")

#PORT SCANNER
@app.route('/portscanner', methods=['GET', 'POST'])
def portscanner():
    Domain = None
    ports = None
    ip_addr = None
    
    form = PortField()
    if form.validate_on_submit():
        Domain = form.Domain.data
        form.Domain.data = ''
        #start port scanner
        ports = nmap3.Nmap().scan_top_ports(Domain)
        ip_addr = socket.gethostbyname(Domain)
    return render_template('port_scanner.html',
    form = form,
    Domain = Domain,
    ports = ports,
    ip_addr = ip_addr
    )

#Donation
@app.route('/donation')
def donation():
    return render_template('donation.html')

#API
@app.route('/API')
def api():
    return render_template('api.html')

@app.route('/api/ip/<domain>', methods=['GET', 'POST'])
def host_ip(domain):
    ip = socket.gethostbyname(domain)
    return {"IP": ip}
@app.route('/api/whois/<Domain>', methods=['GET', 'POST'])
def host_whois(Domain):
    #ip of host
    ip = socket.gethostbyname(str(Domain))
        
    #email information
    emails = whois.whois(str(Domain))["emails"]
    emails = str(emails).replace("[", "").replace("]", "")
        
    #name servers
    name_server = whois.whois(str(Domain))["name_servers"]
    name_server = str(name_server).replace("[", "").replace("]", "")

    #registrar
    registrar = whois.whois(str(Domain))["registrar"]
    registrar = str(registrar).replace("[", "").replace("]", "")

    #creation_date
    creation_date = whois.whois(str(Domain))["creation_date"]
    creation_date = str(creation_date)

    #ip to Location-"http://ip-api.com/json/{query}"
    r = requests.get(f"http://ip-api.com/json/{ip}")
    jsn = r.json()
    country = jsn["country"]
    city = jsn["city"]
    timezone = jsn["timezone"]

    #updated_date
    updated_date = whois.whois(str(Domain))["updated_date"]
    updated_date = str(updated_date)
    return {"ip":ip,
    "emails":emails,
    "name_server":name_server,
    "registerer":registrar,
    "creation_date":creation_date,
    "country":country,
    "time zone":timezone}

@app.route('/api/lat_lon/<ip>')
def lat_lon(ip):
    r = requests.get(f"http://ip-api.com/json/{ip}")
    jsn = r.json()

    Latitude = jsn["lat"]
    Longitude = jsn["lon"]
    
    return {"Latitude":Latitude,
    "Longitude":Longitude}


app.debug = True
app.run()
app.run(debug = True)


if __name__=='__main__':
    app.run()
