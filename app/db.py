import os
import psycopg2
import click
from flask import current_app, g
from flask.cli import with_appcontext


def db_get():
    print("Initializing DB: {}".format(os.environ.get('DATABASE_URL')))
    if 'db' not in g:
        g.db = psycopg2.connect(os.environ.get('DATABASE_URL'))

    return g.db


def db_close(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def db_init():
    db = db_get()
    cur = db.cursor()
    with current_app.open_resource('schema.sql') as f:
        cur.execute(f.read().decode('utf8'))


def db_read(query, params=None, one=True):
    db = db_get()
    cur = db.cursor()
    cur.execute(query, params)
    if one:
        return cur.fetchone()
    else:
        return cur.fetchall()


def db_write(query, params=None):
    db = db_get()
    cur = db.cursor()
    cur.execute(query, params)
    db.commit()
    return True


@click.command('db-init')
@with_appcontext
def db_init_command():
    db_init()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(db_close)
    app.cli.add_command(db_init_command)
