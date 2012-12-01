Django User Registration
========================

This is a flexible app for user registration. It is compatible with latest Django 1.5.
The app has many configurable options to suit different needs. This config file is 
specified in "appsettings" module. Registration form should correspond to your User model fields. 


Notes:
-------
* "config" module defines options for URL, templates, forms, backend.  
* "backend" module defines the registration and activation processes.
* Custom forms should be defined in "forms" package.
* Your User model should contain 'isActive' field for activation process.
* By default this app uses 'email' field for creating activation key, if your
User model does not have this field change it in appsettings module.






