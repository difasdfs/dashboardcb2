from datetime import date, timedelta
from dashboard.models import PemakaianAyam, HariProduksi
from dashboard.supply_chain import eksekusi_struk_sehari
from dashboard.operation import eksekusi

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

def eksekusi_produksi_harian():
    awal = date(2021, 1, 1)
    akhir = date(2021, 4, 12)

    selisih = akhir - awal
    banyak_hari = selisih.days

    for i in range(banyak_hari+1):
        print("Tanggal " + str(awal) + " sedang dieksekusi")
        eksekusi(awal)
        print("Tanggal " + str(awal) + " telah dieksekusi")
        print()
        awal += timedelta(days=1)

    awal = date(2021, 3, 13)
    akhir = date.today() - timedelta(days=1)

    selisih = akhir - awal
    banyak_hari = selisih.days

    for i in range(banyak_hari+1):
        print("Tanggal " + str(awal) + " sedang dieksekusi")
        eksekusi(awal, puasa=True)
        print("Tanggal " + str(awal) + " telah dieksekusi")
        print()
        awal += timedelta(days=1)

def bikin_produksi_harian():
    awal = date(2021, 1, 1)
    akhir = date.today() - timedelta(days=1)

    selisih = akhir - awal
    banyak_hari = selisih.days

    for i in range(banyak_hari+1):

        p = HariProduksi(
            hari = awal,
            antapani_9 = 0,
            antapani_10 = 0,
            antapani_11 = 0,
            antapani_12 = 0,
            antapani_13 = 0,
            antapani_14 = 0,
            antapani_15 = 0,
            antapani_16 = 0,
            antapani_17 = 0,
            antapani_18 = 0,
            antapani_19 = 0,
            antapani_20 = 0,
            antapani_21 = 0,
            antapani_22 = 0,
            antapani_23 = 0,
            antapani_24 = 0,
            antapani_1 = 0,
            antapani_2 = 0,
            antapani_3 = 0,
            jatinangor_9 = 0,
            jatinangor_10 = 0,
            jatinangor_11 = 0,
            jatinangor_12 = 0,
            jatinangor_13 = 0,
            jatinangor_14 = 0,
            jatinangor_15 = 0,
            jatinangor_16 = 0,
            jatinangor_17 = 0,
            jatinangor_18 = 0,
            jatinangor_19 = 0,
            jatinangor_20 = 0,
            jatinangor_21 = 0,
            jatinangor_22 = 0,
            jatinangor_23 = 0,
            jatinangor_24 = 0,
            jatinangor_1 = 0,
            jatinangor_2 = 0,
            jatinangor_3 = 0,
            metro_9 = 0,
            metro_10 = 0,
            metro_11 = 0,
            metro_12 = 0,
            metro_13 = 0,
            metro_14 = 0,
            metro_15 = 0,
            metro_16 = 0,
            metro_17 = 0,
            metro_18 = 0,
            metro_19 = 0,
            metro_20 = 0,
            metro_21 = 0,
            metro_22 = 0,
            metro_23 = 0,
            metro_24 = 0,
            metro_1 = 0,
            metro_2 = 0,
            metro_3 = 0,
            sukapura_9 = 0,
            sukapura_10 = 0,
            sukapura_11 = 0,
            sukapura_12 = 0,
            sukapura_13 = 0,
            sukapura_14 = 0,
            sukapura_15 = 0,
            sukapura_16 = 0,
            sukapura_17 = 0,
            sukapura_18 = 0,
            sukapura_19 = 0,
            sukapura_20 = 0,
            sukapura_21 = 0,
            sukapura_22 = 0,
            sukapura_23 = 0,
            sukapura_24 = 0,
            sukapura_1 = 0,
            sukapura_2 = 0,
            sukapura_3 = 0,
            sukabirus_9 = 0,
            sukabirus_10 = 0,
            sukabirus_11 = 0,
            sukabirus_12 = 0,
            sukabirus_13 = 0,
            sukabirus_14 = 0,
            sukabirus_15 = 0,
            sukabirus_16 = 0,
            sukabirus_17 = 0,
            sukabirus_18 = 0,
            sukabirus_19 = 0,
            sukabirus_20 = 0,
            sukabirus_21 = 0,
            sukabirus_22 = 0,
            sukabirus_23 = 0,
            sukabirus_24 = 0,
            sukabirus_1 = 0,
            sukabirus_2 = 0,
            sukabirus_3 = 0,
            unjani_9 = 0,
            unjani_10 = 0,
            unjani_11 = 0,
            unjani_12 = 0,
            unjani_13 = 0,
            unjani_14 = 0,
            unjani_15 = 0,
            unjani_16 = 0,
            unjani_17 = 0,
            unjani_18 = 0,
            unjani_19 = 0,
            unjani_20 = 0,
            unjani_21 = 0,
            unjani_22 = 0,
            unjani_23 = 0,
            unjani_24 = 0,
            unjani_1 = 0,
            unjani_2 = 0,
            unjani_3 = 0,
            cisitu_9 = 0,
            cisitu_10 = 0,
            cisitu_11 = 0,
            cisitu_12 = 0,
            cisitu_13 = 0,
            cisitu_14 = 0,
            cisitu_15 = 0,
            cisitu_16 = 0,
            cisitu_17 = 0,
            cisitu_18 = 0,
            cisitu_19 = 0,
            cisitu_20 = 0,
            cisitu_21 = 0,
            cisitu_22 = 0,
            cisitu_23 = 0,
            cisitu_24 = 0,
            cisitu_1 = 0,
            cisitu_2 = 0,
            cisitu_3 = 0,
            sukajadi_9 = 0,
            sukajadi_10 = 0,
            sukajadi_11 = 0,
            sukajadi_12 = 0,
            sukajadi_13 = 0,
            sukajadi_14 = 0,
            sukajadi_15 = 0,
            sukajadi_16 = 0,
            sukajadi_17 = 0,
            sukajadi_18 = 0,
            sukajadi_19 = 0,
            sukajadi_20 = 0,
            sukajadi_21 = 0,
            sukajadi_22 = 0,
            sukajadi_23 = 0,
            sukajadi_24 = 0,
            sukajadi_1 = 0,
            sukajadi_2 = 0,
            sukajadi_3 = 0,
            dieksekusi = False
        )
        p.save()

        awal += timedelta(days=1)
# print(banyak_hari)