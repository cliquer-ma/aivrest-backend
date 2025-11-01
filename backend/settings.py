from pathlib import Path
import os
import dotenv

dotenv.load_dotenv()


BASE_DIR                            = Path(__file__).resolve().parent.parent
SECRET_KEY                          = os.getenv('DJANGO_SECRET_KEY')
ROOT_URLCONF                        = 'backend.urls'
X_FRAME_OPTIONS                     = 'SAMEORIGIN'
SECURE_REFERRER_POLICY              = "strict-origin-when-cross-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY   = "same-origin-allow-popups"
ALLOWED_HOSTS                       = ['*']
CORS_ALLOW_ALL_ORIGINS              = True
CORS_ALLOW_CREDENTIALS              = True

WSGI_APPLICATION                    = 'backend.wsgi.application'
ASGI_APPLICATION                    = 'backend.asgi.application'

TIME_ZONE                           = 'Africa/Casablanca'

USE_I18N                            = True
USE_L10N                            = True
USE_TZ                              = True

# LANGUAGES_CODES                     = ['en', 'fr']
LANGUAGES                           = [('en', 'English'), ('fr', 'French'),]
LANGUAGE_CODE                       = 'fr'

# AUTH_USER_MODEL                     = 'users.User'

EMAIL_BACKEND                       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST                          = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER                     = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD                 = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT                          = os.getenv('EMAIL_PORT')
DEFAULT_FROM_EMAIL                  = ''
EMAIL_USE_TLS                       = True
# EMAIL_USE_SSL                     = False

CELERY_BROKER_NAME                  = os.getenv('CELERY_BROKER_NAME')
CELERY_BROKER_PASSWORD              = os.getenv('CELERY_BROKER_PASSWORD')
CELERY_BROKER_PORT                  = os.getenv('CELERY_BROKER_PORT')
CELERY_BROKER_URL                   = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND               = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT               = ['application/json']
CELERY_TASK_SERIALIZER              = 'json'
CELERY_RESULT_SERIALIZER            = 'json'
CELERY_CACHE_BACKEND                = 'django-cache'
CELERY_ENABLE_UTC                   = True

DATABASE_ENGINE                     = 'django.db.backends.postgresql'
DATABASE_NAME                       = os.getenv('DATABASE_NAME')
DATABASE_USER                       = os.getenv('DATABASE_USER')
DATABASE_PASSWORD                   = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST                       = os.getenv('DATABASE_HOST')
DATABASE_PORT                       = os.getenv('DATABASE_PORT')

JWT_SECRET_KEY                      = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM                       = "HS256"

FERNET_SECRET_KEY                   = os.getenv('FERNET_SECRET_KEY')
TOKEN_EXPIRATION_TIME               = 60 * 60 * 24  # 24 hours

STRIPE_SECRET_KEY                   = os.getenv('STRIPE_SECRET_KEY')

GEMINI_API_KEY                      = "AIzaSyDwoat3aP6q04-gmmantNzrr6WwHlxbplY"

STATIC_URL                          = '/static/'
STATICFILES_DIRS                    = [os.path.join(BASE_DIR, 'static_in_env')]
STATIC_ROOT                         = os.path.join(BASE_DIR, 'static_root')

TEMPLATE_BACKEND                    = 'django.template.backends.django.DjangoTemplates'
TEMPLATE_DIRS                       = [os.path.join(BASE_DIR, 'templates')]
TEMPLATE_APP_DIRS                   = True
TEMPLATE_OPTIONS                    = {
    'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages'
    ],
}

DATABASES                           = {'default': {
    'ENGINE'    : DATABASE_ENGINE,
    'NAME'      : DATABASE_NAME,
    'USER'      : DATABASE_USER,
    'PASSWORD'  : DATABASE_PASSWORD,
    'HOST'      : DATABASE_HOST,
    'PORT'      : DATABASE_PORT
}}

TEMPLATES                           = [{
    'BACKEND'   : TEMPLATE_BACKEND,
    'DIRS'      : TEMPLATE_DIRS,
    'APP_DIRS'  : TEMPLATE_APP_DIRS,
    'OPTIONS'   : TEMPLATE_OPTIONS,
}]

INSTALLED_APPS                      = [
    "daphne",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'django_extensions',

    'core.apps.CoreConfig',
    'agents.apps.AgentsConfig',
    'programs.apps.ProgramsConfig',
    'posts.apps.PostsConfig',
    'competitions.apps.CompetitionsConfig',
    'livechat.apps.LivechatConfig'
]

MIDDLEWARE                          = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'core.middleware.IpAddressMiddleware',
    'core.middleware.UserAgentMiddleware',
    'core.middleware.NoCacheMiddleware',
]


CHANNEL_LAYERS                      = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [CELERY_BROKER_URL],
        },
    },
}

# settings.py
CLOUDINARY_CLOUD_NAME = 'dfibistkg'
CLOUDINARY_API_KEY = '559796284768587'
CLOUDINARY_API_SECRET = "q2KZ6WszNtFvmu7Oewb6qM_vWoM"

