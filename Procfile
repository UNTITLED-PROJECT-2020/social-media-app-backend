web: gunicorn AppBackend.wsgi --log-file -
web2: daphne AppBackend.routing:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channel_layer -v2
chatworker: python manage.py runworker --settings=AppBackend.settings.production -v2