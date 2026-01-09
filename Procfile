web: echo "=== STARTING MIGRATIONS ===" && python manage.py migrate && echo "=== MIGRATIONS DONE ===" && echo "=== RUNNING SETUP_ADMIN ===" && python setup_admin.py && echo "=== SETUP_ADMIN DONE ===" && echo "=== STARTING GUNICORN ===" && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT

