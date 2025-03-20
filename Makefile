shell:
	python ./manage.py shell

migrations:
	python ./manage.py makemigrations

migrate:
	python ./manage.py migrate

collect_static:
	python ./manage.py collectstatic --noinput --clear -v 0

