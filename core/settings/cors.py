import os
from decouple import config


CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', 'False') == 'True'
CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_CREDENTIALS', 'False') == 'True'
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', 'False') == 'True'


