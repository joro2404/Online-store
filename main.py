from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify, flash
import json
import sqlite3
from sqlite3 import IntegrityError

from user import User

app = Flask(__name__)
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

@app.route('/')
def home():
    return render_template('index.html')

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
        user = User.find_by_username(username)
        if not user or not user.verify_password(password):
            return jsonify({'token': None})
        token = user.generate_token()
        return jsonify({'token': token.decode('ascii')})



if __name__ == '__main__':
    app.run()
