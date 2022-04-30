import psycopg2
from flask import session

def db_selector(dbname, query):
    conn = psycopg2.connect(dbname)
    cur = conn.cursor() 
    print(query)
    cur.execute(query)
    results = cur.fetchall()
    conn.close()
    return results

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