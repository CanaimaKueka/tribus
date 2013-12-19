DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tribus',
        'USER': 'tribus',
        'PASSWORD': 'tribus',
        'HOST': 'localhost',
        'PORT': '',
    }
 }

INSTALLED_APPS = (
	'south',
    'tribus.testing',
)