import os, os.path
from os import environ

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'metaeditor',
        'USER': 'test',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
    'devel': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.getcwd(), 'database.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# permit running the devel sqlite database with 
#   DJANGO_DATABASE='devel' python manage.py runserver 
default_database = environ.get('DJANGO_DATABASE', 'default')
if not default_database == "default":
    DATABASES['default'] = DATABASES[default_database]

