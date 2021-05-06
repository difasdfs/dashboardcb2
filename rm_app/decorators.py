from django.shortcuts import redirect
from rm_app.logika import isrm
from rm_app.logika.isrm import is_rm

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        is_rm(request.user)
        if request.user.is_authenticated:
            return redirect('index_rm')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
