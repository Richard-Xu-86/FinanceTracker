from pathlib import Path #Used to create safe, cross-platform file paths
from django.contrib import messages
from dotenv import load_dotenv #Loads environment variables from a .env file
load_dotenv()
import os #Lets you access environment variables and file system paths
import dj_database_url



BASE_DIR = Path(__file__).resolve().parent.parent #defines the rootfolder, manage.py

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')#Secret cryptographic key used by Django for 
#security features like sessions and tokens. Loaded from .env.

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']#List of domains that can access your site

SITE_NAME = 'FinanceTracker'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'userexpense',
    'userprefer',
    'userincome',
    'dashboard',
    'allauth'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', #allows Django to serve static files (CSS, JS) in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'FinanceTracker.urls' #Start routing URLs using FinanceTracker/urls.py

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], #A folder for global templates like main.html
        'APP_DIRS': True, #tells django to search each apps templates/ folders
        'OPTIONS': {
            'context_processors': [ #	Automatically injects useful data into every HTML template
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'userprefer.context_processer.Appdata'
            ],
        },
    },
]

WSGI_APPLICATION = 'FinanceTracker.wsgi.application' #build bridge between django and web server


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}
#DATABASES = {
   # 'default': {
        #'ENGINE': 'django.db.backends.postgresql',
        #'NAME': os.environ.get('DB_NAME'),
        #'USER' : os.environ.get('DB_USER'),
        #'PASSWORD' : os.environ.get('DB_USER_PASSWORD'),
        #'HOST' : os.environ.get('DB_HOST'),
        #'PORT' : os.environ.get('DB_PORT'),
   # }
#}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Toronto'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOGIN_URL = 'login'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MESSAGE_TAGS = {
    messages.ERROR :'danger'
}


#how django sends emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_USE_TLS = os.environ.get('EMAIL_TLS') == 'True'
EMAIL_FROM_EMAIL = os.environ.get('EMAIL_FROM_EMAIL')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT'))
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
