from django.core.exceptions import PermissionDenied
from .models import *

def user_is_register(function):
    def wrap(request, *args, **kwargs):
        if hasattr(request.user,'register') and request.user.has_perm('core.can_view_register'):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_doctor(function):
    def wrap(request, *args, **kwargs):
        if hasattr(request.user,'doctor') and request.user.has_perm('core.can_view_doctor'):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
        
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap