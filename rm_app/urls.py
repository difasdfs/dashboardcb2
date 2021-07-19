from django.urls import path
from purchase_order import views as views_po
from . import views


urlpatterns = [
    path('hello_world/', views.hello_world, name='hello_world'),
    path('form_po_cabang/<int:id_po>', views_po.form_po_cabang, name='form_po_cabang'),
    path('po_gunung_mas/<int:id_po>', views_po.po_gunung_mas, name='po_gunung_mas'),
    path('gunung_mas/', views_po.gunung_mas, name='gunung_mas'),
    path('terima_barang/<int:id_po>', views_po.terima_barang, name='terima_barang'),
    

    path('penerimaan/', views_po.penerimaan, name='penerimaan'),
    path('konfirmasi_order/<int:id_po>', views_po.konfirmasi_order, name='konfirmasi_order'),
    path('login_page/', views.login_page, name='login_page'),
    path('logoutuser/', views.logoutuser, name='logoutuser'),
    path('ubah_akun/', views.ubah_akun, name='ubah_akun'),
    path("jadwal_kerja_rencana/", views.jadwal_kerja_rencana, name="jadwal_kerja_rencana"),
    path('purchase_order/', views_po.purchase_order, name='purchase_order'),
    path('statistik_jadwal_kerja/', views.statistik_jadwal_kerja, name="statistik_jadwal_kerja"),
    path('varian_shift/', views.varian_shift, name="varian_shift"),
    path('absen/', views.absen, name='absen'),
    path('shift/', views.shift, name='shift'),
    path('', views.index_rm, name='index_rm')
]
