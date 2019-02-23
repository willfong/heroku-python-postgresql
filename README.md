# Boilerplate: Heroku / Python / Postgresql

## Getting Started

```
git clone https://github.com/willfong/heroku-python-postgresql.git my-new-project
cd my-new-project
python3 -m venv venv
. venv/bin/activate
heroku create
heroku addons:create heroku-postgresql:hobby-dev
heroku config:get DATABASE_URL -s >> .env

```

## Creating Local Environment


## Authentication Providers

Use GitHub for authentication by creating an app here: https://github.com/settings/developers



## Python Packages

pip install Flask Flask-Dance psycopg2-binary waitress
