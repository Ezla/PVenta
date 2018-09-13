from VentaAlex.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pventa',
        'USER': 'papeleria_alex',
        'PASSWORD': 'qwer1234',
        'HOST': 'localhost',
        'PORT': '3306',
        'ATOMIC_REQUESTS': True,
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = (BASE_DIR, 'static',)
STATICFILES_DIRS = (BASE_DIR + '/static', 'static',)
STATIC_ROOT = '/var/www/EnvPVenta/static'
