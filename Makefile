mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

freeze:
	pip freeze >requirements.txt

restart_service:
	systemctl restart warehouse.service

restart_nginx:
	systemctl restart nginx.service

createsuperuser:
	python3 manage.py createsuperuser

makemessages:
	python3 manage.py makemessages -l en --ignore venv
	python3 manage.py makemessages -l ru --ignore venv
	python3 manage.py makemessages -l uz --ignore venv

compile:
	django-admin compilemessages --ignore=venv

