from .base import *
import os
from . import get_env_variable

CAPTCHA_TEST_MODE = True
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
