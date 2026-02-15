import os
from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

BACKEND_URL=os.getenv('BACKEND_URL')

DJANGO_SECRET_KEY=os.getenv('DJANGO_SECRET_KEY')

DATABASE_NAME=os.getenv('DATABASE_NAME')
DATABASE_OWNER=os.getenv('DATABASE_OWNER')
DATABASE_PASSWORD=os.getenv('DATABASE_PASSWORD')
DATABASE_HOST=os.getenv('DATABASE_HOST')
DATABASE_PORT=os.getenv('DATABASE_PORT')

EMAIL_BACKEND=os.getenv('EMAIL_BACKEND')
EMAIL_HOST=os.getenv('EMAIL_HOST')
EMAIL_USE_TLS=os.getenv('EMAIL_USE_TLS')
EMAIL_PORT_SSL=os.getenv('EMAIL_PORT_SSL')
EMAIL_PORT_TLS=os.getenv('EMAIL_PORT_TLS')
EMAIL_HOST_USER=os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=os.getenv('EMAIL_HOST_PASSWORD')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
AUTH_USER_MODEL = 'app.User'

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'app',
    'psycopg2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_OWNER,
        'PASSWORD': DATABASE_PASSWORD, 
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
USE_I18N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
ADMIN_ENABLE_NAV_SIDEBAR = True

USE_TZ = True
TIME_ZONE = 'Asia/Dhaka'