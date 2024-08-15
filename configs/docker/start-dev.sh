#!/bin/sh

pip --no-cache-dir install -r requirements.txt
flask db migrate && flask db upgrade
celery -A tasks.celery worker -Q gpt_queue --loglevel INFO &

# Start uWSGI service in the foreground
python3 wsgi.py
