from config.project_config import settings

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": settings.postgres.dbname,
        "USER": settings.postgres.user,
        "PASSWORD": settings.postgres.password,
        "HOST": settings.postgres.host,
        "PORT": settings.postgres.port,
        "OPTIONS": {"options": "-c search_path=public,content"},
    }
}
