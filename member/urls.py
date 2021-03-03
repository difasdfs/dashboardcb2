from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.halaman_login, name="login"), 
    path('logout/', views.logoutuser, name="logout"),
    
    # DEPARTEMEN IT
    path('index_it/', views.index_it, name="index_it"),
    path('akun_member/', views.akun_member, name='akun_member'),
    path('akun_backoffice/', views.akun_backoffice, name='akun_backoffice'),
    path('buat_akun_backoffice/', views.buat_akun_backoffice, name='buat_akun_backoffice'),
    path('buat_akun_member/', views.buat_akun_member, name='buat_akun_member'),
    path('detail_akun_member/<int:id_member>', views.detail_akun_member, name='detail_akun_member'),
    
    # MEMBER
    path('index/', views.index_member, name='index_member'),
    path('ubah_akun_member/', views.ubah_akun_member, name='ubah_akun_member'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)