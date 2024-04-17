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
	python3 manage.py makemessages -l en
	python3 manage.py makemessages -l ru
	python3 manage.py makemessages -l uz

compile:
	django-admin compilemessages --ignore=env

