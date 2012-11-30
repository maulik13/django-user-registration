from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from user_registration.appsettings import CONFIG_MODULE_PATH


try:
    config = import_module(CONFIG_MODULE_PATH)
except ImportError as e:
    raise ImproperlyConfigured('Error importing config module %s: "%s"' % (CONFIG_MODULE_PATH, e))
