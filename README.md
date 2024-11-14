## Available **make** commands
* **make runserver**
* **make migrations**
* **make migrate**
* **make test**
* **make celery**

### Management command
* **make fetch_currencies** - For fetching currencies, its basically one time command.


## Steps to run
Before running **runserver, celery, fetch_currencies** you need to export **BEACON_API_KEY** in terminal
export BEACON_API_KEY=*************

### In a new terminal
* pip install -r requirements.txt
* docker-compose up -d

### In another terminal

* make migrate
* export BEACON_API_KEY=*************
* make run

### In another terminal

* export BEACON_API_KEY=*************
* make fetch_currencies
* make celery

### In another terminal
* make test

## Tests and Coverage
I wrote overall 17 tests and code coverage percentage is 98% .
Run following commands to see report.
* coverage run manage.py test
* coverage report


## Endpoints

### Currency
http://127.0.0.1:8000/api/currency/
http://127.0.0.1:8000/api/currency/?ordering=code
http://127.0.0.1:8000/api/currency/?ordering=-code

### Exchange Rate
http://127.0.0.1:8000/api/currency/ABC/USD/

## Admin
Run `python manage.py createsuperuser` to create a user
http://127.0.0.1:8000/admin/

I am using `celery and celery beat` to fetch exchange rate from `https://currencybeacon.com/api-documentation`.
From admin, you can create a scheduled task.
http://127.0.0.1:8000/admin/django_celery_beat/periodictask/add/
