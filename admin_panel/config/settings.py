from pathlib import Path

from split_settings.tools import include, optional
from config.project_config import settings

include(
    "components/database.py",
    "components/installed_apps.py",
    "components/middleware.py",
    "components/auth_password_validators.py",
    "components/templates.py",
    "components/secret_key.py",
)

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = settings.django.debug

ALLOWED_HOSTS = settings.django.hosts.split(",")

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
