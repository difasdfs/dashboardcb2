from .models import Complaint, PeriodeKerja
from datetime import date

# id PeriodeKerja, dimulai dari 1 = Januari 2021

# OUTPUT
# [
#  { 
#   "nama bulan" : {
# 	    "cabang 1" : {"kualitas produk" : 40, "pelayanan" : 50, ...},
# 	    "cabang 2" : {"kualitas produk" : 40, "pelayanan" : 50, ...},
# 	   ...
#    }
#  },
# ]

def query_trend_pola_complaint():
    # id untuk data periode kerja tahun 2021
    id_periode_kerja = [a for a in range(1,13)]

    # object dari database periode kerja tahun ini
    periode_kerja_tahun_ini = [PeriodeKerja.objects.get(pk=b) for b in id_periode_kerja]

    # Nama cabang
    NAMA_CABANG = ["Antapani", "Cisitu", "Jatinangor", "Kopo", "Metro", "Sukapura", "Sukabirus", "Sukajadi", "Unjani"]

    # filter berdasarkan bulan dan nama cabang
    hasil = []
    for object_periode_kerja in periode_kerja_tahun_ini:

        awal = object_periode_kerja.awal_periode
        akhir = object_periode_kerja.akhir_periode

        if akhir >= date.today():
            continue
        
        dictionary_cabang_perbulan = {}
        for nama_cabang in NAMA_CABANG:
            komplain = Complaint.objects.filter(tanggal__range=[awal, akhir], cabang=nama_cabang)
            
            komplain_kualitas_produk = len(komplain.filter(jenis="Kualitas Produk"))
            komplain_kebersihan = len(komplain.filter(jenis="Kebersihan"))
            komplain_pelayanan = len(komplain.filter(jenis="Kualitas Produk"))
            komplain_tidak_lengkap = len(komplain.filter(jenis="Kualitas Produk"))
            komplain_total = komplain_kualitas_produk + komplain_kebersihan + komplain_pelayanan + komplain_tidak_lengkap
            
            dictionary_cabang_perbulan[nama_cabang] = {
                "kualitas_produk" : komplain_kualitas_produk,
                "kebersihan" : komplain_kebersihan,
                "pelayanan" : komplain_pelayanan,
                "tidak_lengkap" : komplain_tidak_lengkap,
                "total_komplain" : komplain_total
            }

        hasil.append( 
            {
                'periode' : object_periode_kerja.periode, 
                'data_komplain' : dictionary_cabang_perbulan
            }
        )
    
    return hasil