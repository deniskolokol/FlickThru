from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib import messages

from django.shortcuts import redirect
from functools import wraps

from django.utils.decorators import available_attrs

def forbidden_user(function=None, forbidden_usertypes=[]):
    """
    Decorator for views that checks that the user allowed, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.__class__.__name__ not in forbidden_usertypes,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def request_passes_test(test_func, redirect_url='/'):
    """
    Clone of django standart decorator 'user_passes_test'
    but instead of user object allows to work with request
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request, kwargs):
                return view_func(request, *args, **kwargs)
            messages.error(request, "You don't have access for this page")
            return redirect(redirect_url)
        return _wrapped_view
    return decorator


def cbv_decorator(decorator):
    """
    Turns a normal view decorator into a class-based-view decorator.

    Usage:

    @cbv_decorator(login_required)
    class MyClassBasedView(View):
        pass
    """
    def _decorator(cls):
        cls.dispatch = method_decorator(decorator)(cls.dispatch)
        return cls
    return _decorator
