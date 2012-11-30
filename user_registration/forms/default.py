"""
Registration forms should be based on your User model. You can define custom forms
in "forms" package.
"""

from django.contrib.auth import get_user_model
from django import forms


class DefaultRegistrationForm(forms.Form):
	"""
	User registration form based on a User model containing username and email
	"""
	
	email = forms.EmailField(label='Email', max_length=75,
	                         error_messages={'required': "Email is required for registration"})
	username = forms.RegexField(regex=r'^[\w.@+-]+$', max_length=30,
	                            label='Username',
	                            error_messages={'invalid': "Username may contain only letters, \
	                            numbers and characters . _", 'required': "Username is required for registration"})
	password = forms.CharField(label='Password',
	                            widget=forms.PasswordInput(attrs={}, render_value=False))
	password_re = forms.CharField(label='Confirm password',
	                            widget=forms.PasswordInput(attrs={}, render_value=False))
	
	
	def clean_email(self):
		"""
		Check that provided email address does not already exist
		"""
		User = get_user_model()
		email_in_db = User.objects.filter(email__iexact=self.cleaned_data['email'])
		if email_in_db.exists():
			raise forms.ValidationError("This email address is in use")
		else:
			return self.cleaned_data['email']
		
		
	def clean_username(self):
		"""
		Validate username does not already exist. 
		"""
		User = get_user_model()
		username_in_db = User.objects.filter(username__iexact=self.cleaned_data['username'])
		if username_in_db.exists():
			raise forms.ValidationError("This username is already used by other account")
		else:
			return self.cleaned_data['username']
		
	
	def clean(self):
		"""
		General form validation
		1. Check both passwords match
		Error generation here is not linked with field, but with the form
		"""
		pwd1 = self.cleaned_data.get('password', None)
		pwd2 = self.cleaned_data.get('password_re', None)
		if pwd1 and pwd2:
			if pwd1 != pwd2:
				raise forms.ValidationError('Passwords did not match')
		return self.cleaned_data
	
	