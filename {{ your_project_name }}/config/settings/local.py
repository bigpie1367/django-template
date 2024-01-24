from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = True

SECRET_KEY = "zfDWHBKWfpTNYgpFPssdoS3eav3b5uqkkudcoW099XGGNZrA9s1MMCUXkY9xyhPj"

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

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
