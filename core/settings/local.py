from core.settings.base import *


SECRET_KEY = env.str('DJANGO_SECRET_KEY', default='not secret)')

DEBUG = env.bool('DJANGO_DEBUG', default=True)

ALLOWED_HOSTS = ['*']
