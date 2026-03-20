from .base import *

DEBUG = False
ALLOWED_HOSTS = get_secret("ALLOWED_HOSTS", default="", cast=Csv())

# Example: PostgreSQL for production
DATABASES = {
    "default": {
        "ENGINE": get_secret("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": get_secret("DB_NAME"),
        "USER": get_secret("DB_USER"),
        "PASSWORD": get_secret("DB_PASSWORD"),
        "HOST": get_secret("DB_HOST"),
        "PORT": get_secret("DB_PORT", cast=int),
    }
}

# Static files for production
STATIC_ROOT = BASE_DIR / "staticfiles"

# Example email get_secret for production
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = get_secret("EMAIL_HOST")
EMAIL_PORT = get_secret("EMAIL_PORT", cast=int)
EMAIL_HOST_USER = get_secret("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_secret("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = get_secret("DEFAULT_FROM_EMAIL")