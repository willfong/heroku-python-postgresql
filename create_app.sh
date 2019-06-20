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


echo "This script will create a GitHub Repo and Heroku App from the common boilerplate"
echo "Review this code before running, since it requires your API keys"


CURL_HEROKU="curl --silent -H \"Accept: application/vnd.heroku+json; version=3\""
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
heroku_name_check=`${CURL_HEROKU} https://api.heroku.com/apps/${input_appname}`
echo "${heroku_name_check}"

if [ -z "$heroku_name_check" ] 
then
    # Not Available
    printf "\xE2\x9D\x8C\n"
    echo "Heroku application name not available: ${input_appname}"
    echo ${CURL_HEROKU} https://api.heroku.com/apps/${input_appname}
    exit
else  
    # Available
    printf "\xE2\x9C\x94\n"
fi


echo "Creating GitHub Repo... "
#${CURL_GITHUB} --request POST --data "{\"name\": \"${input_appname}\", \"private\": \"true\", \"auto_init\": \"false\"}" -X POST https://api.github.com/user/repos

