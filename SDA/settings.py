"""
Django settings for SDA project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from SDA.pass_file import DB, CEDU, CSDU, IEDU, ISDU, DEDU, DSDU, SEDU, SSDU, SDE_ORD_PM, DEL_INV_OPER

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ojw$3b5u&f^l9-y@yov)#-qix*&09&rd%*+%sf9)p5@28(9mjm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0','192.168.0.230','192.168.0.240','77.65.12.246']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'djmoney',
    'TaskAPI',
    'PHONES',
    'DELEGATIONS',
    'ID_CARDS',
    'CARS',
    'RK',
    'HIP',
    'INVOICES',
    'INSURANCE',
    'SERVICES',
    'ORDERS',
    'LOG',
    'CASH_ADVANCES',
    'WORKER',
    'django_crontab',
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

ROOT_URLCONF = 'SDA.urls'

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

WSGI_APPLICATION = 'SDA.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # 'django.db.backends.postgresql',
        'NAME': DB[0],
        'USER': DB[1],
        'PASSWORD': DB[2],
        'HOST': DB[3],
        'PORT': DB[4],
    }
}



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'pl'

TIME_ZONE = 'Europe/Warsaw'
USE_I18N = True
USE_L10N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

CRISPY_TEMPLATE_PACK = 'bootstrap3'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

LOGIN_REDIRECT_URL = 'desktop'


MEDIA_ROOT = os.path.join(BASE_DIR, 'public', 'media')
MEDIA_URL = '/media/'


# 1- SKYPE, 2- EMAIL

DELEGATIONS_TO_TARGET = 1
DEL_EMAIL_DO_USERS = DEDU
DEL_SKYPE_DO_USERS = DSDU

# 1- SKYPE, 2- EMAIL

INVOICES_TO_TARGET = 1
INV_EMAIL_DO_USERS = IEDU
INV_SKYPE_DO_USERS = ISDU

# 1- SKYPE, 2- EMAIL

CARS_DATE_SHIFT = 30
CARS_LEASING_SHIFT = 60
CARS_TO_TARGET = 2
CARS_EMAIL_DO_USERS = CEDU
CARS_SKYPE_DO_USERS = CSDU

# 1- SKYPE, 2- EMAIL
SERVICES_DATA_SHIFT = 30
SERVICES_TO_TARGET = 2
SERVICES_EMAIL_DO_USERS = SEDU
SERVICES_SKYPE_DO_USERS = SSDU


# Wy??wietlanie
PAGIN_PAGE = 40
SIMPLE_VIEW = True

# MANEY
GET_NBP = ('EUR', 'GBP', 'USD', 'CHF')
HIS_NBP = 60
CURRENCIES = ('PLN', 'EUR', 'GBP', 'USD', 'CHF')
CURRENCY_CHOICES = [('PLN', 'PLN'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('USD', 'USD'), ('CHF', 'CHF'), ]

CRONJOBS = [
    ('00 05 * * 01,02,03,04,05', 'TaskAPI.cron.test_Cars'),
    ('50 04 * * *',              'TaskAPI.cron.select_Cars'),
    ('* * * * *',                'TaskAPI.cron.AllUpdate'),
    ('15 12 * * *',              'TaskAPI.cron.GetNBP'),
    ('*/30 * * * *',             'LOG.logs.LogToFile'),
]

#  Aby zadzia??a??o w cli wyda?? trzeba polecenie: ./manage.py crontab add

# Info program

INFO_PROGRAM = [
    {
        'WERSJA'     : '4.92g',
        'MODYFIKACJA': '16.02.2022r.',
        'FIRMA'      : 'EDATABIT',
        'AUTOR'      : 'Jaros??aw Str????yk',
        'EMAIL'      : 'mailto:biuro@edatabit.pl',
        'NEMAIL'     : 'biuro@edatabit.pl',
        'TEL'        : '+48 791-648-417',
    },
]

GOOGLE_CRED = BASE_DIR+'/BACKGROUND/sde-sda-credentials.json'

GOOGLE_DOCS_2021 = [
    ('', '', '', 'Kody SDE ??? SDE Plan finansowy 2021 i Nr zlece?? SmartDesignExpo 2019, 2020 i 2021.'),
    ('', '', '', 'Zam??wienia SDE ??? SDE Plan finansowy 2021 ??? SDE Koszty produkcji'),
    ('', '', '', 'Zam??wienia + Zaliczki MPK ??? SDE Plan finansowy 2021 ??? SDE Koszty sta??e'),
]


GOOGLE_DOCS_2022 = [
    ('Realizacja 2022', '11ajMbpwXTSrEXMtAPNTtB7v54GvlHNHP0YPWdC7BACc', 'SDA [Kody SDE]', 'SDA [Kody SDE] ??? Realizacja 2022'),
    ('Realizacja 2022', '11ajMbpwXTSrEXMtAPNTtB7v54GvlHNHP0YPWdC7BACc', 'SDA [Koszty produkcji]', 'SDA [Koszty produkcji] ??? Realizacja 2022'),
    ('Realizacja 2022', '11ajMbpwXTSrEXMtAPNTtB7v54GvlHNHP0YPWdC7BACc', 'SDA [Koszty sta??e]', 'SDA [Koszty sta??e] ??? Realizacja 2022'),
    ('Nr zlece?? SmartDesignExpo 2019, 2020, 2021 i 2022', '1Ev5MQW6GAg3XXsqads58orF_3WrMA35XCgKCYPFrB70', '2022', '')
]

# Pami??taj! Po zmianie LOG_LOOP trzeba r??cznie wykona?? LOG.logs.InitLog()
LOG_LOOP = 200
LOG_FILE = BASE_DIR+'/LOG_FILE/'

#

ORD_PM = SDE_ORD_PM
DEL_INV_OP = DEL_INV_OPER

#

WORKER_KM = '4.50'
