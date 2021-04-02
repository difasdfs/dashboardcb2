from dashboard.models import DataStruk, PeriodeKerja, OmsetBulan
from datetime import datetime, date, timedelta
import pytz

def masukin_database():
    # EDIT YANG DI BAWAH INI AJA
    nama_file = ["struk_desember_kurang.csv"]
    # ----------------------------------------
    # JANGAN DIEDIT!
    for namafile in nama_file:
        file = open(namafile)
        baris = [i for i in file.readlines()]
        baris.reverse()
        for isi in baris[:-1]:
            isi = isi.split(';')
            tanggal_waktu = isi[0].split()
            tanggal_bulan_tahun = tanggal_waktu[0].split("/")
            jam_menit = tanggal_waktu[1].split('.')
            waktustruk = datetime(int(tanggal_bulan_tahun[2]), int(tanggal_bulan_tahun[1]), int(tanggal_bulan_tahun[0]), int(jam_menit[0]), int(jam_menit[1]), tzinfo=pytz.UTC)
            d = DataStruk(nomor_struk=isi[1], created_at=waktustruk, outlet=isi[5], nama_pembayaran=isi[4], tipe_struk=isi[2], money_amount=int(isi[3]))
            d.save()
            print(waktustruk)

def bikin_periode_kerja():
    nama_periode = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    pertambahan = [31, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30]
    pertambahan_akhir = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    tahun = "2021"
    awal_periode = date(2020, 12, 26)
    akhir_periode = date(2021, 1, 25)
    i = 0
    for nama in nama_periode:
        p = PeriodeKerja(periode=nama + " " + tahun, awal_periode=awal_periode, akhir_periode=akhir_periode)
        p.save()
        print(nama + " " + tahun)
        print(awal_periode)
        print(akhir_periode)
        awal_periode += timedelta(days=pertambahan[i])
        akhir_periode += timedelta(days=pertambahan_akhir[i])
        i += 1

def buat_omset_bulan():
    pk = PeriodeKerja.objects.all() # idnya dari kecil ke gede kalau di iterate
    i = 0
    for p in pk:
        ob = OmsetBulan(periode=p, omset_bulan_ini=0, omset_bulan_sebelumnya=0, target_omset=0)
        ob.hitung_omset_bulan()	
        if i == 0:
            i+=1
            continue
        ob.dapatkan_omset_bulan_sebelumnya()