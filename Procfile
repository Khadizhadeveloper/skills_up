web: python manage.py migrate && python manage.py createsuperuser --noinput || true && python manage.py test_data || true && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
