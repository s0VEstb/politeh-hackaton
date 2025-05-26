import os
from decouple import config


CORS_ORIGIN_ALLOW_ALL = config('CORS_ORIGIN_ALLOW_ALL', 'False') == 'True'
CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_CREDENTIALS', 'False') == 'True'
CORS_ALLOW_HEADERS = config('CORS_ALLOW_HEADERS', '*')
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', 'False') == 'True'


