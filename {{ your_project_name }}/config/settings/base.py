"""
Base settings to build other settings files upon.
"""
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / "{{ your_project_name }}"
env = environ.Env()

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG", False)

TIME_ZONE = "Asia/Seoul"
LANGUAGE_CODE = "en-us"

USE_I18N = True
USE_TZ = True

# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="postgres:///{{ your_project_name }}",
    ),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = [
]

LOCAL_APPS = [
    "{{ your_app_name }}"
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# MIGRATION_MODULES = {"sites": ".contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
AUTH_USER_MODEL = "{{ your_app_name }}.User"

LOGIN_REDIRECT_URL = "users:redirect"

LOGIN_URL = "account_login"

# PASSWORDS
# ------------------------------------------------------------------------------
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
STATIC_ROOT = str(BASE_DIR / "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(APPS_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
MEDIA_ROOT = str(APPS_DIR / "media")
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# FIXTURES
# ------------------------------------------------------------------------------
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"

# ADMIN
# ------------------------------------------------------------------------------
ADMIN_URL = "admin/"

# # Celery
# # ------------------------------------------------------------------------------
# if USE_TZ:
#     # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-timezone
#     CELERY_TIMEZONE = TIME_ZONE
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
# CELERY_BROKER_URL = env("CELERY_BROKER_URL")
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
# CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-extended
# CELERY_RESULT_EXTENDED = True
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-always-retry
# # https://github.com/celery/celery/pull/6122
# CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-max-retries
# CELERY_RESULT_BACKEND_MAX_RETRIES = 10
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-accept_content
# CELERY_ACCEPT_CONTENT = ["json"]
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-task_serializer
# CELERY_TASK_SERIALIZER = "json"
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_serializer
# CELERY_RESULT_SERIALIZER = "json"
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
# # TODO: set to whatever value is adequate in your circumstances
# CELERY_TASK_TIME_LIMIT = 5 * 60
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
# # TODO: set to whatever value is adequate in your circumstances
# CELERY_TASK_SOFT_TIME_LIMIT = 60
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
# CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-send-task-events
# CELERY_WORKER_SEND_TASK_EVENTS = True
# # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_send_sent_event
# CELERY_TASK_SEND_SENT_EVENT = True
# # django-allauth
# # ------------------------------------------------------------------------------
# ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# # https://docs.allauth.org/en/latest/account/configuration.html
# ACCOUNT_AUTHENTICATION_METHOD = "username"
# # https://docs.allauth.org/en/latest/account/configuration.html
# ACCOUNT_EMAIL_REQUIRED = True
# # https://docs.allauth.org/en/latest/account/configuration.html
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# # https://docs.allauth.org/en/latest/account/configuration.html
# ACCOUNT_ADAPTER = ".users.adapters.AccountAdapter"
# # https://docs.allauth.org/en/latest/account/forms.html
# ACCOUNT_FORMS = {"signup": "{{ emp_project_name }}.users.forms.UserSignupForm"}
# # https://docs.allauth.org/en/latest/socialaccount/configuration.html
# SOCIALACCOUNT_ADAPTER = ".users.adapters.SocialAccountAdapter"
# # https://docs.allauth.org/en/latest/socialaccount/configuration.html
# SOCIALACCOUNT_FORMS = {"signup": ".users.forms.UserSocialSignupForm"}

# # django-rest-framework
# # -------------------------------------------------------------------------------
# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework.authentication.SessionAuthentication",
#         "rest_framework.authentication.TokenAuthentication",
#     ),
#     "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
#     "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
# }

# # django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
# CORS_URLS_REGEX = r"^/api/.*$"

# # By Default swagger ui is available only to admin user(s). You can change permission classes to change that
# # See more configuration options at https://drf-spectacular.readthedocs.io/en/latest/settings.html#settings
# SPECTACULAR_SETTINGS = {
#     "TITLE": " API",
#     "DESCRIPTION": "Documentation of API endpoints of ",
#     "VERSION": "1.0.0",
#     "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
# }
# # Your stuff...
# # ------------------------------------------------------------------------------
