from django.shortcuts import redirect


def is_rm(user):
    if not user.groups.filter(name='Restaurant Manager').exists():
        return redirect('logoutuser')