import psycopg2
from flask import session
from datetime import datetime

def db_selector(dbname, query):
    conn = psycopg2.connect(dbname)
    cur = conn.cursor() 
    cur.execute(query)
    results = cur.fetchall()
    conn.close()
    return results

def db_updater(dbname, query):
    conn = psycopg2.connect(dbname)
    cur = conn.cursor() 
    cur.execute(query)
    conn.commit()
    conn.close()
    return 

def db_inserter(dbname, query, values):
    conn = psycopg2.connect(dbname)
    cur = conn.cursor() 
    cur.execute(query,values)
    conn.commit()
    conn.close()
    return 

def cookie_get(dbname):
    conn = psycopg2.connect(dbname)
    cur = conn.cursor()
    user_id = session.get('user_id')
    user_cookie = None
    if user_id != None:
        cur.execute(f'SELECT name FROM users WHERE user_id = {user_id}')
        results = cur.fetchall()
        user_cookie = results[0][0]
    conn.close()
    return user_cookie


def convert_unix_time(unix):
    ts = int(unix)
    YYYYMMDD = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
    return YYYYMMDD