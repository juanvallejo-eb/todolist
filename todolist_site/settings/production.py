from .base import *
from . import get_env_variable
import dj_database_url

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_name',
        'USER': 'db_user',
        'PASSWORD': '',
        'HOST': '',
        'PORT': 'db_port_number',
    }
}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)


SOCIAL_AUTH_EVENTBRITE_KEY = get_env_variable('SOCIAL_AUTH_EVENTBRITE_KEY')
SOCIAL_AUTH_EVENTBRITE_SECRET = get_env_variable(
    'SOCIAL_AUTH_EVENTBRITE_SECRET',
)
