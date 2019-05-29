# Boilerplate: Heroku / Python / Postgresql

This is a simple, opinionated, framework for quicking turning a concept in your head onto something you can see. This project was started to help make kickstarting new ideas much easier. This is still a work in progress, rushed out to meet other deadlines. As such, comments and suggestions are very much welcomed. 

## Getting Started

To get started with this boilerplate, you will need to perform the following actions:


### Prerequisites

- Heroku CLI Installed and Logged In: <https://devcenter.heroku.com/articles/heroku-cli>
- Python 3 with venv module: <https://docs.python.org/3/library/venv.html>

### Initial Setup

```shell
git clone https://github.com/willfong/heroku-python-postgresql.git my-new-project
cd my-new-project
python3 -m venv venv
. venv/bin/activate
pip install -r requirements
heroku create
heroku addons:create heroku-postgresql:hobby-dev
heroku config:get DATABASE_URL -s >> .env
```

Generally, you will only need to run these commands once.

### Set Up Database Schema

```shell
heroku pg:psql -f app/schema.sql
```

You can run this as many times as you need

### Set Up GitHub Authentication

Use GitHub for authentication by creating an app here: <https://github.com/settings/developers>

Set up two applications, one for production and one for staging. Heroku will use the Production account, and your local development will use the staging account. This is because GitHub OAuth has an authorization callback, which redirects to only one address. Production redirects to Heroku, and Staging will redirect to localhost.

Once you set up the application, you need to provide this to your local environment and Heroku:

```shell
echo "GITHUB_CLIENT_ID=123...xyz" >> .env
echo "GITHUB_CLIENT_SECRET=abc...890" >> .env
heroku config:set GITHUB_CLIENT_ID=123...xyz
heroku config:set GITHUB_CLIENT_SECRET=abc...890
```

Replace `123...xyz` and `abc...890` with your appropriate keys. Duh...

### Local Development Settings

We want to make a few configuration changes to our local development environment to make programming easier:

- Flask Debug
- OAuth2 HTTPS Security - OAUTHLIB_INSECURE_TRANSPORT=1
- Print Log - PYTHONUNBUFFERED=True

### Start It Up

```shell
heroku local
```

Now you should be able to visit: <http://localhost:5000>

We can push to Heroku:

```shell
git add .
git commit -m "Initial Test"
git push heroku master
```

You should be good to go from here.

## How It Works

### Adding New Routes


### Making Database Queries

There are helper functions in `db.py` called `read()` and `write()`. The first argument is the actual SQL query, the second is optional and is a list of parameters to pass.

```python
query = "INSERT INTO users (name, language) VALUES (%s, %s)"
params = ['willfong', 'python']
db.write(query, params)

query = "SELECT id, name FROM users WHERE active = 1 AND language = %s"
params = ['Python']
users = db.read(query, params)

for user in users:
    print("Name: {} (ID: {})".format(user["name"], user["id"]))
```

## Python Packages

```shell
pip install Flask Flask-Dance psycopg2-binary waitress
```

These are the packages you need. Install them with the command line above, or with `pip install -r requirements.txt`.

As usual, be careful when you install packages from PyPI. Verify the package names from the official documentation to be safe.

<https://incolumitas.com/2016/06/08/typosquatting-package-managers/ >

## Reference Documents

This project was created from the following references:

- <http://flask.pocoo.org/docs/1.0/tutorial/>
- <https://devcenter.heroku.com/articles/getting-started-with-python>
- <http://initd.org/psycopg/docs/usage.html#passing-parameters-to-sql-queries>
- <https://github.com/singingwolfboy/flask-dance-github>
