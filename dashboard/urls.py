from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('klasemen/', views.klasemen, name='klasemen'),
    path('average_check/', views.average_check, name='average_check'),
    path('upgrade_tc_ac/', views.upgrade_tc_ac, name='upgrade_tc_ac'),
    path('omset/', views.omset, name='omset'),
    path('update_dashboard/', views.update_dashboard, name='update_dashboard'),

    # CEO
    path('home_ceo/', views.index_ceo, name='ceo'),
    path('daftar_manager/', views.daftar_manager, name='daftar_manager'),
    path('edit_nilai/<int:id_isi_tugas_rutin>', views.edit_nilai, name='edit_nilai'),

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
    path('tugas_rutin_tuntas/<int:id_tugas>', views.tugas_rutin_tuntas, name='tugas_rutin_tuntas'),
    path('tugas_aktif_manager/', views.tugas_aktif_manager, name="tugas_aktif_manager"),
    path('tugas_tuntas_manager/', views.tugas_tuntas_manager, name='tugas_tuntas_manager'),
    path('duplikasi_tugas_proyek/<int:id_tugas>', views.duplikasi_tugas_proyek, name='duplikasi_tugas_proyek'),
    path('archive_tugas/', views.archive_tugas, name='archive_tugas'),
    path('eksekusi_archive_proyek/<int:id_tugas>', views.eksekusi_archive_proyek, name='eksekusi_archive_proyek'),
    path('eksekusi_archive_rutin/<int:id_tugas>', views.eksekusi_archive_rutin, name='eksekusi_archive_rutin'),
    path('kembalikan_archive_proyek/<int:id_tugas>', views.kembalikan_archive_proyek, name='kembalikan_archive_proyek'),
    path('kembalikan_archive_rutin/<int:id_tugas>', views.kembalikan_archive_rutin, name='kembalikan_archive_rutin'),
    path('lihat_tugas_per_nama/<int:id_user>', views.lihat_tugas_per_nama, name='lihat_tugas_per_nama'),
    path('input_tugas_proyek_kelompok/', views.input_tugas_proyek_kelompok, name="input_tugas_proyek_kelompok"),
    path('input_tugas_rutin_kelompok', views.input_tugas_rutin_kelompok, name="input_tugas_rutin_kelompok"),
    
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
    
    # SISTEM SP OTOMATIS
    path('index_sp/', views.index_sp, name='index_sp'),
    path('debugging_sp/', views.debugging_sp, name='debugging_sp'),
    path('eval_per_periode/', views.eval_per_periode, name='eval_per_periode'),
    path('eksekusi_sp/<int:id_periode_sp>', views.eksekusi_sp, name="eksekusi_sp"),

    # DATA KARYAWAN
    path('data_karyawan/', views.data_karyawan, name='data_karyawan'),
    path('tambah_data_karyawan/', views.tambah_data_karyawan, name='tambah_data_karyawan'),
    path('detail_data_karyawan/<int:id_karyawan>', views.detail_data, name='detail_data_karyawan'),
    path('karyawan_keluar/<int:id_karyawan>', views.karyawan_keluar, name='karyawan_keluar'),
    path('halaman_edit_karyawan/<int:id_karyawan>', views.halaman_edit, name='halaman_edit_karyawan'),
    path('karyawan_tidak_aktif/', views.karyawan_tidak_aktif, name='karyawan_tidak_aktif'),
    path('test_webhook/', views.test_webhook, name='test_webhook'),
    path('export_data_karyawan/', views.export_data_karyawan, name="export_data_karyawan"),
    path('export_karyawan_out/', views.export_karyawan_out, name="export_karyawan_out"),
    path('kepuasan_pelanggan/', views.kepuasan_pelanggan, name='kepuasan_pelanggan'),
    path('input_kepuasan_pelanggan/', views.input_kepuasan_pelanggan, name="input_kepuasan_pelanggan"),
    path('detail_kepuasan_pelanggan/<int:id_kepuasan_pelanggan>', views.detail_kepuasan_pelanggan, name="detail_kepuasan_pelanggan"),

    # ADMIN PSIKOTES
    path('index_alat_test/', views.index_alat_test, name='index_alat_test'),
    path('generate_token/', views.generate_token, name='generate_token'),
    path('daftar_token/', views.daftar_token, name='daftar_token'),
    path('hasil_psikotes/', views.hasil_psikotes, name='hasil_psikotes'),

    # PESERTA PSIKOTES
    path('psikotes/', views.psikotes, name='psikotes'),
    path('data_peserta_psikotes/', views.data_peserta_psikotes, name='data_peserta_psikotes'),
    path('petunjuk_1/', views.petunjuk_1, name='petunjuk_1'),
    path('soal_se_2/', views.soal_se_2, name='soal_se_2'),
    path('petunjuk_3/', views.petunjuk_3, name='petunjuk_3'),
    path('soal_wa_4/', views.soal_wa_4, name='soal_wa_4'),
    path('petunjuk_5/', views.petunjuk_5, name='petunjuk_5'),
    path('soal_an_6/', views.soal_an_6, name='soal_an_6'),
    path('petunjuk_7/', views.petunjuk_7, name='petunjuk_7'),
    path('soal_ge_8/', views.soal_ge_8, name='soal_ge_8'),
    path('petunjuk_9/', views.petunjuk_9, name='petunjuk_9'),
    path('soal_ra_10/', views.soal_ra_10, name='soal_ra_10'),
    path('petunjuk_11/', views.petunjuk_11, name='petunjuk_11'),
    path('soal_zr_12/', views.soal_zr_12, name='soal_zr_12'),
    path('petunjuk_13/', views.petunjuk_13, name='petunjuk_13'),
    path('soal_fa_14/', views.soal_fa_14, name='soal_fa_14'),
    path('petunjuk_15/', views.petunjuk_15, name='petunjuk_15'),
    path('soal_wu_16/', views.soal_wu_16, name='soal_wu_16'),
    path('petunjuk_17/', views.petunjuk_17, name='petunjuk_17'),
    path('hafalan_18/', views.hafalan_18, name='hafalan_18'),
    path('soal_me_19/', views.soal_me_19, name='soal_me_19'),

    # REKAP
    path('rekap/', views.rekap, name='rekap'),

    # MARKETING
    path('complaint_list/', views.complaint_list, name='complaint_list'),
    path('input_complaint/', views.input_complaint, name='input_complaint'),
    path('detail_complaint/<int:id_complaint>', views.detail_complaint, name='detail_complaint'),
    path('edit_complaint/<int:id_complaint>', views.edit_complaint, name='edit_complaint'),
    path('mystery_guest/', views.mystery_guest, name='mystery_guest'),
    path('input_mystery_guest/', views.input_mystery_guest, name='input_mystery_guest'),
    path('detail_mystery_guest/<int:id_mystery_guest>', views.detail_mystery_guest, name='detail_mystery_guest'),

    # SUPPLY CHAIN
    path('index_supply_chain/', views.index_supply_chain, name='index_supply_chain')
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
