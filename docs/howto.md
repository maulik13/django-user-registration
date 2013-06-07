Usage
--------------------
* Make sure the appsettings has proper configuration values
* Link registration page with URL name in the urls.py
* For customization read details below
* To return a custom HttpResponse after registration/activation check the following variables in the config module:
 * after_registration_method = None
 * after_activation_method = None


Config
--------------------
* Check the configuration in the configs package, default values are defined in default.py
* A config module defines the following:
    * URLs
    * Backend
    * Forms
    * Templates


Customization
--------------------
Customization can be done in the following areas:


##### URLs #####
Url names are modified in the config module

##### Templates #####
Create new templates in the template folder and update their references in the config file


##### Forms #####
Create a new form in the forms package and then change its reference in config module