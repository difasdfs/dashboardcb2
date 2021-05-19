from rm_app.models import ProduksiAyam, Cabang
from datetime import date
from django.utils import timezone

def query_rm_app(tanggalnya):
    # bikin kodingan bagaimana apabila tidak ada cabang
    cabangnya = Cabang.objects.all()

    querynya = []

    for a in cabangnya:
        produksi_ayam = ProduksiAyam.objects.filter(cabang=a, tanggal=tanggalnya)
        
        # jika produksi ayam tidak ada
        if not produksi_ayam:
            bikin_tanggal_yang_tidak_ada_produksi(a, tanggalnya)
        
        produksi_ayam = ProduksiAyam.objects.filter(cabang=a, tanggal=tanggalnya)[0]
        isi_tabelnya = isi_tabel(produksi_ayam)

        percabang = {
            'nama_cabang' : a.nama_cabang,
            'isi_tabelnya' : isi_tabelnya,
            'stok_ayam' : produksi_ayam.stok_ayam,
            'stok_chicken_skin' : produksi_ayam.stok_chicken_skin
        }
        querynya.append(percabang)
    
    return querynya
    # querynya = ProduksiAyam.objects.get(cabang=cabangnya)

# ---------------------- LOGIKA ----------------------
def bikin_tanggal_yang_tidak_ada_produksi(cabangnya, tanggalnya):
    p = ProduksiAyam(
        id_pelapor = 0,
        cabang = cabangnya,
        tanggal = tanggalnya,
        waktu_lapor = timezone.now()
    )
    p.save()

def isi_tabel(objek_produksi_ayam):
    a = objek_produksi_ayam
    querynya = [
        ["9:00", a.jam_9_ayam, a.jam_9_nasi, a.jam_9_teh, a.jam_9_milo, a.jam_9_orange, a.jam_9_lemontea],
        ["10:00", a.jam_10_ayam, a.jam_10_nasi, a.jam_10_teh, a.jam_10_milo, a.jam_10_orange, a.jam_10_lemontea],
        ["11:00", a.jam_11_ayam, a.jam_11_nasi, a.jam_11_teh, a.jam_11_milo, a.jam_11_orange, a.jam_11_lemontea],
        ["12:00", a.jam_12_ayam, a.jam_12_nasi, a.jam_12_teh, a.jam_12_milo, a.jam_12_orange, a.jam_12_lemontea],
        ["13:00", a.jam_13_ayam, a.jam_13_nasi, a.jam_13_teh, a.jam_13_milo, a.jam_13_orange, a.jam_13_lemontea],
        ["14:00", a.jam_14_ayam, a.jam_14_nasi, a.jam_14_teh, a.jam_14_milo, a.jam_14_orange, a.jam_14_lemontea],
        ["15:00", a.jam_15_ayam, a.jam_15_nasi, a.jam_15_teh, a.jam_15_milo, a.jam_15_orange, a.jam_15_lemontea],
        ["16:00", a.jam_16_ayam, a.jam_16_nasi, a.jam_16_teh, a.jam_16_milo, a.jam_16_orange, a.jam_16_lemontea],
        ["17:00", a.jam_17_ayam, a.jam_17_nasi, a.jam_17_teh, a.jam_17_milo, a.jam_17_orange, a.jam_17_lemontea],
        ["18:00", a.jam_18_ayam, a.jam_18_nasi, a.jam_18_teh, a.jam_18_milo, a.jam_18_orange, a.jam_18_lemontea],
        ["19:00", a.jam_19_ayam, a.jam_19_nasi, a.jam_19_teh, a.jam_19_milo, a.jam_19_orange, a.jam_19_lemontea],
        ["20:00", a.jam_20_ayam, a.jam_20_nasi, a.jam_20_teh, a.jam_20_milo, a.jam_20_orange, a.jam_20_lemontea],
        ["21:00", a.jam_21_ayam, a.jam_21_nasi, a.jam_21_teh, a.jam_21_milo, a.jam_21_orange, a.jam_21_lemontea],
        ["22:00", a.jam_22_ayam, a.jam_22_nasi, a.jam_22_teh, a.jam_22_milo, a.jam_22_orange, a.jam_22_lemontea],
        ["23:00", a.jam_23_ayam, a.jam_23_nasi, a.jam_23_teh, a.jam_23_milo, a.jam_23_orange, a.jam_23_lemontea],
        ["24:00", a.jam_24_ayam, a.jam_24_nasi, a.jam_24_teh, a.jam_24_milo, a.jam_24_orange, a.jam_24_lemontea],
    ]
    return querynya
