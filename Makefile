SERVICE_SRC_DIR=.

run:
	PYTHONPATH=$(SERVICE_SRC_DIR) python manage.py runserver

test:
	PYTHONPATH=$(SERVICE_SRC_DIR) python manage.py test --settings=currency_exchange.settings_test

migrations:
	PYTHONPATH=$(SERVICE_SRC_DIR) python manage.py makemigrations

migrate:
	PYTHONPATH=$(SERVICE_SRC_DIR) python manage.py migrate

celery:
	PYTHONPATH=$(SERVICE_SRC_DIR) celery -A currency_exchange worker --loglevel=info & \
	PYTHONPATH=$(SERVICE_SRC_DIR) celery -A currency_exchange beat -l info

fetch_currencies:
	PYTHONPATH=$(SERVICE_SRC_DIR) python manage.py fetch_currencies
