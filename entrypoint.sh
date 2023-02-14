#!/bin/sh

echo "INIT MIGRATIONS"
flask --app main.py db init

echo "MIGRATE"
flask --app main.py db migrate

echo "UPGRADE"
flask --app main.py db upgrade

echo "RUN APPLICATION"
gunicorn main:app -w 4 -b 0.0.0.0:5000