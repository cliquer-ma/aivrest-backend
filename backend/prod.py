from .settings import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

# sentry_sdk.init(
#     dsn                     = "https://f88ded6bebe4876cf3704c4411a59d88@o4508654167130112.ingest.us.sentry.io/4508654167261184",
#     integrations            = [DjangoIntegration()],
#     traces_sample_rate      = 1.0,
#     profiles_sample_rate    = 1.0,
#     send_default_pii        = True
# )

ALLOWED_HOSTS                   = [".ma", ".com"]

DEBUG                           = False
CORS_REPLACE_HTTPS_REFERER      = True
HOST_SCHEME                     = "https://"

SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT             = True
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_SECONDS             = 1000000
SECURE_FRAME_DENY               = True
SECURE_HSTS_PRELOAD             = True
SECURE_BROWSER_XSS_FILTER       = True
SECURE_CONTENT_TYPE_NOSNIFF     = True

SESSION_COOKIE_SAMESITE         = 'Strict'
SESSION_COOKIE_SECURE           = True

CSRF_COOKIE_SECURE              = True
CSRF_USE_SESSIONS               = True
CSRF_COOKIE_HTTPONLY            = True

CSP_DEFAULT_SRC                 = ("'none'", )
CSP_CONNECT_SRC                 = ("'self'", )
CSP_OBJECT_SRC                  = ("'none'", )
CSP_BASE_URI                    = ("'none'", )
CSP_FRAME_ANCESTORS             = ("'none'", )
CSP_FORM_ACTION                 = ("'self'", )
CSP_INCLUDE_NONCE_IN            = ('script-src',)

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
