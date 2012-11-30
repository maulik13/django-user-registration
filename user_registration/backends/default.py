from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from user_registration.models import UserRegistration
from user_registration.appsettings import KEY_VALIDITY_DURATION
from user_registration.configs import config
from user_registration import appsettings


class DefaultRegistrationBackend(object):
    """
    Backend defines how the registration and activation processes are defined
    
    @register: What to do after valid register form data is receieved
    @activate: Activation process for a user based on registration data
    @is_registration_open: defines if registration is open
    """
    
    def register(self, request, **kwargs):
        """
        Registration process is defined in this method. This should do the following:
        1. Store the appropriate data based on your logic
        2. Send an email / SMS or any other action for registration process
        
        'kwargs' should contain all the required parameters to create a user
        we can confirm that by using REQUIRED_FIELDS list + USERNAME_FIELD in the User model 
        """
        # create the user and registration data for this user
        new_user, reg_data = UserRegistration.objects.register_user(**kwargs)
        
        # Send an email
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        reg_data.send_activation_email(site)
        return new_user
    
    
    def activate(self, request, activation_key):
        """
        Activation process should be defined here. By default, it is only doing check
        against activation key when user accesses this URL.
        
        You could also check against a secret code that should be provided by the user in
        addition to the key. This code can be sent to the user in registration process by
        email, SMS etc.
        """
        activated = UserRegistration.objects.activate_user(activation_key)
        return activated
        
        
    def is_registration_open(self):
        """
        Override this method to add logic for deciding when registration is allowed
        """
        return True
