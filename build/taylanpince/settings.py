import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Taylan Pince', 'taylanpince@gmail.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'Canada/Eastern'

USE_I18N = True

SITE_ID = 1

MEDIA_ROOT = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'media/')
MEDIA_URL = '/media/'

SECRET_KEY = 'i_4i)=(d84poj9^$%g#h9-zk%(@4+l$nyud^m+=^k+z6@@j=wu'

CACHE_BACKEND = 'db://caches'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'core.utils.notifications.notifications',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'core.utils.notifications.NotificationMiddleware',
)

ROOT_URLCONF = 'taylanpince.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.realpath(os.path.dirname(__file__)), 'templates/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    
    'django_extensions',
    'sorl.thumbnail',
    'tagging',
    'core.utils',
    
    'blog',
)

AKISMET_API_KEY = '6162dece3c36'

GRAVATAR_URL = 'http://www.gravatar.com/avatar.php?'
AVATAR_ICON_SIZE = 48

try:
    from settings_local import *
except:
    pass

DEFAULT_AVATAR_ICON = MEDIA_URL + 'images/icon-avatar.png'
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'
