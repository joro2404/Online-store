from functools import wraps
from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify, flash, session
import json
import sqlite3
from sqlite3 import IntegrityError
from datetime import date


from user import User
from advertisement import Advertisement

app = Flask(__name__)
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        if not token or not User.verify_token(token):
            return redirect('/login')
        return func(*args, **kwargs)
    
    return wrapper


@app.route('/')
def home():
    if session.get('username') :
        session.pop('username', None)
    return redirect('/ads')


@app.route('/ads')
def ads():
    current_user = User.find_by_username(session.get('username'))
    return render_template('ads.html', advertisements=Advertisement.all(), current_user=current_user, session=session)

@app.route('/create_ad', methods=['GET', 'POST'])
@require_login
def create_ad():
    if request.method == 'GET':
        return render_template('create_ad.html')
    elif request.method == 'POST':
        seller = User.find_by_username(session.get('username'))
        values = (
            None,
            seller.id,
            None,
            request.form['name'],
            request.form['description'],
            request.form['price'],
            date.today(),
            1
        )
        Advertisement(*values).create()
        return redirect('/ads')

@app.route('/ads/<int:id>/buy')
@require_login
def buy_ad(id):
    buyer = User.find_by_username(session.get('username'))
    ad = Advertisement.find(id)
    ad.buy(buyer.id)
    return redirect(url_for('ads'))


@app.route('/my_ads')
@require_login
def my_ads():
    seller = User.find_by_username(session.get('username'))
    # print(seller.id)
    return render_template('my_ads.html', ads=Advertisement.get_by_seller_id(seller.id))

@app.route('/my_sold_ads')
@require_login
def my_sold_ads():
    seller = User.find_by_username(session.get('username'))
    ads = Advertisement.get_by_seller_id(seller.id)
    return render_template('my_sold_ads.html', ads=ads)


@app.route('/my_ads/<int:id>/edit', methods=['GET', 'POST'])
def edit_ad(id):
    ad = Advertisement.find(id)
    if request.method == 'GET':
        return render_template('edit_ad.html',ad=ad)
    elif request.method == 'POST':
        ad.name = request.form['name']
        ad.description = request.form['description']
        ad.price = request.form['price']
        ad.save()
        return redirect(url_for('my_ads'))

@app.route('/my_ads/<int:id>/delete', methods=['GET', 'POST'])
def delete_ad(id):
    ad = Advertisement.find(id)
    ad.delete()        

    return redirect('/my_ads')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        values = (
            None,
            request.form['username'],
            User.hash_password(request.form['password']),
            request.form['email'],
            request.form['number'],
            request.form['address']
        )
        try:
            User(*values).create()
            return redirect('/login')
        except sqlite3.IntegrityError as e:
            flash("Email or username are already in use!")
            return(redirect('/register'))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = json.loads(request.data.decode('ascii'))
        username = data['username']
        password = data['password']
        session['username'] = username
        user = User.find_by_username(username)
        if not user or not user.verify_password(password):
            return jsonify({'token': None})
        token = user.generate_token()
        return jsonify({'token': token.decode('ascii')})



if __name__ == '__main__':
    app.run()
