from os import environ
from flask import Flask, redirect, render_template, request, url_for
import requests
import json
import datetime

def getUserData(route):
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    with open("users.txt", "a") as f:
        f.write(f"Page Visited: {route}\n")
        f.write(f"User Agent: {request.headers.get('User-Agent')}\n")
        f.write(f"Remote Addr: {ip}\n")
        f.write(f"DateTime: {datetime.datetime.now()}\n")
        f.write(f"\n\n\n")


app = Flask(__name__)
app.debug = True
app.port = 8000

# 404 Handling
@app.errorhandler(404)
def not_found(e):
    getUserData("404 Page")
    return render_template("pages/404.html")

# Website
@app.route('/')
def index():
    getUserData("Index Page")
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
