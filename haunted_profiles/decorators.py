from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def company_required(view_func):
    """Decorator to restrict view access to company users only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please log in to access this page.")
            return redirect('workos_login')
        
        if not request.user.is_company:
            messages.error(request, "This page is only accessible to company accounts.")
            return redirect('index')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def developer_required(view_func):
    """Decorator to restrict view access to developer users only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please log in to access this page.")
            return redirect('workos_login')
        
        if request.user.is_company:
            messages.error(request, "This page is only accessible to developer accounts.")
            return redirect('index')
        
        return view_func(request, *args, **kwargs)
    return wrapper
