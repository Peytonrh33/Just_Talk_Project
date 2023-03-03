from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.topics import Topic
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import requests
from random import randint
from flask import jsonify



# ===================================================Render About Page
@app.route('/')
def home_page():
    return render_template('home_page.html')

# ===================================================register/login render/action

@app.route('/login/register')
def login_register():
    url = "https://random-username-generate.p.rapidapi.com/"
    querystring = {"locale":"en_US","minAge":"18","maxAge":"50","domain":"ugener.com"}
    headers = {
        "X-RapidAPI-Key": "099f5ec61cmshe5c03ee11aafae3p1a91aajsna4c095222001",
        "X-RapidAPI-Host": "random-username-generate.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print("===================================================",jsonify(response.text), response.ok)
    
    x = response.json()
    print(x)
    print(x['items']['username'])
    random_username = x["items"]["username"]
    return render_template('register_login.html', random_username = random_username)

@app.route('/user/register', methods=['POST'])
def register_user():
    if not User.validate_register(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        "password": pw_hash
    }
    # ==========a insert pulls the id of the user created and the user_id is the id
    user_id = User.save(data)

    session['user_id'] = user_id

    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user_logging_in = User.get_user_email(data)

    # if email not found
    if not user_logging_in:
        flash("Invalid Email/Password")
        return redirect('/login/register')

    # now check password
    if not bcrypt.check_password_hash(user_logging_in.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/login/register')

    #else: if the user puts both in correctly 
    session['user_id'] = user_logging_in.id
    return redirect('/dashboard')
# # ===================================================dashboard render/action

@app.route('/dashboard')
def user_page():
    if "user_id" in session:
        data = {
            'id': session['user_id']
        }
        logged_in_user = User.get_user_id(data)
    else:
        logged_in_user = None
    all_topics = Topic.all_topics()
    return render_template('user_page.html', logged_in_user = logged_in_user, all_topics = all_topics)

# ==================================================Logout Action

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

