'''
Settings file for testing with inmemory file storage and faster password hasher
'''
from configuration.settings import *

DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
