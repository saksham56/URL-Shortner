from os import environ
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
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


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/urlshortner'
db = SQLAlchemy(app)


#Connecting database to table Contact
class URL(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(512), nullable=False)
    timestamp = db.Column(db.String(12), nullable=True)

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

@app.route('/<slug>')
def short(slug):
    try:
        url = URL.query.filter_by(slug=slug).first()
        getUserData(request.path)
        return redirect(url.url)
    except:
        getUserData(request.path)
        return render_template('pages/404.html')

# add new url to database
@app.route('/add', methods=['POST'])
def add():
    getUserData("Add Page")
    if request.method == 'POST':
        url = request.form['url']
        slug = request.form['slug']
        if url == '':
            return render_template('index.html', error=True)
        if slug == '':
            slug = url
        url = URL(url=url, slug=slug)
        db.session.add(url)
        db.session.commit()
        return 1

#check slug is already in database
@app.route('/check', methods=['POST'])
def check():
    getUserData("Check Page")
    if request.method == 'POST':
        slug = request.form['slug']
        url = URL.query.filter_by(slug=slug).first()
        if url:
            return 1
        else:
            return 0
    
    

if __name__ == '__main__':
    app.run()
