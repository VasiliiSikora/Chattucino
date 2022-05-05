from crypt import methods
from email.policy import default
import re
from flask import Flask, render_template, redirect, request, session, jsonify
import psycopg2
import bcrypt
import requests
import os
from functions import convert_unix_time, db_selector, db_inserter, cookie_get
from datetime import datetime, date

from map import location_get, static_map_get
from weather import weather_get

#convert UNIX time to YYYY-MM-DD
ts = int('1651370400')
print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d'))

#import config vars from heroku
DB_URL = os.environ.get('DATABASE_URL', 'dbname=chattucino')
SECRET_KEY = os.environ.get('SECRET_KEY', 'pretend secret key for testing')

#when want to push local db to heroku: heroku pf:push database_name_here DATABASE_URL
#heroku psql to update stuff in the heroku app

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    today = datetime.today().strftime('%Y-%m-%d')
    today_compare = datetime.strptime(today, '%Y-%m-%d').date()
    # conn = psycopg2.connect(DB_URL)
    # cur = conn.cursor()
    # cur.execute('SELECT post_id, posts.user_id, name, fav_coffee, location, flair, date, max_people FROM posts INNER JOIN users ON users.user_id = posts.user_id') #Pull post data
    # results = cur.fetchall()
    results = db_selector(DB_URL, 'SELECT post_id, posts.user_id, name, fav_coffee, location, flair, date, max_people FROM posts INNER JOIN users ON users.user_id = posts.user_id')
    posts = []
    for row in results:
        post = {
            'post_id': row[0],
            'name': row[2],
            'fav_coffee': row[3],
            'location': row[4],
            'flair': row[5],
            'date': row[6],
            'max_people': row[7]
        }
        #deal with weather
        if post['date']>today_compare:
            weather_json = weather_get(post['location'])
            weather_results = weather_json['daily']
            for row in weather_results:
                date = convert_unix_time(row['dt'])
                if str(date) == str(post['date']):
                    post['temperature'] = row['temp']['day']
                    post['weather'] = row['weather'][0]['main']
                    icon = row['weather'][0]['icon']
                    post['icon'] = f'http://openweathermap.org/img/wn/{icon}@2x.png'

        posts.append(post)

        #Check for interested/going users
        interested = db_selector(DB_URL,f"SELECT COUNT(*) FROM interested WHERE (post_id={post['post_id']} AND (going='P' OR going='Y'))")
        post['interested'] = interested[0][0]
    # conn.close()
    user_cookie = cookie_get(DB_URL)
    print(user_cookie)

    if user_cookie==None:
        return render_template('frontpage.html')

    return render_template('home.html', posts = posts, user_cookie = user_cookie, today=today_compare)

@app.route('/new_post')
def new_post():
    user_cookie = cookie_get(DB_URL)
    return render_template('new_post.html', user_cookie=user_cookie)

@app.route('/new_post_action', methods=['POST'])
def new_post_action():
    user_id = session.get('user_id')
    street_address = request.form.get('street_address')
    location = request.form.get('location')
    state = request.form.get('state')
    date = request.form.get('date')
    max_people = request.form.get('max_people')
    flair = request.form.get('flair')
    if user_id == None:
        return redirect('/')
    if user_id!=None and street_address!=None and location!=None and state!=None and date!=None and max_people!=None and flair!=None:
        db_inserter(DB_URL, 'INSERT INTO posts(user_id, street_address, location, state,date, max_people, flair) VALUES (%s, %s, %s, %s, %s, %s, %s)',[user_id, street_address, location, state,date, max_people, flair])

        return redirect('/')
    else:
        return render_template('failed.html')

@app.route('/signup')
def signup():
    user_cookie = cookie_get(DB_URL)
    if user_cookie != None:
        return redirect('/')
    return render_template('sign_up.html', user_cookie=user_cookie)

@app.route('/signup_action', methods=['POST'])
def signup_action():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    pw_confirm = request.form.get('confirm')
    fav_coffee = request.form.get('fav_coffee')
    default_beans = 0
    if password == pw_confirm and name!=None and password != None and email != None and fav_coffee != None:
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    else: 
        return render_template('failed.html')
    db_inserter(DB_URL, 'INSERT INTO users(name, password, email, fav_coffee,beans) VALUES (%s, %s, %s, %s, %s)',[name, hashed_pw, email, fav_coffee, default_beans])
    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_action', methods=['POST'])
def login_action():
    email = request.form.get('email')
    password = request.form.get('password')

    results = db_selector(DB_URL, f"SELECT * FROM users WHERE email LIKE '{email}'")
    if results != []:
        password_hash = results[0][2]
        pw_check = bcrypt.checkpw(password.encode(), password_hash.encode())
    else:
        return render_template('failed.html')        

    if results != [] and email in results[0] and pw_check:
        id = results[0][0]
        session['user_id'] = id
        print(session['user_id'])
        return redirect('/')
    else:
        return render_template('failed.html')

@app.route('/logout')
def delete_cookie():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

@app.route('/post_detail')
def more_detail():
    today = datetime.today().strftime('%Y-%m-%d')
    today_compare = datetime.strptime(today, '%Y-%m-%d').date()
    user_cookie = cookie_get(DB_URL)
    post_id=request.args.get('post_id')
    results = db_selector(DB_URL, f'SELECT post_id, posts.user_id, name, fav_coffee, location, flair, date, max_people, street_address, state FROM posts INNER JOIN users ON users.user_id = posts.user_id WHERE posts.post_id = {post_id}')

    for row in results:
        post = {
            'post_id': row[0],
            'name': row[2],
            'fav_coffee': row[3],
            'location': row[4],
            'flair': row[5],
            'date': row[6],
            'max_people': row[7],
            'street_address': row[8],
            'state': row[9]
        }

        #deal with weather
        weather_json = weather_get(f"{post['street_address']}, {post['location']}, {post['state']} Australia")
        weather_results = weather_json['daily']
        for row in weather_results:
            date = convert_unix_time(row['dt'])
            if str(date) == str(post['date']):
                post['temperature'] = row['temp']['day']
                post['weather'] = row['weather'][0]['main']
                icon = row['weather'][0]['icon']
                post['icon'] = f'http://openweathermap.org/img/wn/{icon}@2x.png'

        #Need to resolve search query by having more detailed location
        map_url = static_map_get(f"{post['street_address']}, {post['location']}, {post['state']} Australia")

        interested = db_selector(DB_URL,f"SELECT COUNT(*) FROM interested WHERE (post_id={post['post_id']} AND (going='P' OR going='Y'))")
        post['interested'] = interested[0][0]
        users_interested = db_selector(DB_URL,f"SELECT name FROM interested INNER JOIN users ON users.user_id=interested.interested_user WHERE (post_id={post['post_id']} AND (going='P' OR going='Y'));")
        print(users_interested)

    return render_template('post_detail.html', post=post, map_url=map_url, user_cookie=user_cookie, users_interested=users_interested,today=today_compare)

@app.route('/request_to_go', methods=['POST'])
def register_interest():
    user_cookie = session['user_id']
    post_id=request.form.get('post_id')
    user_check = db_selector(DB_URL,f'SELECT * FROM interested WHERE (post_id={post_id} AND interested_user = {user_cookie})')
    if user_check == []:
        pending = "P"
        db_inserter(DB_URL,'INSERT INTO interested(post_id,interested_user, going) VALUES (%s, %s, %s)',[post_id, user_cookie, pending])
    return redirect('/')

@app.route('/user')
def user_profile():
    today = datetime.today().strftime('%Y-%m-%d')
    today_compare = datetime.strptime(today, '%Y-%m-%d').date()
    user_page = request.args.get('id')
    user_id = session['user_id']
    # conn = psycopg2.connect(DB_URL)
    # cur = conn.cursor()
    # cur.execute('SELECT post_id, posts.user_id, name, fav_coffee, location, flair, date, max_people FROM posts INNER JOIN users ON users.user_id = posts.user_id') #Pull post data
    # results = cur.fetchall()
    user_details = db_selector(DB_URL, f'SELECT name, about, hometown, age FROM user_page INNER JOIN users ON user_page.user_id=users.user_id WHERE user_page.user_id={user_page}')

    for row in user_details:
        profile_info = {
            'name': row[0],
            'about': row[1],
            'hometown': row[2],
            'age': row[3]
        }

    results = db_selector(DB_URL, f'SELECT post_id, posts.user_id, name, fav_coffee, location, flair, date, max_people FROM posts INNER JOIN users ON users.user_id = posts.user_id WHERE posts.user_id={user_page}')
    posts = []
    interest_list = []
    for row in results:
        post = {
            'post_id': row[0],
            'name': row[2],
            'fav_coffee': row[3],
            'location': row[4],
            'flair': row[5],
            'date': row[6],
            'max_people': row[7]
        }
        
        #deal with weather
        if post['date']>today_compare:
            weather_json = weather_get(post['location'])
            weather_results = weather_json['daily']
            for row in weather_results:
                date = convert_unix_time(row['dt'])
                if str(date) == str(post['date']):
                    post['temperature'] = row['temp']['day']
                    post['weather'] = row['weather'][0]['main']
                    icon = row['weather'][0]['icon']
                    post['icon'] = f'http://openweathermap.org/img/wn/{icon}@2x.png'

            posts.append(post)

        #Check for interested/going users
        interested = db_selector(DB_URL,f"SELECT COUNT(*) FROM interested WHERE (post_id={post['post_id']} AND (going='P' OR going='Y'))")
        post['interested'] = interested[0][0]

        interested = db_selector(DB_URL,f"SELECT name, users.user_id FROM interested INNER JOIN users ON interested.interested_user=users.user_id WHERE (post_id={post['post_id']} AND going='P')")

        for entry in interested:
            interest = {
                'name': entry[0],
                'user_id':entry[1]
            }
            interest_list.append(interest)

    print(interest_list)

    # conn.close()
    user_cookie = cookie_get(DB_URL)

    return render_template('user_profile.html', posts = posts, user_cookie = user_cookie, today=today_compare, id=int(user_page), profile_info=profile_info, user_id=user_id)

@app.route('/test')
def test():
    return render_template('frontpage.html')

#Important for Heroku to work:
if __name__ == "__main__":
    app.run(debug=True)