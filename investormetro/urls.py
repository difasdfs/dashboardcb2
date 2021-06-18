from django.urls import path
from . import views

urlpatterns = [
    path('halaman_login/', views.loginpage, name='halaman_login'),
    path('logout/', views.logoutuser, name='logout'),
    path('', views.index, name='indexcrisbarmetro'),
]
