from VentaAlex.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'prueba',
        'USER': 'root',
        'PASSWORD': 'qwe123',
        'HOST': 'localhost',
        'PORT': '3306',
        'ATOMIC_REQUESTS': True,
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = (BASE_DIR, 'static',)
