import random
import datetime
import hashlib

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.template.loader import render_to_string

from user_registration.appsettings import HASH_USER_FIELD, KEY_VALIDITY_DURATION, FROM_EMAIL
from user_registration.configs import config
from user_registration.utils import get_model_field_values


class ActivationKeyInvalid(Exception):
    pass


class ActivationKeyExpired(Exception):
    pass


class UserAlreadyActivated(Exception):
    pass


class UserRegistrationManager(models.Manager):

    """
    Manager for handling user registration data
    """

    def register_user(self, **kwargs):
        """
        This function should create a user based on user model and create registration profile
        'kwargs' contains the same fields required by the User model (custom or default)
        This app requires only one field in the user model, that is 'is_active'
        """
        # Create user based on the current user model
        UserModel = get_user_model()
        user_data = get_model_field_values(UserModel, kwargs)
        # Assume that the form data dict keys match the fields in the User model
        user = UserModel.objects.create_user(**user_data)
        user.is_active = False
        user.save()
        reg_data = self.create_reg_info(user)
        return user, reg_data

    def create_reg_info(self, user):
        """
        This function should be used to create a registration data for a user. This wil create
        an activation key by using a hash of a user field (based on appsettings).
        """
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        hash_src_str = getattr(user, HASH_USER_FIELD)
        activation_key = hashlib.sha1(salt + hash_src_str).hexdigest()
        key_expiry_time = timezone.now() + datetime.timedelta(KEY_VALIDITY_DURATION)
        reg_data = self.create(user=user, activation_key=activation_key, key_expiry_time=key_expiry_time)
        return reg_data

    def activate_user(self, activation_key):
        """
        Activate a user with given activation_key by calling the record level
        activation function. This allows other applications to activate a user from
        the user object directly.
        """
        try:
            reg_info = self.get(activation_key=activation_key)
        except self.model.DoesNotExist:
            raise ActivationKeyInvalid

        reg_info.activate_user()


class UserRegistration(models.Model):

    """
    Supporting table for storing registration info
    """

    UserModel = get_user_model()
    user = models.OneToOneField(UserModel)
    activation_key = models.CharField('activation key', max_length=40)
    secret_code = models.CharField('secret code', max_length=10, null=True)
    key_expiry_time = models.DateTimeField('key expiration time')

    objects = UserRegistrationManager()

    def __unicode__(self):
        return "{0}".format(self.user)

    def is_activation_key_expired(self):
        return self.key_expiry_time < timezone.now()

    def activate_user(self):
        """
        Following conditions should be met:
        1. User is not already active
        2. Activation key is not expired
        """
        if not self.user.is_active:
            if not self.is_activation_key_expired():
                self.user.is_active = True
                self.user.save()
                # delete this profile? or add/change a flag?
                return True
            raise ActivationKeyExpired
        raise UserAlreadyActivated

    def send_activation_email(self, site):
        """send email to the user linked with this registration record"""
        ctx_dict = {'username': self.user.username,
                    'activation_key': self.activation_key,
                    'key_validity_duration': KEY_VALIDITY_DURATION,
                    'site': site}

        subject = render_to_string(config.register_email_subject_template, ctx_dict)
        subject = ''.join(subject.splitlines())  # subject must be one line
        message = render_to_string(config.register_email_body_template, ctx_dict)

        self.user.email_user(subject, message, FROM_EMAIL)
