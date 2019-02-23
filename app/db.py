import os
import psycopg2
import psycopg2.extras
from flask import g


def db_get():
    if 'db' not in g:
        print("Initializing DB: {}".format(os.environ.get('DATABASE_URL')))
        g.db = psycopg2.connect(os.environ.get('DATABASE_URL'))
    return g.db


def db_close(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def read(query, params=None, one=True):
    db = db_get()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query, params)
    if one:
        return cur.fetchone()
    else:
        return cur.fetchall()


def write(query, params=None):
    db = db_get()
    cur = db.cursor()
    cur.execute(query, params)
    db.commit()
    return True
