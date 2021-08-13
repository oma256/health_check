from core.settings.base import *


SECRET_KEY = env.str('DJANGO_SECRET_KEY')

DEBUG = env.bool('DJANGO_DEBUG')

ALLOWED_HOSTS = ['*']

HUEY['connection']['host'] = 'redis'
