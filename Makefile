install:
	poetry install

start:
	poetry run python manage.py runserver

makemigrate:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

shell:
	poetry run python manage.py shell_plus --ipython

lint:
	poetry run flake8 task_manager
	poetry run flake8 task_manager/labels
	poetry run flake8 task_manager/statuses
	poetry run flake8 task_manager/tasks
	poetry run flake8 task_manager/users

tests:
	poetry run python manage.py test

tests-cov:
	poetry run coverage run --source='.' manage.py test
	poetry run coverage xml