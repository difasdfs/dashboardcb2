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

def benerin_produksi():
    hari_produksi = HariProduksi.objects.all()
    for h in hari_produksi:
        h.antapani_9 = h.antapani_10
        h.antapani_10 = h.antapani_11
        h.antapani_11 = h.antapani_12
        h.antapani_12 = h.antapani_13
        h.antapani_13 = h.antapani_14
        h.antapani_14 = h.antapani_15
        h.antapani_15 = h.antapani_16
        h.antapani_16 = h.antapani_17
        h.antapani_17 = h.antapani_18
        h.antapani_18 = h.antapani_19
        h.antapani_19 = h.antapani_20
        h.antapani_20 = h.antapani_21
        h.antapani_21 = h.antapani_22
        h.antapani_22 = h.antapani_23
        h.antapani_23 = h.antapani_24
        h.antapani_24 = h.antapani_1
        h.antapani_1 = h.antapani_2
        h.antapani_2 = h.antapani_3
        h.antapani_3 = 0
        h.jatinangor_9 = h.jatinangor_10
        h.jatinangor_10 = h.jatinangor_11
        h.jatinangor_11 = h.jatinangor_12
        h.jatinangor_12 = h.jatinangor_13
        h.jatinangor_13 = h.jatinangor_14
        h.jatinangor_14 = h.jatinangor_15
        h.jatinangor_15 = h.jatinangor_16
        h.jatinangor_16 = h.jatinangor_17
        h.jatinangor_17 = h.jatinangor_18
        h.jatinangor_18 = h.jatinangor_19
        h.jatinangor_19 = h.jatinangor_20
        h.jatinangor_20 = h.jatinangor_21
        h.jatinangor_21 = h.jatinangor_22
        h.jatinangor_22 = h.jatinangor_23
        h.jatinangor_23 = h.jatinangor_24
        h.jatinangor_24 = h.jatinangor_1
        h.jatinangor_1 = h.jatinangor_2
        h.jatinangor_2 = h.jatinangor_3
        h.jatinangor_3 = 0
        h.metro_9 = h.metro_10
        h.metro_10 = h.metro_11
        h.metro_11 = h.metro_12
        h.metro_12 = h.metro_13
        h.metro_13 = h.metro_14
        h.metro_14 = h.metro_15
        h.metro_15 = h.metro_16
        h.metro_16 = h.metro_17
        h.metro_17 = h.metro_18
        h.metro_18 = h.metro_19
        h.metro_19 = h.metro_20
        h.metro_20 = h.metro_21
        h.metro_21 = h.metro_22
        h.metro_22 = h.metro_23
        h.metro_23 = h.metro_24
        h.metro_24 = h.metro_1
        h.metro_1 = h.metro_2
        h.metro_2 = h.metro_3
        h.metro_3 = 0
        h.sukapura_9 = h.sukapura_10
        h.sukapura_10 = h.sukapura_11
        h.sukapura_11 = h.sukapura_12
        h.sukapura_12 = h.sukapura_13
        h.sukapura_13 = h.sukapura_14
        h.sukapura_14 = h.sukapura_15
        h.sukapura_15 = h.sukapura_16
        h.sukapura_16 = h.sukapura_17
        h.sukapura_17 = h.sukapura_18
        h.sukapura_18 = h.sukapura_19
        h.sukapura_19 = h.sukapura_20
        h.sukapura_20 = h.sukapura_21
        h.sukapura_21 = h.sukapura_22
        h.sukapura_22 = h.sukapura_23
        h.sukapura_23 = h.sukapura_24
        h.sukapura_24 = h.sukapura_1
        h.sukapura_1 = h.sukapura_2
        h.sukapura_2 = h.sukapura_3
        h.sukapura_3 = 0
        h.sukabirus_9 = h.sukabirus_10
        h.sukabirus_10 = h.sukabirus_11
        h.sukabirus_11 = h.sukabirus_12
        h.sukabirus_12 = h.sukabirus_13
        h.sukabirus_13 = h.sukabirus_14
        h.sukabirus_14 = h.sukabirus_15
        h.sukabirus_15 = h.sukabirus_16
        h.sukabirus_16 = h.sukabirus_17
        h.sukabirus_17 = h.sukabirus_18
        h.sukabirus_18 = h.sukabirus_19
        h.sukabirus_19 = h.sukabirus_20
        h.sukabirus_20 = h.sukabirus_21
        h.sukabirus_21 = h.sukabirus_22
        h.sukabirus_22 = h.sukabirus_23
        h.sukabirus_23 = h.sukabirus_24
        h.sukabirus_24 = h.sukabirus_1
        h.sukabirus_1 = h.sukabirus_2
        h.sukabirus_2 = h.sukabirus_3
        h.sukabirus_3 = 0
        h.unjani_9 = h.unjani_10
        h.unjani_10 = h.unjani_11
        h.unjani_11 = h.unjani_12
        h.unjani_12 = h.unjani_13
        h.unjani_13 = h.unjani_14
        h.unjani_14 = h.unjani_15
        h.unjani_15 = h.unjani_16
        h.unjani_16 = h.unjani_17
        h.unjani_17 = h.unjani_18
        h.unjani_18 = h.unjani_19
        h.unjani_19 = h.unjani_20
        h.unjani_20 = h.unjani_21
        h.unjani_21 = h.unjani_22
        h.unjani_22 = h.unjani_23
        h.unjani_23 = h.unjani_24
        h.unjani_24 = h.unjani_1
        h.unjani_1 = h.unjani_2
        h.unjani_2 = h.unjani_3
        h.unjani_3 = 0
        h.cisitu_9 = h.cisitu_10
        h.cisitu_10 = h.cisitu_11
        h.cisitu_11 = h.cisitu_12
        h.cisitu_12 = h.cisitu_13
        h.cisitu_13 = h.cisitu_14
        h.cisitu_14 = h.cisitu_15
        h.cisitu_15 = h.cisitu_16
        h.cisitu_16 = h.cisitu_17
        h.cisitu_17 = h.cisitu_18
        h.cisitu_18 = h.cisitu_19
        h.cisitu_19 = h.cisitu_20
        h.cisitu_20 = h.cisitu_21
        h.cisitu_21 = h.cisitu_22
        h.cisitu_22 = h.cisitu_23
        h.cisitu_23 = h.cisitu_24
        h.cisitu_24 = h.cisitu_1
        h.cisitu_1 = h.cisitu_2
        h.cisitu_2 = h.cisitu_3
        h.cisitu_3 = 0
        h.sukajadi_9 = h.sukajadi_10
        h.sukajadi_10 = h.sukajadi_11
        h.sukajadi_11 = h.sukajadi_12
        h.sukajadi_12 = h.sukajadi_13
        h.sukajadi_13 = h.sukajadi_14
        h.sukajadi_14 = h.sukajadi_15
        h.sukajadi_15 = h.sukajadi_16
        h.sukajadi_16 = h.sukajadi_17
        h.sukajadi_17 = h.sukajadi_18
        h.sukajadi_18 = h.sukajadi_19
        h.sukajadi_19 = h.sukajadi_20
        h.sukajadi_20 = h.sukajadi_21
        h.sukajadi_21 = h.sukajadi_22
        h.sukajadi_22 = h.sukajadi_23
        h.sukajadi_23 = h.sukajadi_24
        h.sukajadi_24 = h.sukajadi_1
        h.sukajadi_1 = h.sukajadi_2
        h.sukajadi_2 = h.sukajadi_3
        h.sukajadi_3 = 0
        h.save()
        

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