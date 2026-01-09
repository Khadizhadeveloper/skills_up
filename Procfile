web: python manage.py migrate && (python manage.py create_superuser || echo "SUPERUSER COMMAND FAILED") && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
