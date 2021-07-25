from .models import DataStruk
from dashboard.models import PeriodeKerja
from datetime import datetime, timedelta

import pytz
import math

def main(PERIODE):
    cabang = ['Crisbar Antapani','Crisbar Cisitu','Crisbar Jatinangor','Crisbar Kopo','Crisbar Metro Margahayu','Crisbar Sukabirus','Crisbar Sukapura','Crisbar Sukajadi','Crisbar Unjani',]

    querynya = []

    for c in cabang:
        sekarang = query_percabang(c, PERIODE)
        lalu = query_percabang(c, PERIODE-1, periode_lalu=True)
        selisih = selisih_list(lalu, sekarang)
        querynya.append(
            [
                c,
                (sekarang[0], selisih[0]),
                (sekarang[1], selisih[1]),
                (sekarang[2], selisih[2]),
                (sekarang[3], selisih[3]),
            ]
        )

    return querynya

def query_percabang(cabang, periode, periode_lalu = False):

    channel_dine_in_takeaway = ["Kredit Bank Lain","Debit Bank Lain","Kredit BRI","Debit BRI","QR BRI","BCA","SHOPEE PAY","OVO","GOPAY","Cash"]

    gofood = hitung_perchannel(cabang, "GO FOOD", awal_akhir(periode, periode_lalu))
    grabfood = hitung_perchannel(cabang, "GRAB FOOD", awal_akhir(periode, periode_lalu))
    shopeefood = hitung_perchannel(cabang, "SHOPEE FOOD", awal_akhir(periode, periode_lalu))
    dinein_takeaway = hitung_perchannel(cabang, channel_dine_in_takeaway, awal_akhir(periode, periode_lalu))

    return [dinein_takeaway, gofood, grabfood, shopeefood]

def selisih_list(list1, list2):
    hasil = [format_string(list2[a] - list1[a]) for a in range(len(list1))]
    return hasil

def format_string(angka):
    if angka > 0:
        hasil = "+" + str(angka)
    else:
        hasil = str(angka)
    return hasil

def hitung_perchannel(cabang, channel_pembayaran, rentang):

    if isinstance(channel_pembayaran, list):
        ds = DataStruk.objects.filter(store_id=cabang, created_at__range=[rentang['awal'], rentang['akhir']], payments__in=channel_pembayaran)
    else:
        ds = DataStruk.objects.filter(store_id=cabang, created_at__range=[rentang['awal'], rentang['akhir']], payments=channel_pembayaran)
    
    
    banyaknya_struk = len(ds)
    banyak_hari = rentang['selisih_hari']

    try:
        tren_pelanggan = math.ceil( banyaknya_struk / banyak_hari )
    except:
        tren_pelanggan = 0
    
    return tren_pelanggan

def awal_akhir(periode, periode_lalu):
    p = PeriodeKerja.objects.get(pk=periode)
    awal_periode = datetime(p.awal_periode.year, p.awal_periode.month, p.awal_periode.day, 8, 0, 0, tzinfo=pytz.UTC) - timedelta(hours=7)
    
    if periode_lalu:
        akhir_periode = datetime(p.akhir_periode.year, p.akhir_periode.month, p.akhir_periode.day, 23, 59, 59, tzinfo=pytz.UTC) - timedelta(hours=7)
    else:
        akhir_periode = pytz.utc.localize(datetime.utcnow())

    selisih = akhir_periode - awal_periode

    return {'awal' : awal_periode, 'akhir' : akhir_periode, 'selisih_hari' : selisih.days}

# ------------------ BOX QUERY PELANGGAN ------------------ 

def box_tren_pelanggan(periode):
    
    periode_ini = hitung_tren_box(awal_akhir(periode, periode_lalu=False))
    periode_lalu = hitung_tren_box(awal_akhir(periode-1, periode_lalu=True))
    kenaikan_penurunan = format_string(periode_ini - periode_lalu)

    return {'periode_ini' : periode_ini, 'periode_lalu' : periode_lalu, 'kenaikan_penurunan' : kenaikan_penurunan}

def hitung_tren_box(rentang):
    ds = DataStruk.objects.filter(created_at__range=[rentang['awal'], rentang['akhir']])
    selisih_hari = rentang['selisih_hari']

    try:
        rata_rata_tren = math.ceil(len(ds) / selisih_hari)
    except:
        rata_rata_tren = 0

    return rata_rata_tren
