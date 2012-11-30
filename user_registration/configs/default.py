"""
This module defines all the configurable variables to change application behavior.
To override these settings, you can copy this module and change the values or you can import
 this module and override only required variables.
"""

# URL parts definition
register_url = "register/"
register_closed_url = "registration/closed/"
register_complete_url = "registration/complete/"
register_failed_url = "registration/failed/"
activate_url = "activate/"
activate_complete_url = "activation/complete/"
activate_failed_url = "activation/failed/"

# Parameters passed to the registration and activation views
register_attrs = {'backend': 'user_registration.backends.default.DefaultRegistrationBackend',
                   'form_class': 'user_registration.forms.default.DefaultRegistrationForm',
                   'template': 'user_registration/default/register_form.html',
                   }

activate_attrs = {'backend': 'user_registration.backends.default.DefaultRegistrationBackend',
                   'form_class': None,
                   'template': 'user_registration/default/activate_form.html',
                   }

# Custom methods to be called when completing main actions (register and activate)
# These methods should return a Response object
after_registration_method = None
after_activation_method = None

# Define template paths here. Put the custom templates in templates/user_registration/yourfolder
register_email_subject_template = 'user_registration/default/register_email_subject.txt'
register_email_body_template = 'user_registration/default/register_email_body.txt'
register_closed_template = 'user_registration/default/register_closed.html'
register_complete_template = 'user_registration/default/register_complete.html'
register_failed_template = 'user_registration/default/register_failed.html'
activate_complete_template = 'user_registration/default/activate_complete.html'
activate_failed_template = 'user_registration/default/activate_failed.html'