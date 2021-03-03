from django.contrib.auth.models import User

def anggotabagian(nama_manager, bagian):
    users = User.objects.filter(last_name=bagian).exclude(first_name=nama_manager)
    return users

def apamanager(user):
    return user.groups.filter(name='Manager').exists()