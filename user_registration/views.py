from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.contrib import messages

from user_registration import appsettings 
from user_registration.utils import get_module_object
from user_registration.configs import config
from user_registration import models


def register(request, backend, form_class, template, **kwargs):
    """
    View for new user registration. The view fetches the appropriate form 
    depending on the configuration defined in config file.
    
    Registration view can have three results:
    1. Registration is closed, no new user signups.
    2. Registration was complete (successful).
    3. Registration failed due to backend error.
    
    For registration 'closed' and 'failed' events you can use a custom template defined by config.
    For registration 'complete' you can either use a customized template or provide a function
    that returns a HttpResponse.
    """ 
    backend = get_module_object(backend)()
    if backend.is_registration_open():
        return redirect(reverse('register_closed'))
    
    form_class = get_module_object(form_class)
    
    if request.method == 'POST':
        form = form_class(data = request.POST)
        if form.is_valid():
            user = backend.register(request, **form.cleaned_data)
            if user is not None:
                # If custom method to return Response object
                if config.after_registration_method:
                    after_reg_method = get_module_object(config.after_registration_method)
                    return after_reg_method(request, user)
                # TODO email and username needs to be flexible
                messages.success(request, user.email, extra_tags='register')
                messages.success(request, user.username, extra_tags='register')                
                return redirect(reverse('register_complete'))
            return redirect(reverse('register_failed'))
    else:
        form = form_class()
        
    return render(request, template, {'form': form})


def register_complete(request, template_name):
    """
    Default view after registration is complete
    """
    message_list = []
    registration_msgs = messages.get_messages(request)
    for message in registration_msgs:
        if 'reg' in message.tags:
            message_list.append(message.message)
    data = {}
    try:
        data['email'] = message_list[0]
        data['username']= message_list[1]
    except:
        pass
    return render(request, template_name, data)


def activate(request, backend, form_class, template, **kwargs):
    """
    Link to this view is sent to the user for activation. The form for activation is optional.
    form_class can be set Activation page can include additional input required by user based on the process.
    Hence this view should also handle POST method and pass captured data to the activation backend.
    
    Activation could just use the activation key in the URL, or Enter a code sent via email or SMS 
    """
    do_activate = False
    # if activation requires input from user
    if form_class:
        if request.method == 'POST':
            form = form_class(data = request.POST)
            if form.is_valid():
                kwargs.update(request.POST)
                do_activate = True
        else:
            form = form_class()
        if not do_activate:
            return render(request, template, {'form':form})
    
    # We have reached the activation process    
    backend_class = get_module_object(backend)
    try:
        user = backend_class().activate(request, **kwargs)
    except Exception, e:
        messages.success(request, e.__class__.__name__, extra_tags='activate')
        return redirect(reverse('activate_failed'))
    
    # If custom method needs to return Response object
    if config.after_activation_method:
        after_act_method = get_module_object(config.after_activation_method)
        return after_act_method(request, user)
    
    return redirect(reverse('activate_complete'))
