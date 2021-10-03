#!/bin/bash

chmod +x wait-for-it.sh
./wait-for-it.sh -h localhost -p 5432

createdb hoogle

python manage.py makemigrations
python manage.py migrate --noinput 
python manage.py runserver 0.0.0.0:8000
