import os

import django
import environ


ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('apps')

env = environ.Env()

DEBUG = False

INSTALLED_APPS = (
    'modeltranslation',
    'huey.contrib.djhuey',
    'jet',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'imagekit',
    'ckeditor',
    'import_export',
    'fcm_django',
    'drf_yasg',
    'rest_framework_swagger',
    'dj_pagination',

    'apps.users',
    'apps.news',
    'apps.indicators',
    'apps.notifications',
    'apps.crm',
    'apps.main',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'dj_pagination.middleware.PaginationMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(ROOT_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': env.db(
        'DJANGO_DEFAULT_DATABASE',
        default='postgres://user:password@127.0.0.1:5432/test_db',
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.User'

LANGUAGE_CODE = 'ru-ru'

EXTRA_LANG_INFO = {
    'ky': {
        'bidi': False,
        'code': 'ky',
        'name': 'Kyrgyz',
        'name_local': u'Кыргызча',
    },
}

LANG_INFO = django.conf.locale.LANG_INFO
LANG_INFO.update(EXTRA_LANG_INFO)
django.conf.locale.LANG_INFO = LANG_INFO

gettext = lambda s: s
LANGUAGES = (
    ('ru', gettext('Russian')),
    ('ky', gettext('Kyrgyz')),
)

# MODELTRANSLATION_TRANSLATION_FILES = (
#     'apps.news.translation',
# )

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
MODELTRANSLATION_LANGUAGES = ('ru', 'ky')

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = str(ROOT_DIR('static'))

STATICFILES_DIRS = (
    str(ROOT_DIR('staticfiles')),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_URL = '/media/'

MEDIA_ROOT = str(ROOT_DIR('media'))

ADMIN_THUMBNAIL_STYLE = {"display": "block", "width": "80px", "height": "auto"}

LOGIN_URL = 'admin:login'

JET_THEMES = [
    {
        'theme': 'default',  # theme folder name
        'color': '#2b3647',  # color of the theme's button in user menu
        'title': 'Default',   # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]

FCM_DJANGO_SETTINGS = {
    "APP_VERBOSE_NAME": "FCM CARDIO",
    "FCM_SERVER_KEY": env.str('DJANGO_FCM_SERVER_KEY'),
    "ONE_DEVICE_PER_USER": True,
    "DELETE_INACTIVE_DEVICES": True,
}

LOCALE_PATHS = (
    os.path.join(ROOT_DIR, 'locale'),
)

REDIS_URL = 'redis://localhost:6379/0'

# settings.py
HUEY = {
    'huey_class': 'huey.RedisHuey',  # Huey implementation to use.
    'name': DATABASES['default']['NAME'],  # Use db name for huey.
    'results': True,  # Store return values of tasks.
    'store_none': False,  # If a task returns None, do not save to results.
    'immediate': DEBUG,  # If DEBUG=True, run synchronously.
    'utc': False,  # Use UTC for all times internally.
    'blocking': True,  # Perform blocking pop rather than poll Redis.
    'connection': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'connection_pool': None,  # Definitely you should use pooling!
        # ... tons of other options, see redis-py for details.

        # huey-specific connection parameters.
        'read_timeout': 1,  # If not polling (blocking pop), use timeout.
        'url': None,  # Allow Redis config via a DSN.
    },
    'consumer': {
        'workers': 1,
        'worker_type': 'thread',
        'initial_delay': 0.1,  # Smallest polling interval, same as -d.
        'backoff': 1.15,  # Exponential backoff using this rate, -b.
        'max_delay': 10.0,  # Max possible polling interval, -m.
        'scheduler_interval': 1,  # Check schedule every second, -s.
        'periodic': True,  # Enable crontab feature.
        'check_worker_health': True,  # Enable worker health checks.
        'health_check_interval': 1,  # Check worker health every second.
    },
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'syslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'address': '/dev/stdout',
        }
    },
    # 'loggers': {
    #     'django.request': {
    #         'handlers': ['mail_admins'],
    #         'level': 'ERROR',
    #         'propagate': True,
    #     },
    #    'huey.consumer': {
    #         'handlers': ['syslog'],
    #         'level': 'INFO',
    #         'propagate': True,
    #    }
    # }
}
