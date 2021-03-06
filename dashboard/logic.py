from django.contrib.auth.models import User
from .models import DataStruk, PeriodeKerja, Complaint, KepuasanPelanggan
from datetime import datetime, timedelta
from django.utils import timezone
import pytz

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
    
    CABANG = ['Antapani', 'Cisitu', 'Jatinangor', 'Kopo', 'Metro', 'Sukabirus', 'Sukapura', 'Sukajadi', 'Unjani', 'All Crisbar']

    c = Complaint.objects.all()
    c = c.exclude(jenis="Lainnya")
    complaint_periode = c.filter(tanggal__range=[periode.awal_periode, periode.akhir_periode])
    complaint_periode_sebelumnya = c.filter(tanggal__range=[periode_sebelumnya.awal_periode, periode_sebelumnya.akhir_periode])
    
    complaint_cabang = [fungsi_helper_untuk_fungsi_di_bawah(c, complaint_periode, complaint_periode_sebelumnya) for c in CABANG]
    antapani, cisitu, jatinangor, kopo, metro, sukabirus, sukapura, sukajadi, unjani, all_crisbar = complaint_cabang

    return antapani, cisitu, jatinangor, kopo, metro, sukabirus, sukapura, sukajadi, unjani, all_crisbar

def query_kepuasan_pelanggan_dashboard():
    semua_kp = KepuasanPelanggan.objects.all().order_by('-tanggal')
    sesudah_sebelum_kp = semua_kp[:2]
    sesudah = sesudah_sebelum_kp[0]
    sebelum = sesudah_sebelum_kp[1]

    if sesudah.google_kopo == None:
        sesudah.google_kopo = 0.0
    if sesudah.gofood_kopo == None:
        sesudah.gofood_kopo = 0.0
    if sesudah.grabfood_kopo == None:
        sesudah.grabfood_kopo = 0.0
    if sesudah.survei_kopo == None:
        sesudah.survei_kopo = 0.0

    if sebelum.google_kopo == None:
        sebelum.google_kopo = 0.0
    if sebelum.gofood_kopo == None:
        sebelum.gofood_kopo = 0.0
    if sebelum.grabfood_kopo == None:
        sebelum.grabfood_kopo = 0.0
    if sebelum.survei_kopo == None:
        sebelum.survei_kopo = 0.0

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

        ["Kopo",
        sesudah.google_kopo, berselisih(sesudah.google_kopo, sebelum.google_kopo), 
        sesudah.gofood_kopo, berselisih(sesudah.gofood_kopo, sebelum.gofood_kopo), 
        sesudah.grabfood_kopo, berselisih(sesudah.grabfood_kopo, sebelum.grabfood_kopo), 
        sesudah.survei_kopo, berselisih(sesudah.survei_kopo, sebelum.survei_kopo),
        sesudah.dapat_average("Kopo"), berselisih(sesudah.dapat_average("Kopo"), sebelum.dapat_average("Kopo"))
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

def format_rupiah(angka):

    if isinstance(angka, float):
        angka = str(angka)
        angka = angka.split('.')
        angka = angka[0]
        angka = int(angka)

    if angka >= 1000000:
        jutaan = angka // 1000000
        pengurang = jutaan * 1000000
        angka = angka - pengurang

        ribuan = angka // 1000
        pengurang = ribuan * 1000
        ribuan = "00000" + str(ribuan)
        ribuan = ribuan[-3:]

        angka = angka - pengurang
        sisa = '00000' + str(angka)
        sisa = sisa[-3:]

        return "Rp. " + str(jutaan) + '.' + ribuan + '.' + sisa
    elif angka >= 1000:
        ribuan = angka // 1000
        pengurang = ribuan * 1000
        angka = angka - pengurang

        sisa = '00000' + str(angka)
        sisa = sisa[-3:]
        
        return "Rp. " + str(ribuan) + '.' + sisa
    else:
        return str(angka)

def query_penjualan_harian_dashboard(PERIODE):
    struk = PeriodeKerja.objects.get(pk=PERIODE)
    
    awal_periode = datetime(struk.awal_periode.year, struk.awal_periode.month, struk.awal_periode.day, 0, 0, 1, tzinfo=pytz.UTC) - timedelta(hours=7)
    akhir_periode = datetime(struk.akhir_periode.year, struk.akhir_periode.month, struk.akhir_periode.day, 23, 59, 59, tzinfo=pytz.UTC) - timedelta(hours=7)
    
    sekarang = timezone.now()
    selisih = sekarang - awal_periode

    struk_periode = DataStruk.objects.filter(created_at__range=[awal_periode, akhir_periode])
    struk_periode = struk_periode.order_by('created_at')
    
    dine_in_take_away_antapani = 0
    gofood_antapani = 0
    grabfood_antapani = 0
    
    dine_in_take_away_cisitu = 0
    gofood_cisitu = 0
    grabfood_cisitu = 0

    dine_in_take_away_jatinangor = 0
    gofood_jatinangor = 0
    grabfood_jatinangor = 0

    dine_in_take_away_metro = 0
    gofood_metro = 0
    grabfood_metro = 0
    
    dine_in_take_away_sukabirus = 0
    gofood_sukabirus = 0
    grabfood_sukabirus = 0

    dine_in_take_away_sukapura = 0
    gofood_sukapura = 0
    grabfood_sukapura = 0

    dine_in_take_away_sukajadi = 0
    gofood_sukajadi = 0
    grabfood_sukajadi = 0

    dine_in_take_away_unjani = 0
    gofood_unjani = 0
    grabfood_unjani = 0
    
    i = 1
    for a in struk_periode:
        if "GO FOOD" in a.nama_pembayaran:
            
            if "Antapani" in a.outlet:
                gofood_antapani += a.money_amount
            elif "Cisitu" in a.outlet:
                gofood_cisitu += a.money_amount
            elif "Jatinangor" in a.outlet:
                gofood_jatinangor += a.money_amount
            elif "Metro" in a.outlet:
                gofood_metro += a.money_amount
            elif "Sukabirus" in a.outlet:
                gofood_sukabirus += a.money_amount
            elif "Sukapura" in a.outlet:
                gofood_sukapura += a.money_amount
            elif "Sukajadi" in a.outlet:
                gofood_sukajadi += a.money_amount
            elif "Unjani" in a.outlet:
                gofood_unjani += a.money_amount

        elif "GRAB" in a.nama_pembayaran:

            if "Antapani" in a.outlet:
                grabfood_antapani += a.money_amount
            elif "Cisitu" in a.outlet:
                grabfood_cisitu += a.money_amount
            elif "Jatinangor" in a.outlet:
                grabfood_jatinangor += a.money_amount
            elif "Metro" in a.outlet:
                grabfood_metro += a.money_amount
            elif "Sukabirus" in a.outlet:
                grabfood_sukabirus += a.money_amount
            elif "Sukapura" in a.outlet:
                grabfood_sukapura += a.money_amount
            elif "Sukajadi" in a.outlet:
                grabfood_sukajadi += a.money_amount
            elif "Unjani" in a.outlet:
                grabfood_unjani += a.money_amount
        else:
            if "Antapani" in a.outlet:
                dine_in_take_away_antapani += a.money_amount
            elif "Cisitu" in a.outlet:
                dine_in_take_away_cisitu += a.money_amount
            elif "Jatinangor" in a.outlet:
                dine_in_take_away_jatinangor += a.money_amount
            elif "Metro" in a.outlet:
                dine_in_take_away_metro += a.money_amount
            elif "Sukabirus" in a.outlet:
                dine_in_take_away_sukabirus += a.money_amount
            elif "Sukapura" in a.outlet:
                dine_in_take_away_sukapura += a.money_amount
            elif "Sukajadi" in a.outlet:
                dine_in_take_away_sukajadi += a.money_amount
            elif "Unjani" in a.outlet:
                dine_in_take_away_unjani += a.money_amount
        
    hasil = [
        ["Antapani", format_rupiah(dine_in_take_away_antapani/selisih.days), format_rupiah((gofood_antapani/selisih.days)*0.8), format_rupiah((grabfood_antapani/selisih.days)*0.8), format_rupiah( (dine_in_take_away_antapani/selisih.days)+((gofood_antapani/selisih.days)*0.8)+((grabfood_antapani/selisih.days)*0.8) )],
        ["Cisitu", format_rupiah(dine_in_take_away_cisitu/selisih.days), format_rupiah((gofood_cisitu/selisih.days)*0.8), format_rupiah((grabfood_cisitu/selisih.days)*0.8), format_rupiah( (dine_in_take_away_cisitu/selisih.days)+((gofood_cisitu/selisih.days)*0.8)+((grabfood_cisitu/selisih.days)*0.8) )],
        ["Jatinangor", format_rupiah(dine_in_take_away_jatinangor/selisih.days), format_rupiah((gofood_jatinangor/selisih.days)*0.8), format_rupiah((grabfood_jatinangor/selisih.days)*0.8), format_rupiah( (dine_in_take_away_jatinangor/selisih.days)+((gofood_jatinangor/selisih.days)*0.8)+((grabfood_jatinangor/selisih.days)*0.8) )],
        ["Metro", format_rupiah(dine_in_take_away_metro/selisih.days), format_rupiah((gofood_metro/selisih.days)*0.8), format_rupiah((grabfood_metro/selisih.days)*0.8), format_rupiah( (dine_in_take_away_metro/selisih.days)+((gofood_metro/selisih.days)*0.8)+((grabfood_metro/selisih.days)*0.8) )],
        ["Sukabirus", format_rupiah(dine_in_take_away_sukabirus/selisih.days), format_rupiah((gofood_sukabirus/selisih.days)*0.8), format_rupiah((grabfood_sukabirus/selisih.days)*0.8), format_rupiah( (dine_in_take_away_sukabirus/selisih.days)+((gofood_sukabirus/selisih.days)*0.8)+((grabfood_sukabirus/selisih.days)*0.8) )],
        ["Sukapura", format_rupiah(dine_in_take_away_sukapura/selisih.days), format_rupiah((gofood_sukapura/selisih.days)*0.8), format_rupiah((grabfood_sukapura/selisih.days)*0.8), format_rupiah( (dine_in_take_away_sukapura/selisih.days)+((gofood_sukapura/selisih.days)*0.8)+((grabfood_sukapura/selisih.days)*0.8) )],
        ["Sukajadi", format_rupiah(dine_in_take_away_sukajadi/selisih.days), format_rupiah((gofood_sukajadi/selisih.days)*0.8), format_rupiah((grabfood_sukajadi/selisih.days)*0.8), format_rupiah( (dine_in_take_away_sukajadi/selisih.days)+((gofood_sukajadi/selisih.days)*0.8)+((grabfood_sukajadi/selisih.days)*0.8) )],
        ["Unjani", format_rupiah(dine_in_take_away_unjani/selisih.days), format_rupiah((gofood_unjani/selisih.days)*0.8), format_rupiah((grabfood_unjani/selisih.days)*0.8), format_rupiah( (dine_in_take_away_unjani/selisih.days)+((gofood_unjani/selisih.days)*0.8)+((grabfood_unjani/selisih.days)*0.8))],
    ]
    
    return hasil


def query_perhitungan_penjualan_harian_dashboard(PERIODE, periode_sebelumnya=False):
    struk = PeriodeKerja.objects.get(pk=PERIODE)
    
    awal_periode = datetime(struk.awal_periode.year, struk.awal_periode.month, struk.awal_periode.day, 0, 0, 1, tzinfo=pytz.UTC) - timedelta(hours=7)
    akhir_periode = datetime(struk.akhir_periode.year, struk.akhir_periode.month, struk.akhir_periode.day, 23, 59, 59, tzinfo=pytz.UTC) - timedelta(hours=7)
    
    if periode_sebelumnya:
        sekarang = akhir_periode
    else:
        sekarang = timezone.now()
    
    selisih = sekarang - awal_periode

    struk_periode = DataStruk.objects.filter(created_at__range=[awal_periode, akhir_periode])
    struk_periode = struk_periode.order_by('created_at')
    
    dine_in_take_away_antapani = 0
    gofood_antapani = 0
    grabfood_antapani = 0
    
    dine_in_take_away_cisitu = 0
    gofood_cisitu = 0
    grabfood_cisitu = 0

    dine_in_take_away_jatinangor = 0
    gofood_jatinangor = 0
    grabfood_jatinangor = 0

    dine_in_take_away_metro = 0
    gofood_metro = 0
    grabfood_metro = 0
    
    dine_in_take_away_sukabirus = 0
    gofood_sukabirus = 0
    grabfood_sukabirus = 0

    dine_in_take_away_sukapura = 0
    gofood_sukapura = 0
    grabfood_sukapura = 0

    dine_in_take_away_sukajadi = 0
    gofood_sukajadi = 0
    grabfood_sukajadi = 0

    dine_in_take_away_unjani = 0
    gofood_unjani = 0
    grabfood_unjani = 0
    
    for a in struk_periode:
        if "GO FOOD" in a.nama_pembayaran:
            
            if "Antapani" in a.outlet:
                gofood_antapani += a.money_amount - 800
            elif "Cisitu" in a.outlet:
                gofood_cisitu += a.money_amount - 800
            elif "Jatinangor" in a.outlet:
                gofood_jatinangor += a.money_amount - 800
            elif "Metro" in a.outlet:
                gofood_metro += a.money_amount - 800
            elif "Sukabirus" in a.outlet:
                gofood_sukabirus += a.money_amount - 800
            elif "Sukapura" in a.outlet:
                gofood_sukapura += a.money_amount - 800
            elif "Sukajadi" in a.outlet:
                gofood_sukajadi += a.money_amount - 800
            elif "Unjani" in a.outlet:
                gofood_unjani += a.money_amount - 800

        elif "GRAB" in a.nama_pembayaran:

            if "Antapani" in a.outlet:
                grabfood_antapani += a.money_amount
            elif "Cisitu" in a.outlet:
                grabfood_cisitu += a.money_amount
            elif "Jatinangor" in a.outlet:
                grabfood_jatinangor += a.money_amount
            elif "Metro" in a.outlet:
                grabfood_metro += a.money_amount
            elif "Sukabirus" in a.outlet:
                grabfood_sukabirus += a.money_amount
            elif "Sukapura" in a.outlet:
                grabfood_sukapura += a.money_amount
            elif "Sukajadi" in a.outlet:
                grabfood_sukajadi += a.money_amount
            elif "Unjani" in a.outlet:
                grabfood_unjani += a.money_amount
        else:

            if ("OVO" in a.nama_pembayaran) or ("SHOPEE PAY" in a.nama_pembayaran) or ("GOPAY" in a.nama_pembayaran):
                jumlah_uang = a.money_amount * 0.993
            else:
                jumlah_uang = a.money_amount

            if "Antapani" in a.outlet:
                dine_in_take_away_antapani += jumlah_uang
            elif "Cisitu" in a.outlet:
                dine_in_take_away_cisitu += jumlah_uang
            elif "Jatinangor" in a.outlet:
                dine_in_take_away_jatinangor += jumlah_uang
            elif "Metro" in a.outlet:
                dine_in_take_away_metro += jumlah_uang
            elif "Sukabirus" in a.outlet:
                dine_in_take_away_sukabirus += jumlah_uang
            elif "Sukapura" in a.outlet:
                dine_in_take_away_sukapura += jumlah_uang
            elif "Sukajadi" in a.outlet:
                dine_in_take_away_sukajadi += jumlah_uang
            elif "Unjani" in a.outlet:
                dine_in_take_away_unjani += jumlah_uang
        
    hasil = [
        # Dine in Take Away, Go food, grabfood, total
        [dine_in_take_away_antapani/selisih.days, (gofood_antapani/selisih.days)*0.8, (grabfood_antapani/selisih.days)*0.8, (dine_in_take_away_antapani/selisih.days)+((gofood_antapani/selisih.days)*0.8)+((grabfood_antapani/selisih.days)*0.8) ],             # ANTAPANI
        [dine_in_take_away_cisitu/selisih.days, (gofood_cisitu/selisih.days)*0.8, (grabfood_cisitu/selisih.days)*0.8, (dine_in_take_away_cisitu/selisih.days)+((gofood_cisitu/selisih.days)*0.8)+((grabfood_cisitu/selisih.days)*0.8) ],                         # CISITU
        [dine_in_take_away_jatinangor/selisih.days, (gofood_jatinangor/selisih.days)*0.8, (grabfood_jatinangor/selisih.days)*0.8, (dine_in_take_away_jatinangor/selisih.days)+((gofood_jatinangor/selisih.days)*0.8)+((grabfood_jatinangor/selisih.days)*0.8) ], # JATINANGOR
        [dine_in_take_away_metro/selisih.days, (gofood_metro/selisih.days)*0.8, (grabfood_metro/selisih.days)*0.8, (dine_in_take_away_metro/selisih.days)+((gofood_metro/selisih.days)*0.8)+((grabfood_metro/selisih.days)*0.8) ],                               # METRO
        [dine_in_take_away_sukabirus/selisih.days, (gofood_sukabirus/selisih.days)*0.8, (grabfood_sukabirus/selisih.days)*0.8, (dine_in_take_away_sukabirus/selisih.days)+((gofood_sukabirus/selisih.days)*0.8)+((grabfood_sukabirus/selisih.days)*0.8) ],       # SUKABIRUS
        [dine_in_take_away_sukapura/selisih.days, (gofood_sukapura/selisih.days)*0.8, (grabfood_sukapura/selisih.days)*0.8, (dine_in_take_away_sukapura/selisih.days)+((gofood_sukapura/selisih.days)*0.8)+((grabfood_sukapura/selisih.days)*0.8) ],             # SUKAPURA
        [dine_in_take_away_sukajadi/selisih.days, (gofood_sukajadi/selisih.days)*0.8, (grabfood_sukajadi/selisih.days)*0.8, (dine_in_take_away_sukajadi/selisih.days)+((gofood_sukajadi/selisih.days)*0.8)+((grabfood_sukajadi/selisih.days)*0.8) ],             # SUKAJADI
        [dine_in_take_away_unjani/selisih.days, (gofood_unjani/selisih.days)*0.8, (grabfood_unjani/selisih.days)*0.8, (dine_in_take_away_unjani/selisih.days)+((gofood_unjani/selisih.days)*0.8)+((grabfood_unjani/selisih.days)*0.8)],                          # UNJANI
    ]
    
    return hasil

def dapat_selisih_penjualan_harian(PERIODE):
    hasil_periode = query_perhitungan_penjualan_harian_dashboard(PERIODE)
    hasil_periode_sebelumnya = query_perhitungan_penjualan_harian_dashboard((PERIODE-1), True)
    
    hasil = []
    i = 0
    for hp in hasil_periode:
        j = 0
        list_dalam = []
        for h in hp:
            selisih = h - hasil_periode_sebelumnya[i][j]
            if selisih > 0:
                list_dalam.append('+' + str(format_rupiah(selisih)))
            elif selisih < 0:
                selisih = -selisih
                list_dalam.append('-' + format_rupiah(selisih))
            else:
                list_dalam.append(format_rupiah(selisih))
            j += 1
        hasil.append(list_dalam)
        i += 1
    return hasil

def tren_penjualan_harian(PERIODE):
    tph = query_perhitungan_penjualan_harian_dashboard(PERIODE)
    tph_rupiah = [ [format_rupiah(i) for i in isi] for isi in tph]
    tph_selisih = dapat_selisih_penjualan_harian(PERIODE)

    cabang = ['Antapani', 'Cisitu', 'Jatinangor', 'Metro', 'Sukabirus', 'Sukapura', 'Sukajadi', 'Unjani']
    hasil = []
    i = 0
    for tph in tph_rupiah:
        j = 0
        hsl = []
        hsl.append(cabang[i])
        for isi in tph:
            hsl.append([isi, tph_selisih[i][j]])
            j += 1
        hasil.append(hsl)
        i += 1

    return hasil

def tren_penjualan_harian_all_crisbar(PERIODE):
    total_dine_in = 0
    perhitungan = query_perhitungan_penjualan_harian_dashboard(PERIODE)

    total_dine_in = sum([a[0] for a in perhitungan])
    total_gofood = sum([a[1] for a in perhitungan])
    total_grabfood = sum([a[2] for a in perhitungan])
    total_all_crisbar = sum([a[3] for a in perhitungan])

    return ["All Crisbar", format_rupiah(total_dine_in), format_rupiah(total_gofood), format_rupiah(total_grabfood), format_rupiah(total_all_crisbar)]

def tren_penjualan_harian_all_crisbar_debugging(PERIODE):
    sekarang = query_perhitungan_penjualan_harian_dashboard(PERIODE)
    periode_lalu = query_perhitungan_penjualan_harian_dashboard(PERIODE, True)

    hasil = []
    i = 0
    for isi in sekarang:
        j = 0
        hasil2 = []
        for isi_dalem in isi:
            selisih = isi_dalem - periode_lalu[i][j]
            hasil2.append(selisih)
            j += 1
        i += 1
        hasil.append(hasil2)

    return hasil
