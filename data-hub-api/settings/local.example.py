from .base import *  # noqa


ADMINS = (
    ('UKTI Digital', 'Your email'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'data-hub-api',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
        'TEST': {
            'SERIALIZE': False,
        },
    }
}


# You might want to use sqlite3 for testing in local as it's much faster.
if IN_TESTING:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/tmp/data-hub-api_test.db',
            'TEST': {
                'SERIALIZE': False,
            },
        }
    }

INSTALLED_APPS += [
    'django_extensions'
]


CDMS_ADFS_URL = ''
CDMS_BASE_URL = ''
CDMS_USERNAME = ''
CDMS_PASSWORD = ''
CDMS_COOKIE_KEY = b'RKfgWE-GYNy3mWHm5wEUZavralDzSMKDguBfyuBag8A='


LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,
    'handlers': {
        'console': {
            # logging handler that outputs log messages to terminal
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',  # message level to be written to console
        },
    },
    'loggers': {
        '': {
            # this sets root level logger to log debug and higher level
            # logs to console. All other loggers inherit settings from
            # root level logger.
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,  # this tells logger to send logging message to its parent (will send if set to True)
        },
        'django.db.backends': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False
        },
        'cmds_api': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False
        }
    },
}
