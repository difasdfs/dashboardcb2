from django.contrib.auth.models import User
from .models import PeriodeKerja, Complaint

def anggotabagian(nama_manager, bagian):
    users = User.objects.filter(last_name=bagian).exclude(first_name=nama_manager)
    return users

def apamanager(user):
    return user.groups.filter(name='Manager').exists()

def fungsi_helper_untuk_fungsi_di_bawah(cabangnya, complaint_periode, complaint_periode_sebelumnya):
    
    if cabangnya != "All Crisbar":
        complaint_cabang = complaint_periode.filter(cabang=cabangnya)
        complaint_cabang_sebelumnya = complaint_periode_sebelumnya.filter(cabang=cabangnya)
    else:
        complaint_cabang = complaint_periode
        complaint_cabang_sebelumnya = complaint_periode_sebelumnya

    total_complaint_cabang = len(complaint_cabang)
    total_complaint_cabang_sebelumnya = len(complaint_cabang_sebelumnya)

    kualitas_produk_cabang = complaint_cabang.filter(jenis="Kualitas Produk")
    kualitas_produk_cabang = len(kualitas_produk_cabang)
    kualitas_produk_cabang_sebelumnya = complaint_cabang_sebelumnya.filter(jenis="Kualitas Produk")
    kualitas_produk_cabang_sebelumnya = len(kualitas_produk_cabang_sebelumnya)

    kebersihan_cabang = complaint_cabang.filter(jenis="Kebersihan")
    kebersihan_cabang = len(kebersihan_cabang)
    kebersihan_cabang_sebelumnya = complaint_cabang_sebelumnya.filter(jenis="Kebersihan")
    kebersihan_cabang_sebelumnya = len(kebersihan_cabang_sebelumnya)

    pelayanan_cabang = complaint_cabang.filter(jenis="Pelayanan")
    pelayanan_cabang = len(pelayanan_cabang)
    pelayanan_cabang_sebelumnya = complaint_cabang_sebelumnya.filter(jenis="Pelayanan")
    pelayanan_cabang_sebelumnya = len(pelayanan_cabang_sebelumnya)

    tidak_lengkap_cabang = complaint_cabang.filter(jenis="Tidak Lengkap")
    tidak_lengkap_cabang = len(tidak_lengkap_cabang)
    tidak_lengkap_cabang_sebelumnya = complaint_cabang_sebelumnya.filter(jenis="Tidak Lengkap")
    tidak_lengkap_cabang_sebelumnya = len(tidak_lengkap_cabang_sebelumnya)

    cabang = [
        (kualitas_produk_cabang, str(kualitas_produk_cabang - kualitas_produk_cabang_sebelumnya)),
        (kebersihan_cabang, str(kebersihan_cabang-kebersihan_cabang_sebelumnya)),
        (pelayanan_cabang, str(pelayanan_cabang-pelayanan_cabang_sebelumnya)),
        (tidak_lengkap_cabang, str(tidak_lengkap_cabang-tidak_lengkap_cabang_sebelumnya)),
        (total_complaint_cabang, str(total_complaint_cabang-total_complaint_cabang_sebelumnya))
    ]

    return cabang

def query_complaint_dashboard(PERIODE):
    periode = PeriodeKerja.objects.get(pk=PERIODE)
    periode_sebelumnya = PeriodeKerja.objects.get(pk=(PERIODE-1))
    
    c = Complaint.objects.all()
    c = c.exclude(jenis="Lainnya")
    complaint_periode = c.filter(tanggal__range=[periode.awal_periode, periode.akhir_periode])
    complaint_periode_sebelumnya = c.filter(tanggal__range=[periode_sebelumnya.awal_periode, periode_sebelumnya.akhir_periode])

    antapani = fungsi_helper_untuk_fungsi_di_bawah("Antapani", complaint_periode, complaint_periode_sebelumnya)
    cisitu = fungsi_helper_untuk_fungsi_di_bawah("Cisitu", complaint_periode, complaint_periode_sebelumnya)
    jatinangor = fungsi_helper_untuk_fungsi_di_bawah("Jatinangor", complaint_periode, complaint_periode_sebelumnya)
    metro = fungsi_helper_untuk_fungsi_di_bawah("Metro", complaint_periode, complaint_periode_sebelumnya)
    sukabirus = fungsi_helper_untuk_fungsi_di_bawah("Sukabirus", complaint_periode, complaint_periode_sebelumnya)
    sukapura = fungsi_helper_untuk_fungsi_di_bawah("Sukapura", complaint_periode, complaint_periode_sebelumnya)
    sukajadi = fungsi_helper_untuk_fungsi_di_bawah("Sukajadi", complaint_periode, complaint_periode_sebelumnya)
    unjani = fungsi_helper_untuk_fungsi_di_bawah("Unjani", complaint_periode, complaint_periode_sebelumnya)
    all_crisbar = fungsi_helper_untuk_fungsi_di_bawah("All Crisbar", complaint_periode, complaint_periode_sebelumnya)

    return antapani, cisitu, jatinangor, metro, sukabirus, sukapura, sukajadi, unjani, all_crisbar