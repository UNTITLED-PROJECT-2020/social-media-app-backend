web: daphne AppBackend.asgi:application --port $PORT --bind 0.0.0.0 -v2
web2: gunicorn AppBackend.wsgi --log-file -
worker: python manage.py runworker channel_layer -v2
chatworker: python manage.py runworker --settings=AppBackend.settings.production -v2