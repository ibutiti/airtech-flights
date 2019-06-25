release: python manage.py migrate --noinput
web: gunicorn configuration.wsgi:application --workers 4 --log-level info --log-file -
scheduler: python manage.py start_scheduler
worker: python manage.py rqworker default
