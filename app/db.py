import os
import psycopg2
import psycopg2.extras
from flask import g


def db_get():
    if "db" not in g:
        print("Initializing DB: {}".format(os.environ.get("DATABASE_URL")))
        g.db = psycopg2.connect(os.environ.get("DATABASE_URL"))
    return g.db


def db_close(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def read(query, params=None, one=False):
    db = db_get()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # TODO: Need to add better error handling
    try:
        cur.execute(query, params)
    except psycopg2.Error as e:
        print("Database error: {}\n{}".format(query, e))
        return False
    if one:
        return cur.fetchone()
    else:
        return cur.fetchall()


def write(query, params=None, returning=False):
    db = db_get()
    cur = db.cursor()
    # TODO: Need to add better error handling
    try:
        cur.execute(query, params)
        db.commit()
    except psycopg2.Error as e:
        print("Database error: {}\n{}".format(query, e))
        return False
    if returning:
        return cur.fetchone()
    else:
        return True
