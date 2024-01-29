from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = True

SECRET_KEY = "zfDWHBKWfpTNYgpFPssdoS3eav3b5uqkkudcoW099XGGNZrA9s1MMCUXkY9xyhPj"

ALLOWED_HOSTS = ["*"]

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# # Celery
# # ------------------------------------------------------------------------------
# CELERY_TASK_EAGER_PROPAGATES = True
# # ------------------------------------------------------------------------------
