from django.urls import path
from . import views


urlpatterns = [
    path('hello_world/', views.hello_world, name='hello_world'),
    path('login_page/', views.login_page, name='login_page'),
    path('logoutuser/', views.logoutuser, name='logoutuser'),
    path('ubah_akun/', views.ubah_akun, name='ubah_akun'),
    path('absen/', views.absen, name='absen'),
    path('', views.index_rm, name='index_rm')
]
