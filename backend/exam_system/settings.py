import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.geten("ie#4&qe7ra@e5(ci$%16#v*aafy8b!31n0i*amno3jiyw1st93")
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Настройки allauth
SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = "username_email"  # Вход по username или email
ACCOUNT_EMAIL_REQUIRED = True  # Email обязателен
ACCOUNT_UNIQUE_EMAIL = True  # Уникальный email
ACCOUNT_USERNAME_REQUIRED = True  # Обязательное поле username
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"  # Поле для username
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True  # Двойной ввод пароля
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_SESSION_REMEMBER = True  # Запоминать пользователя
ACCOUNT_EMAIL_VERIFICATION = "none"  # Без подтверждения email
LOGIN_REDIRECT_URL = "/exams/"  # После входа
LOGOUT_REDIRECT_URL = "/"  # После выхода
ACCOUNT_FORMS = {
    "signup": "accounts.forms.CustomSignupForm",
    "login": "accounts.forms.CustomLoginForm",
}

INSTALLED_APPS = [
    # Стандартные Django приложения
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Сторонние приложения
    "rest_framework",
    "rest_framework_simplejwt",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.yandex",
    # Локальные приложения
    "accounts",
    "exams",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "exam_system.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "exam_system.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Настройки аутентификации
AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Настройки REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("JWT", "Bearer"),
}

# Настройки OAuth (Yandex)
SOCIALACCOUNT_PROVIDERS = {
    "yandex": {
        "APP": {
            "client_id": os.getenv("fee73ba4acb14c9284b96351b02880ed"),
            "secret": os.getenv("G6ef7a6696700454b99337f0a9755fd27"),
            "key": "",
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {
            "access_type": "online",
            "prompt": "select_account",
        },
        "OAUTH_PKCE_ENABLED": True,
    }
}

# Настройки email (для разработки)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
