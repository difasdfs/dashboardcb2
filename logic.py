from django.contrib.auth.models import User
from .models import PeriodeKerja, Complaint, KepuasanPelanggan

def anggotabagian(nama_manager, bagian):
    users = User.objects.filter(last_name=bagian).exclude(first_name=nama_manager)
    return users

def apamanager(user):
    return user.groups.filter(name='Manager').exists()

def berselisih(variabel1, variabel2):
    hasil = variabel1 - variabel2
    if hasil > 0:
        return '+' + str(hasil)
    else:
        return str(hasil)

def selisih_trend(variabel1, variabel2):
    hasil = variabel1 - variabel2
    if hasil > 0:
        return '+' + str(hasil) + '↑'
    elif hasil == 0:
        return str(hasil)
    else:
        return str(hasil) + '↓'

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
        (cabangnya, ''),
        (kualitas_produk_cabang, berselisih(kualitas_produk_cabang, kualitas_produk_cabang_sebelumnya)),
        (kebersihan_cabang, berselisih(kebersihan_cabang, kebersihan_cabang_sebelumnya)),
        (pelayanan_cabang, berselisih(pelayanan_cabang, pelayanan_cabang_sebelumnya)),
        (tidak_lengkap_cabang, berselisih(tidak_lengkap_cabang, tidak_lengkap_cabang_sebelumnya)),
        (total_complaint_cabang, berselisih(total_complaint_cabang, total_complaint_cabang_sebelumnya)),
    ]

    return cabang

def query_complaint_dashboard(PERIODE):
    periode = PeriodeKerja.objects.get(pk=PERIODE)
    periode_sebelumnya = PeriodeKerja.objects.get(pk=(PERIODE-1))
    
    CABANG = ['Antapani', 'Cisitu', 'Jatinangor', 'Metro', 'Sukabirus', 'Sukapura', 'Sukajadi', 'Unjani', 'All Crisbar']

    c = Complaint.objects.all()
    c = c.exclude(jenis="Lainnya")
    complaint_periode = c.filter(tanggal__range=[periode.awal_periode, periode.akhir_periode])
    complaint_periode_sebelumnya = c.filter(tanggal__range=[periode_sebelumnya.awal_periode, periode_sebelumnya.akhir_periode])
    
    complaint_cabang = [fungsi_helper_untuk_fungsi_di_bawah(c, complaint_periode, complaint_periode_sebelumnya) for c in CABANG]
    antapani, cisitu, jatinangor, metro, sukabirus, sukapura, sukajadi, unjani, all_crisbar = complaint_cabang

    return antapani, cisitu, jatinangor, metro, sukabirus, sukapura, sukajadi, unjani, all_crisbar

def query_kepuasan_pelanggan_dashboard():
    print("fungsi query_kepuasan_pelanggan_dashboard kebaca")
    semua_kp = KepuasanPelanggan.objects.all().order_by('-tanggal')
    sesudah_sebelum_kp = semua_kp[:2]
    sesudah = sesudah_sebelum_kp[0]
    sebelum = sesudah_sebelum_kp[1]
    return sesudah
    # print(sesudah, sebelum)

def query_box_home(PERIODE):
    total_complaint = 0
    sebelum = 0
    trend = 0

    periode = PeriodeKerja.objects.get(pk=PERIODE)
    periode_sebelumnya = PeriodeKerja.objects.get(pk=(PERIODE-1))
    complaint_periode = Complaint.objects.filter(tanggal__range=[periode.awal_periode, periode.akhir_periode]).exclude(jenis="Lainnya")
    complaint_periode_sebelumnya = Complaint.objects.filter(tanggal__range=[periode_sebelumnya.awal_periode, periode_sebelumnya.akhir_periode]).exclude(jenis="Lainnya")
    
    total_complaint = len(complaint_periode)
    sebelum = len(complaint_periode_sebelumnya)
    trend = selisih_trend(total_complaint, sebelum)

    hasil = {
        'complaint' : {'total_complaint' : total_complaint, 'sebelum' : sebelum, 'trend' : trend}
    }

    return hasil