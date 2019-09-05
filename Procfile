release: python manage.py migrate --setting=todolist_site.settings.production
web: gunicorn todolist_site.wsgi --log-file -