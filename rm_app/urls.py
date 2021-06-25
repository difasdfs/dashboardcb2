from django.urls import path
from . import views


urlpatterns = [
    path('hello_world/', views.hello_world, name='hello_world'),
    path('login_page/', views.login_page, name='login_page'),
    path('logoutuser/', views.logoutuser, name='logoutuser'),
    path('ubah_akun/', views.ubah_akun, name='ubah_akun'),
    path("jadwal_kerja_rencana/", views.jadwal_kerja_rencana, name="jadwal_kerja_rencana"),
    path('statistik_jadwal_kerja/', views.statistik_jadwal_kerja, name="statistik_jadwal_kerja"),
    path('varian_shift/', views.varian_shift, name="varian_shift"),
    path('absen/', views.absen, name='absen'),
    path('shift/', views.shift, name='shift'),
    path('', views.index_rm, name='index_rm')
]
