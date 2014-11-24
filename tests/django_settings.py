from os import path

BASE_DIR = path.dirname(__file__)

LANGUAGE_CODE = 'en'
SECRET_KEY = 'ji2r2iGkZqJVbWDhXrgDKDR2qG#mmtvBZXPXDugA4H)KFLwLHy'
SITE_ID = 1

SOUTH_TESTS_MIGRATE = True
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--nologcapture']

MEDIA_ROOT = '/tmp/cmsplugin-articles/'
ROOT_URLCONF = 'urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sites',
    'django_nose',
    'djangocms_text_ckeditor',
    'cms',
    'menus',
    'mptt',
    'south',
    'cmsplugin_articles',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.core.context_processors.request',
]

TEMPLATE_DIRS = [
    path.join(BASE_DIR, 'templates'),
]

CMS_TEMPLATES = [
    ('dummy.html', 'Dummy'),
]
