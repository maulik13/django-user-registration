from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module


def get_module_object(path):
    """
    Returns an object(of any type) from the module where last token is the object you are looking for
    e.g. Fetch a class object: get_module_object('app.backends.default.Class')
    e.g. Fetch a method object: get_module_object('app.backends.default.method')
    """
    i = path.rfind('.')
    module, attr = path[:i], path[i + 1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error loading registration backend %s: "%s"' % (module, e))
    try:
        mod_obj = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('"%s" in module "%s" is not a valid attribute' % (attr, module))
    return mod_obj


def get_model_field_values(model, data_dict):
    """
    Given a model and dictionary this function will return a new dictionary with keys matching the model fields
    """
    model_param_dict = {}
    model_fields = model._meta.get_all_field_names()

    for field in model_fields:
        if field in data_dict:
            model_param_dict[field] = data_dict[field]

    return model_param_dict
