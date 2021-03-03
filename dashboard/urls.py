from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('profile/', views.profile, name='profile'),

    # CEO
    path('home_ceo/', views.index_ceo, name='ceo'),
    path('daftar_manager/', views.daftar_manager, name='daftar_manager'),

    # MANAGER
    path('manager/', views.manager, name='manager'),
    path('registrasi_eksekutif/', views.registrasi_eksekutif, name='registrasi_eksekutif'),
    path('input_tugas_proyek/<int:id_eksekutif>', views.input_tugas_proyek, name='input_tugas_proyek'),
    path('input_tugas_rutin/<int:id_eksekutif>', views.input_tugas_rutin, name='input_tugas_rutin'),
    path('daftar_eksekutif/', views.daftar_eksekutif, name='daftar_eksekutif'),
    path('delete_eksekutif/<int:id_eksekutif>', views.delete_eksekutif, name='delete_eksekutif'),
    path('mdetail_proyek/<int:id_tugas>', views.mdetail_proyek, name='mdetail_proyek'),
    path('mdetail_rutin/<int:id_tugas>', views.mdetail_rutin, name='mdetail_rutin'),
    path('tuntas/<int:id_tugas>', views.tuntas, name='tuntas'),
    path('rutin_tuntas/<int:id_tugas>', views.rutin_tuntas, name='rutin_tuntas'),
    path('edit_tugas_proyek/<int:id_tugas>', views.edit_tugas_proyek, name='edit_tugas_proyek'),
    path('edit_tugas_rutin/<int:id_tugas>', views.edit_tugas_rutin, name='edit_tugas_rutin'),
    path('progress_tugas_rutin/<int:id_tugas>', views.progress_tugas_rutin, name='progress_tugas_rutin'),
    path('tugas_aktif_manager/', views.tugas_aktif_manager, name="tugas_aktif_manager"),
    path('tugas_tuntas_manager/', views.tugas_tuntas_manager, name='tugas_tuntas_manager'),
    
    # EKSEKUTIF
    path('eksekutif/', views.eksekutif, name='eksekutif'),
    path('daftar_tugas/', views.daftar_tugas, name='daftar_tugas'),
    path('tugas_tuntas/', views.tugas_tuntas, name='tugas_tuntas'),
    path('daftar_tugas_rutin/<int:id_tugas>', views.daftar_tugas_rutin, name='daftar_tugas_rutin'),
    path('detail_tugas_proyek/<int:id_tugas>', views.detail_tugas_proyek, name='detail_tugas_proyek'),
    path('upload_dokumentasi_tp/<int:id_tugas>', views.upload_dokumentasi_tp, name='upload_dokumentasi_tp'),
    path('upload_dokumentasi_tr/<int:id_tugas>', views.upload_dokumentasi_tr, name='upload_dokumentasi_tr'),
    path('lihat_tugas/', views.lihat_tugas, name='lihat_tugas'),
    path('lihat_tugas_tuntas/', views.lihat_tugas_tuntas, name='lihat_tugas_tuntas'),
    
    # DATA KARYAWAN
    path('data_karyawan/', views.data_karyawan, name='data_karyawan'),
    path('tambah_data_karyawan/', views.tambah_data_karyawan, name='tambah_data_karyawan'),
    path('detail_data_karyawan/<int:id_karyawan>', views.detail_data, name='detail_data_karyawan'),
    path('karyawan_keluar/<int:id_karyawan>', views.karyawan_keluar, name='karyawan_keluar'),
    path('halaman_edit_karyawan/<int:id_karyawan>', views.halaman_edit, name='halaman_edit_karyawan'),
    path('karyawan_tidak_aktif/', views.karyawan_tidak_aktif, name='karyawan_tidak_aktif'),
    path('test_webhook/', views.test_webhook, name='test_webhook'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
