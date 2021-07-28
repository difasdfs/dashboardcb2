from .models import DataStruk
from dashboard.models import PeriodeKerja
import pytz
from datetime import datetime, timedelta

def main(PERIODE):

    # Crisbar Antapani
    # Crisbar Cisitu
    # Crisbar Jatinangor
    # Crisbar Kopo
    # Crisbar Metro Margahayu
    # Crisbar Sukabirus
    # Crisbar Sukapura
    # Crisbar Sukajadi
    # Crisbar Unjani

    periode_saat_ini = PERIODE
    query_sekarang_diformat = {
        "antapani" : filter_channel_pembayaran("Crisbar Antapani", periode_saat_ini),
        "cisitu" : filter_channel_pembayaran("Crisbar Cisitu", periode_saat_ini),
        "jatinangor" : filter_channel_pembayaran("Crisbar Jatinangor", periode_saat_ini),
        "kopo" : filter_channel_pembayaran("Crisbar Kopo", periode_saat_ini),
        "metro" : filter_channel_pembayaran("Crisbar Metro Margahayu", periode_saat_ini),
        "sukabirus" : filter_channel_pembayaran("Crisbar Sukabirus", periode_saat_ini),
        "sukapura" : filter_channel_pembayaran("Crisbar Sukapura", periode_saat_ini),
        "sukajadi" : filter_channel_pembayaran("Crisbar Sukajadi", periode_saat_ini),
        "unjani" : filter_channel_pembayaran("Crisbar Unjani", periode_saat_ini),
    }

    query_sekarang = {
        "antapani" : filter_channel_pembayaran("Crisbar Antapani", periode_saat_ini, diformat=False),
        "cisitu" : filter_channel_pembayaran("Crisbar Cisitu", periode_saat_ini, diformat=False),
        "jatinangor" : filter_channel_pembayaran("Crisbar Jatinangor", periode_saat_ini, diformat=False),
        "kopo" : filter_channel_pembayaran("Crisbar Kopo", periode_saat_ini, diformat=False),
        "metro" : filter_channel_pembayaran("Crisbar Metro Margahayu", periode_saat_ini, diformat=False),
        "sukabirus" : filter_channel_pembayaran("Crisbar Sukabirus", periode_saat_ini, diformat=False),
        "sukapura" : filter_channel_pembayaran("Crisbar Sukapura", periode_saat_ini, diformat=False),
        "sukajadi" : filter_channel_pembayaran("Crisbar Sukajadi", periode_saat_ini, diformat=False),
        "unjani" : filter_channel_pembayaran("Crisbar Unjani", periode_saat_ini, diformat=False),
    }

    query_kemarin = {
        "antapani" : filter_channel_pembayaran("Crisbar Antapani", periode_saat_ini-1, diformat=False, kemarin=True),
        "cisitu" : filter_channel_pembayaran("Crisbar Cisitu", periode_saat_ini-1, diformat=False, kemarin=True),
        "jatinangor" : filter_channel_pembayaran("Crisbar Jatinangor", periode_saat_ini-1, diformat=False, kemarin=True),
        "kopo" : filter_channel_pembayaran("Crisbar Kopo", periode_saat_ini-1, diformat=False, kemarin=True),
        "metro" : filter_channel_pembayaran("Crisbar Metro Margahayu", periode_saat_ini-1, diformat=False, kemarin=True),
        "sukabirus" : filter_channel_pembayaran("Crisbar Sukabirus", periode_saat_ini-1, diformat=False, kemarin=True),
        "sukapura" : filter_channel_pembayaran("Crisbar Sukapura", periode_saat_ini-1, diformat=False, kemarin=True),
        "sukajadi" : filter_channel_pembayaran("Crisbar Sukajadi", periode_saat_ini-1, diformat=False, kemarin=True),
        "unjani" : filter_channel_pembayaran("Crisbar Unjani", periode_saat_ini-1, diformat=False, kemarin=True),
    }
    
    selisih = {
        "antapani" : [format_rupiah(query_sekarang["antapani"][a] - query_kemarin["antapani"][a]) for a in range(len(query_kemarin["antapani"]))],
        "cisitu" : [format_rupiah(query_sekarang["cisitu"][a] - query_kemarin["cisitu"][a]) for a in range(len(query_kemarin["cisitu"]))],
        "jatinangor" : [format_rupiah(query_sekarang["jatinangor"][a] - query_kemarin["jatinangor"][a]) for a in range(len(query_kemarin["jatinangor"]))],
        "kopo" : [format_rupiah(query_sekarang["kopo"][a] - query_kemarin["kopo"][a]) for a in range(len(query_kemarin["kopo"]))],
        "metro" : [format_rupiah(query_sekarang["metro"][a] - query_kemarin["metro"][a]) for a in range(len(query_kemarin["metro"]))],
        "sukabirus" : [format_rupiah(query_sekarang["sukabirus"][a] - query_kemarin["sukabirus"][a]) for a in range(len(query_kemarin["sukabirus"]))],
        "sukapura" : [format_rupiah(query_sekarang["sukapura"][a] - query_kemarin["sukapura"][a]) for a in range(len(query_kemarin["sukapura"]))],
        "sukajadi" : [format_rupiah(query_sekarang["sukajadi"][a] - query_kemarin["sukajadi"][a]) for a in range(len(query_kemarin["sukajadi"]))],
        "unjani" : [format_rupiah(query_sekarang["unjani"][a] - query_kemarin["unjani"][a]) for a in range(len(query_kemarin["unjani"]))]
    }

    # GO FOOD, GRABFOOD, SHOPEE FOOD, DINE IN TAKEAWAY
    querynya = [
        ["Crisbar Antapani", (query_sekarang_diformat['antapani'][0], selisih['antapani'][0]), (query_sekarang_diformat['antapani'][1], selisih['antapani'][1]), (query_sekarang_diformat['antapani'][2], selisih['antapani'][2]), (query_sekarang_diformat['antapani'][3], selisih['antapani'][3])],
        ["Crisbar Cisitu", (query_sekarang_diformat['cisitu'][0], selisih['cisitu'][0]), (query_sekarang_diformat['cisitu'][1], selisih['cisitu'][1]), (query_sekarang_diformat['cisitu'][2], selisih['cisitu'][2]), (query_sekarang_diformat['cisitu'][3], selisih['cisitu'][3])],
        ["Crisbar Jatinangor", (query_sekarang_diformat['jatinangor'][0], selisih['jatinangor'][0]), (query_sekarang_diformat['jatinangor'][1], selisih['jatinangor'][1]), (query_sekarang_diformat['jatinangor'][2], selisih['jatinangor'][2]), (query_sekarang_diformat['jatinangor'][3], selisih['jatinangor'][3])],
        ["Crisbar Taman Kopo Indah", (query_sekarang_diformat['kopo'][0], selisih['kopo'][0]), (query_sekarang_diformat['kopo'][1], selisih['kopo'][1]), (query_sekarang_diformat['kopo'][2], selisih['kopo'][2]), (query_sekarang_diformat['kopo'][3], selisih['kopo'][3])],
        ["Crisbar Metro Margahayu", (query_sekarang_diformat['metro'][0], selisih['metro'][0]), (query_sekarang_diformat['metro'][1], selisih['metro'][1]), (query_sekarang_diformat['metro'][2], selisih['metro'][2]), (query_sekarang_diformat['metro'][3], selisih['metro'][3])],
        ["Crisbar Sukabirus", (query_sekarang_diformat['sukabirus'][0], selisih['sukabirus'][0]), (query_sekarang_diformat['sukabirus'][1], selisih['sukabirus'][1]), (query_sekarang_diformat['sukabirus'][2], selisih['sukabirus'][2]), (query_sekarang_diformat['sukabirus'][3], selisih['sukabirus'][3])],
        ["Crisbar Sukapura", (query_sekarang_diformat['sukapura'][0], selisih['sukapura'][0]), (query_sekarang_diformat['sukapura'][1], selisih['sukapura'][1]), (query_sekarang_diformat['sukapura'][2], selisih['sukapura'][2]), (query_sekarang_diformat['sukapura'][3], selisih['sukapura'][3])],
        ["Crisbar Sukajadi", (query_sekarang_diformat['sukajadi'][0], selisih['sukajadi'][0]), (query_sekarang_diformat['sukajadi'][1], selisih['sukajadi'][1]), (query_sekarang_diformat['sukajadi'][2], selisih['sukajadi'][2]), (query_sekarang_diformat['sukajadi'][3], selisih['sukajadi'][3])],
        ["Crisbar Unjani", (query_sekarang_diformat['unjani'][0], selisih['unjani'][0]), (query_sekarang_diformat['unjani'][1], selisih['unjani'][1]), (query_sekarang_diformat['unjani'][2], selisih['unjani'][2]), (query_sekarang_diformat['unjani'][3], selisih['unjani'][3])],
    ]

    return querynya

def filter_channel_pembayaran(cabang, periode, diformat=True, kemarin=False):

    channel_dine_in_takeaway = ["Kredit Bank Lain","Debit Bank Lain","Kredit BRI","Debit BRI","QR BRI","BCA","SHOPEE PAY","OVO","GOPAY","Cash"]

    gofood = rata_rata_sales(filter_sales(cabang, "GO FOOD", periode, kemarin), diformat)
    grabfood = rata_rata_sales(filter_sales(cabang, "GRAB FOOD", periode, kemarin), diformat)
    shopeefood = rata_rata_sales(filter_sales(cabang, "SHOPEE FOOD", periode, kemarin), diformat)
    dinein_takeaway = rata_rata_sales(filter_sales(cabang, channel_dine_in_takeaway, periode, kemarin), diformat)

    return [gofood, grabfood, shopeefood, dinein_takeaway]


def filter_sales(cabang, channel_pembayaran, periode, kemarin):

    periodenya = PeriodeKerja.objects.get(pk=periode)
    # periodenya.awal_periode
    awal_periode = datetime(periodenya.awal_periode.year, periodenya.awal_periode.month, periodenya.awal_periode.day, 8, 0, 0, tzinfo=pytz.UTC) - timedelta(hours=7)
    akhir_periode = datetime(periodenya.akhir_periode.year, periodenya.akhir_periode.month, periodenya.akhir_periode.day, 23, 59, 59, tzinfo=pytz.UTC) - timedelta(hours=7)

    if isinstance(channel_pembayaran, list):
        ds = DataStruk.objects.filter(store_id = cabang, payments__in = channel_pembayaran, created_at__range=[awal_periode, akhir_periode])
    else:
        ds = DataStruk.objects.filter(store_id = cabang, payments = channel_pembayaran, created_at__range=[awal_periode, akhir_periode])

    if not kemarin:
        akhir_periode = pytz.utc.localize(datetime.utcnow())

    selisih_hari = akhir_periode - awal_periode
    selisih_hari = selisih_hari.days

    if selisih_hari == 0:
        selisih_hari = 1

    return ds, selisih_hari

def rata_rata_sales(filter_sales, diformat = False):

    salesnya = filter_sales[0]
    selisih_hari = filter_sales[1]

    # ambil total sales
    total_sales = 0
    for s in salesnya:
        if s.receipt_type == 'REFUND':
            total_sales -= s.total_money_filter()
        else:
            total_sales += s.total_money_filter()

    # rata-rata = total sales / banyak sales
    if total_sales == 0:
        rata_rata = 0
    else:
        rata_rata = total_sales / selisih_hari

    if diformat:
        return format_rupiah(rata_rata)
    else:
        return rata_rata


def format_rupiah(angka, total_penjualan = False):

    angka = int(angka)
    if angka < 0:
        minus = True
        angka = angka * -1
    else:
        minus = False

    if angka >= 1_000_000_000:
        milyaran = angka // 1_000_000_000
        angka = angka - (milyaran*1_000_000_000)
        ratusan_juta = angka // 100_000_000
        angka = angka - (ratusan_juta*100_000_000)
        puluhan_juta = angka // 10_000_000
        angka = angka - (puluhan_juta*10_000_000)
        juta = angka // 1_000_000
        angka = angka - (juta*1_000_000)
        ratusan_ribu = angka // 100_000
        angka = angka - (ratusan_ribu*100_000)
        puluhan_ribu = angka // 10_000
        angka = angka - (puluhan_ribu * 10_000)
        ribu = angka // 1000
        angka = angka - (ribu*1000)
        ratusan = angka // 100
        angka = angka - (ratusan*100)
        puluhan = angka // 10
        angka = angka - (puluhan*10)   

        # print("milyaran rupiah")
        if total_penjualan:
            hasil = "Rp " + str(milyaran) + "." + str(ratusan_juta) + str(puluhan_juta) + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            if minus:
                return "-" + hasil[:7] + "m"
            else:
                return hasil[:7] + "m"
        else:
            if minus:
                return "-" + "Rp " + str(milyaran) + "." + str(ratusan_juta) + str(puluhan_juta) + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            else:
                return "Rp " + str(milyaran) + "." + str(ratusan_juta) + str(puluhan_juta) + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            
        
    elif angka >= 100_000_000:
        ratusan_juta = angka // 100_000_000
        angka = angka - (ratusan_juta*100_000_000)
        puluhan_juta = angka // 10_000_000
        angka = angka - (puluhan_juta*10_000_000)
        juta = angka // 1_000_000
        angka = angka - (juta*1_000_000)
        ratusan_ribu = angka // 100_000
        angka = angka - (ratusan_ribu*100_000)
        puluhan_ribu = angka // 10_000
        angka = angka - (puluhan_ribu * 10_000)
        ribu = angka // 1000
        angka = angka - (ribu*1000)
        ratusan = angka // 100
        angka = angka - (ratusan*100)
        puluhan = angka // 10
        angka = angka - (puluhan*10)

        # print("jutaan rupiah")
        if total_penjualan:
            hasil = "Rp " + str(ratusan_juta) + str(puluhan_juta) + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            if minus:
                return "-" + hasil[:9] + "jt"
            else:
                return hasil[:9] + "jt"
        else:
            if minus:
                return "-" + "Rp " + str(ratusan_juta) + str(puluhan_juta) + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            else:
                return "Rp " + str(ratusan_juta) + str(puluhan_juta) + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
        
    elif angka >= 10_000_000:    
        puluhan_juta = angka // 10_000_000
        angka = angka - (puluhan_juta*10_000_000)
        juta = angka // 1_000_000
        angka = angka - (juta*1_000_000)
        ratusan_ribu = angka // 100_000
        angka = angka - (ratusan_ribu*100_000)
        puluhan_ribu = angka // 10_000
        angka = angka - (puluhan_ribu * 10_000)
        ribu = angka // 1000
        angka = angka - (ribu*1000)
        ratusan = angka // 100
        angka = angka - (ratusan*100)
        puluhan = angka // 10
        angka = angka - (puluhan*10)

        # print("puluhan juta rupiah")
        if total_penjualan:
            hasil = "Rp " + str(puluhan_juta) + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            if minus:
                return "-" + hasil[:7] + "jt"
            else:
                return hasil[:7] + "jt"
        else:
            if minus:
                return "-" + "Rp " + str(puluhan_juta) + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            else:
                return "Rp " + str(puluhan_juta) + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
    
    elif angka >= 1_000_000:

        juta = angka // 1_000_000
        angka = angka - (juta*1_000_000)
        ratusan_ribu = angka // 100_000
        angka = angka - (ratusan_ribu*100_000)
        puluhan_ribu = angka // 10_000
        angka = angka - (puluhan_ribu * 10_000)
        ribu = angka // 1000
        angka = angka - (ribu*1000)
        ratusan = angka // 100
        angka = angka - (ratusan*100)
        puluhan = angka // 10
        angka = angka - (puluhan*10)
        
        if total_penjualan:
            hasil = "Rp " + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            if minus:
                return "-" + hasil[:6] + "jt"
            else:
                return hasil[:6] + "jt"
        else:
            if minus:
                return "-" + "Rp " + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            else:
                return "Rp " + str(juta) + "." + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            
    elif angka >= 100_000:
        ratusan_ribu = angka // 100_000
        angka = angka - (ratusan_ribu*100_000)
        puluhan_ribu = angka // 10_000
        angka = angka - (puluhan_ribu * 10_000)
        ribu = angka // 1000
        angka = angka - (ribu*1000)
        ratusan = angka // 100
        angka = angka - (ratusan*100)
        puluhan = angka // 10
        angka = angka - (puluhan*10)
        
        # print("ratusan ribu rupiah")
        if total_penjualan:
            hasil = "Rp " + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            if minus:
                return "-" + hasil[:8] + "rb"
            else:
                return hasil[:8] + "rb"
        else:
            if minus:
                return "-" + "Rp " + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            else:
                return "Rp " + str(ratusan_ribu) + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            
    elif angka >= 10_000:
        
        puluhan_ribu = angka // 10_000
        angka = angka - (puluhan_ribu * 10_000)
        ribu = angka // 1000
        angka = angka - (ribu*1000)
        ratusan = angka // 100
        angka = angka - (ratusan*100)
        puluhan = angka // 10
        angka = angka - (puluhan*10)
        
        # print("puluhan ribu rupiah")
        if total_penjualan:
            hasil = "Rp " + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            if minus:
                return "-" + hasil[:7] + "rb"
            else:
                return hasil[:7] + "rb"
        else:
            if minus:
                return "-" + "Rp " + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            else:
                return "Rp " + str(puluhan_ribu) + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            
    elif angka >= 1_000:
        
        ribu = angka // 1000
        angka = angka - (ribu*1000)
        ratusan = angka // 100
        angka = angka - (ratusan*100)
        puluhan = angka // 10
        angka = angka - (puluhan*10)
        
        # print("ribuan rupiah")
        if total_penjualan:
            hasil = "Rp " + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            if minus:
                return "-" + hasil[:6] + "rb"
            else:
                return hasil[:6] + "rb"
        else:
            if minus:
                return "-" + "Rp " + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)
            else:
                return "Rp " + str(ribu) + "." + str(ratusan) + str(puluhan) + str(angka)

    elif angka >= 100:
        ratusan = angka // 100
        angka = angka - (ratusan*100)
        puluhan = angka // 10
        angka = angka - (puluhan*10)
        
        # print("ribuan rupiah")
        if minus:
            return "-" + "Rp " + str(ratusan) + str(puluhan) + str(angka)
        else:
            return "Rp " + str(ratusan) + str(puluhan) + str(angka)

    elif angka >= 10:
        puluhan = angka // 10
        angka = angka - (puluhan*10)
        
        # print("ribuan rupiah")
        if minus:
            return "-" + "Rp " + str(puluhan) + str(angka)
        else:
            return "Rp " + str(puluhan) + str(angka)

    else:
        # print("satuan rupiah")
        if minus:
            return "-" + "Rp " + str(angka)
        else:
            return "Rp " + str(angka)
