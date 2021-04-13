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

    hasil = [
        ["Antapani", 
        sesudah.google_antapani, berselisih(sesudah.google_antapani, sebelum.google_antapani), 
        sesudah.gofood_antapani, berselisih(sesudah.gofood_antapani, sebelum.gofood_antapani), 
        sesudah.grabfood_antapani, berselisih(sesudah.grabfood_antapani, sebelum.grabfood_antapani), 
        sesudah.survei_antapani, berselisih(sesudah.survei_antapani, sebelum.survei_antapani),
        sesudah.dapat_average("Antapani"), berselisih(sesudah.dapat_average("Antapani"), sebelum.dapat_average("Antapani"))
        ],

        ["Cisitu", 
        sesudah.google_cisitu, berselisih(sesudah.google_cisitu, sebelum.google_cisitu), 
        sesudah.gofood_cisitu, berselisih(sesudah.gofood_cisitu, sebelum.gofood_cisitu), 
        sesudah.grabfood_cisitu, berselisih(sesudah.grabfood_cisitu, sebelum.grabfood_cisitu), 
        sesudah.survei_cisitu, berselisih(sesudah.survei_cisitu, sebelum.survei_cisitu),
        sesudah.dapat_average("Cisitu"), berselisih(sesudah.dapat_average("Cisitu"), sebelum.dapat_average("Cisitu"))
        ],

        ["Jatinangor", 
        sesudah.google_jatinangor, berselisih(sesudah.google_jatinangor, sebelum.google_jatinangor), 
        sesudah.gofood_jatinangor, berselisih(sesudah.gofood_jatinangor, sebelum.gofood_jatinangor), 
        sesudah.grabfood_jatinangor, berselisih(sesudah.grabfood_jatinangor, sebelum.grabfood_jatinangor), 
        sesudah.survei_jatinangor, berselisih(sesudah.survei_jatinangor, sebelum.survei_jatinangor),
        sesudah.dapat_average("Jatinangor"), berselisih(sesudah.dapat_average("Jatinangor"), sebelum.dapat_average("Jatinangor"))
        ],

        ["Metro", 
        sesudah.google_metro, berselisih(sesudah.google_metro, sebelum.google_metro), 
        sesudah.gofood_metro, berselisih(sesudah.gofood_metro, sebelum.gofood_metro), 
        sesudah.grabfood_metro, berselisih(sesudah.grabfood_metro, sebelum.grabfood_metro), 
        sesudah.survei_metro, berselisih(sesudah.survei_metro, sebelum.survei_metro),
        sesudah.dapat_average("Metro"), berselisih(sesudah.dapat_average("Metro"), sebelum.dapat_average("Metro"))
        ],

        ["Sukabirus", 
        sesudah.google_sukabirus, berselisih(sesudah.google_sukabirus, sebelum.google_sukabirus), 
        sesudah.gofood_sukabirus, berselisih(sesudah.gofood_sukabirus, sebelum.gofood_sukabirus), 
        sesudah.grabfood_sukabirus, berselisih(sesudah.grabfood_sukabirus, sebelum.grabfood_sukabirus), 
        sesudah.survei_sukabirus, berselisih(sesudah.survei_sukabirus, sebelum.survei_sukabirus),
        sesudah.dapat_average("Sukabirus"), berselisih(sesudah.dapat_average("Sukabirus"), sebelum.dapat_average("Sukabirus"))
        ],

        ["Sukapura", 
        sesudah.google_sukapura, berselisih(sesudah.google_sukapura, sebelum.google_sukapura), 
        sesudah.gofood_sukapura, berselisih(sesudah.gofood_sukapura, sebelum.gofood_sukapura), 
        sesudah.grabfood_sukapura, berselisih(sesudah.grabfood_sukapura, sebelum.grabfood_sukapura), 
        sesudah.survei_sukapura, berselisih(sesudah.survei_sukapura, sebelum.survei_sukapura),
        sesudah.dapat_average("Sukapura"), berselisih(sesudah.dapat_average("Sukapura"), sebelum.dapat_average("Sukapura"))
        ],

        ["Sukajadi", 
        sesudah.google_sukajadi, berselisih(sesudah.google_sukajadi, sebelum.google_sukajadi), 
        sesudah.gofood_sukajadi, berselisih(sesudah.gofood_sukajadi, sebelum.gofood_sukajadi), 
        sesudah.grabfood_sukajadi, berselisih(sesudah.grabfood_sukajadi, sebelum.grabfood_sukajadi), 
        sesudah.survei_sukajadi, berselisih(sesudah.survei_sukajadi, sebelum.survei_sukajadi),
        sesudah.dapat_average("Sukajadi"), berselisih(sesudah.dapat_average("Sukajadi"), sebelum.dapat_average("Sukajadi"))
        ],

        ["Unjani", 
        sesudah.google_unjani, berselisih(sesudah.google_unjani, sebelum.google_unjani), 
        sesudah.gofood_unjani, berselisih(sesudah.gofood_unjani, sebelum.gofood_unjani), 
        sesudah.grabfood_unjani, berselisih(sesudah.grabfood_unjani, sebelum.grabfood_unjani), 
        sesudah.survei_unjani, berselisih(sesudah.survei_unjani, sebelum.survei_unjani),
        sesudah.dapat_average("Unjani"), berselisih(sesudah.dapat_average("Unjani"), sebelum.dapat_average("Unjani"))
        ],
    ]

    return hasil
    # print(sesudah, sebelum)

def query_box_home(PERIODE):
    total_complaint = 0
    sebelum = 0
    trend = 0

    # COMPLAINT
    periode = PeriodeKerja.objects.get(pk=PERIODE)
    periode_sebelumnya = PeriodeKerja.objects.get(pk=(PERIODE-1))
    complaint_periode = Complaint.objects.filter(tanggal__range=[periode.awal_periode, periode.akhir_periode]).exclude(jenis="Lainnya")
    complaint_periode_sebelumnya = Complaint.objects.filter(tanggal__range=[periode_sebelumnya.awal_periode, periode_sebelumnya.akhir_periode]).exclude(jenis="Lainnya")
    
    total_complaint = len(complaint_periode)
    sebelum = len(complaint_periode_sebelumnya)
    trend = selisih_trend(total_complaint, sebelum)

    # KEPUASAN PELENAGGAN
    semua_kp = KepuasanPelanggan.objects.all().order_by('-tanggal')
    sesudah_sebelum_kp = semua_kp[:2]
    sekarang_kp = sesudah_sebelum_kp[0]
    sebelum_kp = sesudah_sebelum_kp[1]
    avg_semua = sekarang_kp.dapat_average_semua()
    avg_sebelum = sebelum_kp.dapat_average_semua()
    trend_kp = selisih_trend(avg_semua, avg_sebelum)

    hasil = {
        'complaint' : {'total_complaint' : total_complaint, 'sebelum' : sebelum, 'trend' : trend},
        'kepuasan_pelanggan' : {'avg_semua' : avg_semua, 'sebelum': avg_sebelum, 'trend' : trend_kp}
    }

    return hasil