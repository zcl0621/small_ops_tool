#!/bin/bash
nginx
cd /walnut
if [ ! -f /walnut/db/db.sqlite3 ];then
    python3 manage.py makemigrations
    python3 manage.py migrate
fi
python3 manage.py runserver 0.0.0.0:8000 &
celery -A walnut worker -l info -B
