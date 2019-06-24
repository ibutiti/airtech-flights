'''
Settings file for testing with inmemory file storage, faster password hasher, synchronous queues
'''
from configuration.settings import *

DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
# Turn async off for testing
for queue_config in RQ_QUEUES.values():
    queue_config['ASYNC'] = False
