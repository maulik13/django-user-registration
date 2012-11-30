"""
Configure URL strings in config file and other parameters to change urlconf
"""

from django.conf.urls import patterns, url
from django.shortcuts import render

from user_registration import views
from user_registration.configs import config


urlpatterns = patterns('',
    url(r'^{}$'.format(config.register_url), views.register, 
            config.register_attrs,
            name='register'),
    url(r'^{}$'.format(config.register_complete_url), views.register_complete,
            {'template_name':config.register_complete_template},
            name='register_complete'),
    url(r'^{}$'.format(config.register_failed_url), views.register_failed,
            {'template_name':config.register_failed_template},
            name='register_failed'),                       
    url(r'^{}$'.format(config.register_closed_url), render,
            {'template_name':config.register_closed_template},
            name='register_closed'),
    url(r'^{}(?P<activation_key>\w+)/$'.format(config.activate_url), views.activate,
            config.activate_attrs,
            name='activate'),
    url(r'^{}$'.format(config.activate_complete_url), render,
            {'template_name': config.activate_complete_template},
            name='activate_complete'),
    url(r'^{}$'.format(config.activate_failed_url), render,
            {'template_name': config.activate_failed_template},
            name='activate_failed'),    
)
