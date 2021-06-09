import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '#rc20^70q7uc1$6)f#a!q_1=(h0137i1%)n+0%ci*0&liup@bk'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # Formato para numeros
    'rest_framework',
    'Apps.Producto',
    'Apps.Venta',
    'Apps.Perfil',
    'Apps.Estadistica',
    'Apps.Varios',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'Apps.Venta.middleware.ValidarCuenta',
]

ROOT_URLCONF = 'VentaAlex.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Apps.Venta.context_processors.menu',
            ],
        },
    },
]

WSGI_APPLICATION = 'VentaAlex.wsgi.application'

LANGUAGE_CODE = 'es-MX'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_PROFILE_MODULE = 'Perfil.UserProfile'
# AUTH_USER_MODEL = 'Perfil.User'

MEDIA_ROOT = os.path.join(BASE_DIR, '../../media')
MEDIA_URL = '/media/'
