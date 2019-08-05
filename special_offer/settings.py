"""
Django settings for special_offer project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import logging

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static/')
# MEDIA_DIR = os.path.join(BASE_DIR, 'media')
MEDIA_DIR = '/home/spffo/public_html/backend/media'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_0q@o$rf!f9-pls@&1@$m=r%0g9bpv%7wcikqoor!kmagcrr5n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'aahmedsamyspecialoffer.pythonanywhere.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'corsheaders',
    'users',
    'galleries',
    'offers',
    'ads',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'special_offer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'special_offer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'special_offer_db',
#         'USER': 'special_offer_user',
#         'PASSWORD': 'special_offer_password',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'spffo_special_offer_db',
#         'USER': 'spffo_nagy3n',
#         'PASSWORD': 'S6j^oHJ6^~$~',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ar'

TIME_ZONE = 'Asia/Dubai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


def gettext(s): return s


LANGUAGES = (
    ('ar', gettext('Arabic')),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = STATIC_DIR
MEDIA_ROOT = MEDIA_DIR

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles/"),
]

# Authentication model #####
AUTH_USER_MODEL = 'users.User'
################################

# rest framework ###############
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}
################################

# JWT AUTH #####################
JWT_AUTH = {
    "JWT_VERIFY_EXPIRATION": False,
    'JWT_ALLOW_REFRESH': False,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_PAYLOAD_HANDLER': 'users.jwt_custom.jwt_payload_handler',
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': 'users.jwt_custom.jwt_get_username_from_payload',
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.jwt_custom.jwt_response_payload_handler',
}
################################

# CORS HEADERS SETTINGS ########
CORS_ORIGIN_ALLOW_ALL = True
################################

logging.Formatter()
logging.basicConfig(filename='special_offer.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG if DEBUG else logging.INFO)

# EMAILS SETTINGS ##############

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'aahmedsamy.specialoffer@gmail.com'
EMAIL_HOST_PASSWORD = 'adminadminspecialoffer'
################################

# tinify #######################
TINIFY_API_KEY = "hgsRJGVhNMlGnYFGZP0WHmp8M21pQxyW"
################################

################################
# Twilio ########################
TWILIO_ACCOUNT_SID = "ACf57bfcde0f1ed047e6542af5ace1b22d"
TWILIO_AUTH_TOKEN = "a53f15649201f6a4dad2c6c836f531d4"
TWILIO_NUMBER = "+16156546342"
################################
