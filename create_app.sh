#!/bin/bash

if [ -z "$GITHUB_USERNAME" ]
then
    echo "GitHub Username Not Found"
    exit
fi

if [ -z "$GITHUB_ACCESS_TOKEN" ]
then
    echo "GitHub Access Token Not Found"
    exit
fi

if [ -z "$HEROKU_ACCESS_TOKEN" ]
then
    echo "Heroku Access Token Not Found"
    exit
fi

echo "This script will create a GitHub Repo and Heroku App from the common boilerplate"
echo "Review this code before running, since it requires your API keys"


CURL_HEROKU='curl --verbose --header "Accept: application/vnd.heroku+json;version=3"'
CURL_GITHUB="curl --silent -u ${GITHUB_USERNAME}:${GITHUB_ACCESS_TOKEN}"


echo -n "Name of app: "
read input_appname


echo -n "Checking GitHub for: ${input_appname}  "
github_name_check=`${CURL_GITHUB} https://api.github.com/repos/${GITHUB_USERNAME}/${input_appname}|grep "Not Found"`
if [ -z "$github_name_check" ] 
then
    # Not Available
    printf "\xE2\x9D\x8C\n"
    echo "Repository already exists: ${input_appname}"
    exit
else
    # Available
    printf "\xE2\x9C\x94\n"
fi


echo -n "Checking Heroku for: ${input_appname}  "
#heroku_name_check=`${CURL_HEROKU} https://api.heroku.com/apps/${input_appname}`
heroku_name_check=`curl --silent --header "Accept: application/vnd.heroku+json; version=3" https://api.heroku.com/apps/${input_appname}|grep "Couldn't find that app"`

if [ -z "$heroku_name_check" ] 
then
    # Not Available
    printf "\xE2\x9D\x8C\n"
    echo "Heroku application name not available: ${input_appname}"
    exit
else  
    # Available
    printf "\xE2\x9C\x94\n"
fi


echo "Creating GitHub Repo..."
${CURL_GITHUB} --request POST --data "{\"name\": \"${input_appname}\", \"private\": \"true\", \"auto_init\": \"false\"}" https://api.github.com/user/repos

echo "Creating Heroku App..."
curl --silent --header "Accept: application/vnd.heroku+json; version=3" --header "Authorization: Bearer ${HEROKU_ACCESS_TOKEN}" --header "Content-Type: application/json" --request POST --data "{\"name\": \"${input_appname}\",\"region\": \"us\",\"stack\": \"heroku-18\"}" https://api.heroku.com/apps


echo "Getting Boiler Plate Template..."
curl -L -o temp_boiler_plate.zip https://github.com/willfong/heroku-python-postgresql/archive/master.zip

echo "Uncompressing..."
unzip temp_boiler_plate.zip
rm -rf temp_boiler_plate.zip

echo "Creating Project Directory..."
mv heroku-python-postgresql-master $input_appname


echo "Initalizing Git..."
cd $input_appname
git init
git remote add origin git@github.com:$GITHUB_USERNAME/$input_appname.git

echo "Setting up local environment file..."
cp env-sample .env

echo "Setting up Python Environment..."
python3 -m venv venv

echo "Installing Requirements..."
. venv/bin/activate
pip install -r requirements.txt

echo "Setting up Heroku Application..."
heroku git:remote --app $input_appname

echo "Setting up Heroku Database..."
heroku addons:create heroku-postgresql:hobby-dev
heroku config:get DATABASE_URL -s >> .env

echo "Setting Session secret key..."
echo "SESSION_SECRET_KEY=`python3 -c 'import os; print(os.urandom(64).hex())'`" >> .env