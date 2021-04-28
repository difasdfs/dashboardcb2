from datetime import date, timedelta
from dashboard.models import PemakaianAyam
from dashboard.supply_chain import eksekusi_struk_sehari

def fungsinya():
    awal = date(2021, 1, 1)
    akhir = date.today() - timedelta(days=1)

    selisih = akhir - awal
    banyak_hari = selisih.days

    for i in range(banyak_hari+1):

        p = PemakaianAyam(
            tanggal = awal,
            pemakaian_ayam = 0,
            pemakaian_ayam_antapani = 0,
            pemakaian_ayam_jatinangor = 0,
            pemakaian_ayam_metro = 0,
            pemakaian_ayam_sukapura = 0,
            pemakaian_ayam_sukabirus = 0,
            pemakaian_ayam_unjani = 0,
            pemakaian_ayam_cisitu = 0,
            pemakaian_ayam_sukajadi = 0,
            dieksekusi = False
        )
        p.save()

        awal += timedelta(days=1)


def hitung_pemakaian_ayam_api():
    pemakaian_ayam = PemakaianAyam.objects.all()

    for p in pemakaian_ayam:
        tanggal = p.tanggal
        print("Tanggal " + str(tanggal) + " sedang dieksekusi")
        eksekusi_struk_sehari(tanggal)
        print("Tanggal " + str(tanggal) + " telah dieksekusi")
        print()


# print(banyak_hari)