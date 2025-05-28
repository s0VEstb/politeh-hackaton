from .base import BASE_DIR
from decouple import config
import os


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST'),
        'PORT': config('POSTGRES_PORT', '5432'),
        'OPTIONS': {
            'options': '-c search_path=public',
        },
        # ВАЖНО: запретить Django создавать расширения
        'POSTGIS_MANAGE_EXTENSIONS': False,
    }
    
}

GEOS_LIBRARY_PATH = None
GDAL_LIBRARY_PATH = None
import os
os.environ['PROJ_LIB'] = '/usr/share/proj'


ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS').split(',')
CORS_ALLOWED_ORIGINS =  config('CORS_ALLOWED_ORIGINS').split(',')

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 3600