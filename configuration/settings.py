import environ

ROOT_DIR = environ.Path(__file__) - 2
env = environ.Env()

env.read_env(str(ROOT_DIR.path(".env")))

SECRET_KEY = env('SECRET_KEY', default='some_secret_key')

DEBUG = env('DEBUG', default='False')

ALLOWED_HOSTS = ['0.0.0.0', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.postgres',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_rq',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'authentication',
    'flights',
    'payments',
    'reservations',
    'tickets',
    'userprofile',
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'configuration.authentication.BearerTokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'EXCEPTION_HANDLER': 'common.middleware.drf_custom_handler'
}

AUTH_USER_MODEL = 'authentication.User'

ROOT_URLCONF = 'configuration.urls'

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

WSGI_APPLICATION = 'configuration.wsgi.application'

TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_DIR = 'test-results/airtech-api'
TEST_OUTPUT_FILE_NAME = 'results.xml'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': env.db(
        default='postgres://postgres:postgres@db:5432/postgres',
        engine='django.db.backends.postgresql_psycopg2')
}

CACHES = {
    'default': env.cache(
        default='rediscache://127.0.0.1:6379/1?client_class=django_redis.client.DefaultClient',
    )
}

# RQ configs
RQ_QUEUES = {
    'default': {
        'USE_REDIS_CACHE': 'default',
        'DEFAULT_TIMEOUT': 600
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# aws file storage settings via django-storages
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_AUTO_CREATE_BUCKET = True
AWS_BUCKET_ACL = AWS_DEFAULT_ACL
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', default='your-chosen-s3-bucket-name')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='your-bucket-aws-region')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default='obtained-from-your-aws-console')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default='obtained-from-your-aws-console')
