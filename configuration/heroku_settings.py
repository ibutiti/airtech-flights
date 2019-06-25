from os import getenv
from configuration.settings import *

DEBUG = False
SECRET_KEY = getenv('SECRET_KEY')
DATABASES = {
    'default': ''
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': getenv('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        }
    }
}

AWS_ACCESS_KEY_ID = getenv('AWS_ACCESS_KEY_ID')
AWS_S3_REGION_NAME = getenv('AWS_S3_REGION_NAME')
AWS_SECRET_ACCESS_KEY = getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = getenv('AWS_STORAGE_BUCKET_NAME')
DEFAULT_FROM_EMAIL = getenv('DEFAULT_FROM_EMAIL')
ANYMAIL = {
    'AMAZON_SES_CLIENT_PARAMS': {
        'region_name': getenv('AWS_SES_REGION_NAME', default='us-east-1')
    }
}
