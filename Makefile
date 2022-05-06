migrations:
	docker-compose run --rm web python manage.py makemigrations

migrate:
	docker-compose run --rm web python manage.py migrate

admin:
	docker-compose run --rm web python manage.py createsuperuser