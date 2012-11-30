"""
This file stores the application specific settings for user_registration
These settings variables can be overridden in site's settings.py by adding the prefix defined below.
e.g. To override what user model field should be used to generate hash, do this in settings.py
REG_HASH_USER_FIELD = 'openid'
"""

from django.conf import settings

# Prefix to be used for all the following variables in order to override them in settings.py
PREFIX = 'REG_'

# Flag to turn registration on/off, this is used by backend 
REGISTRATION_OPEN = getattr(settings, PREFIX+'REGISTRATION_OPEN', True)

# Name of User class field that should be used to generate hash for activation key
HASH_USER_FIELD = getattr(settings, PREFIX+'HASH_USER_FIELD', 'email')

# Validity duration of activation key in DAYS 
KEY_VALIDITY_DURATION = getattr(settings, PREFIX+'KEY_VALIDITY_DURATION', 100)

# Configure user-registration using this module, you can create a new config module and set it here
CONFIG_MODULE_PATH = getattr(settings, PREFIX+'CONFIG_MODULE_PATH', 'user_registration.configs.default')

# From email address, default is based on default email from site settings 
FROM_EMAIL = getattr(settings, PREFIX+'FROM_EMAIL', settings.DEFAULT_FROM_EMAIL)
