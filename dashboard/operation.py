from .models import HariProduksi, AssemblyProduct
from datetime import datetime, timedelta, date
import statistics as stat
import pytz
import requests
import json

rumus_id_outlet = {
        'dc2497ed-963e-42ff-96a2-aeb7a8b65668' : 'Crisbar Metro Margahayu',
        'f0567abc-86a2-4f85-b027-82947b0a3983' : 'Crisbar Antapani',
        'fad4f949-711d-11ea-8d93-0603130a05b8' : 'Crisbar Sukabirus',
        'faa54a24-711d-11ea-8d93-0603130a05b8' : 'Crisbar Sukapura',
        'faa54a0c-711d-11ea-8d93-0603130a05b8' : 'Crisbar Sukajadi',
        'faa549f4-711d-11ea-8d93-0603130a05b8' : 'Crisbar Jatinangor',
        'faa545eb-711d-11ea-8d93-0603130a05b8' : 'Crisbar Unjani',
        'faa5442b-711d-11ea-8d93-0603130a05b8' : 'Crisbar Cisitu'
    }

# tanggal = objek datetime.date
# jam = integer
def penentu_awal_akhir_jam(tanggal, jam):
    
    jam -= 1

    awal = datetime(tanggal.year, tanggal.month, tanggal.day, jam, 0, 1, tzinfo=pytz.UTC) - timedelta(hours=7)
    akhir = datetime(tanggal.year, tanggal.month, tanggal.day, jam, 59, 59, tzinfo=pytz.UTC) - timedelta(hours=7)

    string_awal = awal.isoformat()[:-6] + ".000Z"
    string_akhir = akhir.isoformat()[:-6] + ".000Z"

    return string_awal, string_akhir

def eksekusi_struk_sehari(tanggalnya, jamnya):

    """ mengupdate kelas PemakaianAyam sesuai tanggal dan jam yang dimasukkan """

    objek_hari_produksi = HariProduksi.objects.get(hari=tanggalnya)
    awal, akhir = penentu_awal_akhir_jam( tanggalnya, jamnya)
    baseUrl = 'https://api.loyverse.com/v1.0/receipts'
    access_token = '4a3e5665ac324711b13d677c8c05cac8'
    header = {'Authorization' : 'Bearer ' + access_token}
    payload = {
        "created_at_min" : awal,
        "created_at_max" : akhir,
        'limit' : 250
    }
    respon = requests.get(baseUrl, headers=header, params=payload)
    hasil = json.loads(respon.text) # dictionary

    ayam_antapani = 0
    ayam_jatinangor = 0
    ayam_metro = 0
    ayam_sukapura = 0
    ayam_sukabirus = 0
    ayam_unjani = 0
    ayam_cisitu = 0
    ayam_sukajadi = 0

    while True:
        if "cursor" in hasil.keys():
            kumpulan_struk = hasil['receipts']

            for struk in kumpulan_struk:
                try:
                    outlet = rumus_id_outlet[struk['store_id']]
                except:
                    continue
                if struk['receipt_type'] == "SALE":
                    list_pesanan = struk['line_items'] # list of dict
                    for pesanan in list_pesanan:
                        skunya = pesanan['sku'] # string
                        objek_assembly_product = AssemblyProduct.objects.get(sku=skunya)
                        kuantitas = pesanan['quantity'] # integer
                        if "Antapani" in outlet:
                            ayam_antapani += (kuantitas * objek_assembly_product.ayam)
                        elif "Jatinangor" in outlet:
                            ayam_jatinangor += (kuantitas * objek_assembly_product.ayam)
                        elif "Metro" in outlet:
                            ayam_metro += (kuantitas * objek_assembly_product.ayam)
                        elif "Sukapura" in outlet:
                            ayam_sukapura += (kuantitas * objek_assembly_product.ayam)
                        elif "Sukabirus" in outlet:
                            ayam_sukabirus += (kuantitas * objek_assembly_product.ayam)
                        elif "Unjani" in outlet:
                            ayam_unjani += (kuantitas * objek_assembly_product.ayam)
                        elif "Cisitu" in outlet:
                            ayam_cisitu += (kuantitas * objek_assembly_product.ayam)
                        elif "Sukajadi" in outlet:
                            ayam_sukajadi += (kuantitas * objek_assembly_product.ayam)
                else:
                    continue

            respon = requests.get(baseUrl, headers=header, params={ "cursor" : hasil["cursor"]})
            hasil = json.loads(respon.text)
        else:
            kumpulan_struk = hasil['receipts']

            for struk in kumpulan_struk:
                try:
                    outlet = rumus_id_outlet[struk['store_id']]
                except:
                    continue
                if struk['receipt_type'] == "SALE":
                    list_pesanan = struk['line_items'] # list of dict
                    for pesanan in list_pesanan:
                        skunya = pesanan['sku'] # string
                        objek_assembly_product = AssemblyProduct.objects.get(sku=skunya)
                        kuantitas = pesanan['quantity'] # integer
                        if "Antapani" in outlet:
                            ayam_antapani += (kuantitas * objek_assembly_product.ayam)
                        elif "Jatinangor" in outlet:
                            ayam_jatinangor += (kuantitas * objek_assembly_product.ayam)
                        elif "Metro" in outlet:
                            ayam_metro += (kuantitas * objek_assembly_product.ayam)
                        elif "Sukapura" in outlet:
                            ayam_sukapura += (kuantitas * objek_assembly_product.ayam)
                        elif "Sukabirus" in outlet:
                            ayam_sukabirus += (kuantitas * objek_assembly_product.ayam)
                        elif "Unjani" in outlet:
                            ayam_unjani += (kuantitas * objek_assembly_product.ayam)
                        elif "Cisitu" in outlet:
                            ayam_cisitu += (kuantitas * objek_assembly_product.ayam)
                        elif "Sukajadi" in outlet:
                            ayam_sukajadi += (kuantitas * objek_assembly_product.ayam)
                else:
                    continue

            break

    if jamnya == 1:
        objek_hari_produksi.antapani_1 = ayam_antapani
        objek_hari_produksi.jatinangor_1 = ayam_jatinangor
        objek_hari_produksi.metro_1 = ayam_metro
        objek_hari_produksi.sukapura_1 = ayam_sukapura
        objek_hari_produksi.sukabirus_1 = ayam_sukabirus
        objek_hari_produksi.unjani_1 = ayam_unjani
        objek_hari_produksi.cisitu_1 = ayam_cisitu
        objek_hari_produksi.sukajadi_1 = ayam_sukajadi
    elif jamnya == 2:
        objek_hari_produksi.antapani_2 = ayam_antapani
        objek_hari_produksi.jatinangor_2 = ayam_jatinangor
        objek_hari_produksi.metro_2 = ayam_metro
        objek_hari_produksi.sukapura_2 = ayam_sukapura
        objek_hari_produksi.sukabirus_2 = ayam_sukabirus
        objek_hari_produksi.unjani_2 = ayam_unjani
        objek_hari_produksi.cisitu_2 = ayam_cisitu
        objek_hari_produksi.sukajadi_2 = ayam_sukajadi
    elif jamnya == 3:
        objek_hari_produksi.antapani_3 = ayam_antapani
        objek_hari_produksi.jatinangor_3 = ayam_jatinangor
        objek_hari_produksi.metro_3 = ayam_metro
        objek_hari_produksi.sukapura_3 = ayam_sukapura
        objek_hari_produksi.sukabirus_3 = ayam_sukabirus
        objek_hari_produksi.unjani_3 = ayam_unjani
        objek_hari_produksi.cisitu_3 = ayam_cisitu
        objek_hari_produksi.sukajadi_3 = ayam_sukajadi
    elif jamnya == 9:
        objek_hari_produksi.antapani_9 = ayam_antapani
        objek_hari_produksi.jatinangor_9 = ayam_jatinangor
        objek_hari_produksi.metro_9 = ayam_metro
        objek_hari_produksi.sukapura_9 = ayam_sukapura
        objek_hari_produksi.sukabirus_9 = ayam_sukabirus
        objek_hari_produksi.unjani_9 = ayam_unjani
        objek_hari_produksi.cisitu_9 = ayam_cisitu
        objek_hari_produksi.sukajadi_9 = ayam_sukajadi
    elif jamnya == 10:
        objek_hari_produksi.antapani_10 = ayam_antapani
        objek_hari_produksi.jatinangor_10 = ayam_jatinangor
        objek_hari_produksi.metro_10 = ayam_metro
        objek_hari_produksi.sukapura_10 = ayam_sukapura
        objek_hari_produksi.sukabirus_10 = ayam_sukabirus
        objek_hari_produksi.unjani_10 = ayam_unjani
        objek_hari_produksi.cisitu_10 = ayam_cisitu
        objek_hari_produksi.sukajadi_10 = ayam_sukajadi
    elif jamnya == 11:
        objek_hari_produksi.antapani_11 = ayam_antapani
        objek_hari_produksi.jatinangor_11 = ayam_jatinangor
        objek_hari_produksi.metro_11 = ayam_metro
        objek_hari_produksi.sukapura_11 = ayam_sukapura
        objek_hari_produksi.sukabirus_11 = ayam_sukabirus
        objek_hari_produksi.unjani_11 = ayam_unjani
        objek_hari_produksi.cisitu_11 = ayam_cisitu
        objek_hari_produksi.sukajadi_11 = ayam_sukajadi
    elif jamnya == 12:
        objek_hari_produksi.antapani_12 = ayam_antapani
        objek_hari_produksi.jatinangor_12 = ayam_jatinangor
        objek_hari_produksi.metro_12 = ayam_metro
        objek_hari_produksi.sukapura_12 = ayam_sukapura
        objek_hari_produksi.sukabirus_12 = ayam_sukabirus
        objek_hari_produksi.unjani_12 = ayam_unjani
        objek_hari_produksi.cisitu_12 = ayam_cisitu
        objek_hari_produksi.sukajadi_12 = ayam_sukajadi
    elif jamnya == 13:
        objek_hari_produksi.antapani_13 = ayam_antapani
        objek_hari_produksi.jatinangor_13 = ayam_jatinangor
        objek_hari_produksi.metro_13 = ayam_metro
        objek_hari_produksi.sukapura_13 = ayam_sukapura
        objek_hari_produksi.sukabirus_13 = ayam_sukabirus
        objek_hari_produksi.unjani_13 = ayam_unjani
        objek_hari_produksi.cisitu_13 = ayam_cisitu
        objek_hari_produksi.sukajadi_13 = ayam_sukajadi
    elif jamnya == 14:
        objek_hari_produksi.antapani_14 = ayam_antapani
        objek_hari_produksi.jatinangor_14 = ayam_jatinangor
        objek_hari_produksi.metro_14 = ayam_metro
        objek_hari_produksi.sukapura_14 = ayam_sukapura
        objek_hari_produksi.sukabirus_14 = ayam_sukabirus
        objek_hari_produksi.unjani_14 = ayam_unjani
        objek_hari_produksi.cisitu_14 = ayam_cisitu
        objek_hari_produksi.sukajadi_14 = ayam_sukajadi
    elif jamnya == 15:
        objek_hari_produksi.antapani_15 = ayam_antapani
        objek_hari_produksi.jatinangor_15 = ayam_jatinangor
        objek_hari_produksi.metro_15 = ayam_metro
        objek_hari_produksi.sukapura_15 = ayam_sukapura
        objek_hari_produksi.sukabirus_15 = ayam_sukabirus
        objek_hari_produksi.unjani_15 = ayam_unjani
        objek_hari_produksi.cisitu_15 = ayam_cisitu
        objek_hari_produksi.sukajadi_15 = ayam_sukajadi
    elif jamnya == 16:
        objek_hari_produksi.antapani_16 = ayam_antapani
        objek_hari_produksi.jatinangor_16 = ayam_jatinangor
        objek_hari_produksi.metro_16 = ayam_metro
        objek_hari_produksi.sukapura_16 = ayam_sukapura
        objek_hari_produksi.sukabirus_16 = ayam_sukabirus
        objek_hari_produksi.unjani_16 = ayam_unjani
        objek_hari_produksi.cisitu_16 = ayam_cisitu
        objek_hari_produksi.sukajadi_16 = ayam_sukajadi
    elif jamnya == 17:
        objek_hari_produksi.antapani_17 = ayam_antapani
        objek_hari_produksi.jatinangor_17 = ayam_jatinangor
        objek_hari_produksi.metro_17 = ayam_metro
        objek_hari_produksi.sukapura_17 = ayam_sukapura
        objek_hari_produksi.sukabirus_17 = ayam_sukabirus
        objek_hari_produksi.unjani_17 = ayam_unjani
        objek_hari_produksi.cisitu_17 = ayam_cisitu
        objek_hari_produksi.sukajadi_17 = ayam_sukajadi
    elif jamnya == 18:
        objek_hari_produksi.antapani_18 = ayam_antapani
        objek_hari_produksi.jatinangor_18 = ayam_jatinangor
        objek_hari_produksi.metro_18 = ayam_metro
        objek_hari_produksi.sukapura_18 = ayam_sukapura
        objek_hari_produksi.sukabirus_18 = ayam_sukabirus
        objek_hari_produksi.unjani_18 = ayam_unjani
        objek_hari_produksi.cisitu_18 = ayam_cisitu
        objek_hari_produksi.sukajadi_18 = ayam_sukajadi
    elif jamnya == 19:
        objek_hari_produksi.antapani_19 = ayam_antapani
        objek_hari_produksi.jatinangor_19 = ayam_jatinangor
        objek_hari_produksi.metro_19 = ayam_metro
        objek_hari_produksi.sukapura_19 = ayam_sukapura
        objek_hari_produksi.sukabirus_19 = ayam_sukabirus
        objek_hari_produksi.unjani_19 = ayam_unjani
        objek_hari_produksi.cisitu_19 = ayam_cisitu
        objek_hari_produksi.sukajadi_19 = ayam_sukajadi
    elif jamnya == 20:
        objek_hari_produksi.antapani_20 = ayam_antapani
        objek_hari_produksi.jatinangor_20 = ayam_jatinangor
        objek_hari_produksi.metro_20 = ayam_metro
        objek_hari_produksi.sukapura_20 = ayam_sukapura
        objek_hari_produksi.sukabirus_20 = ayam_sukabirus
        objek_hari_produksi.unjani_20 = ayam_unjani
        objek_hari_produksi.cisitu_20 = ayam_cisitu
        objek_hari_produksi.sukajadi_20 = ayam_sukajadi
    elif jamnya == 21:
        objek_hari_produksi.antapani_21 = ayam_antapani
        objek_hari_produksi.jatinangor_21 = ayam_jatinangor
        objek_hari_produksi.metro_21 = ayam_metro
        objek_hari_produksi.sukapura_21 = ayam_sukapura
        objek_hari_produksi.sukabirus_21 = ayam_sukabirus
        objek_hari_produksi.unjani_21 = ayam_unjani
        objek_hari_produksi.cisitu_21 = ayam_cisitu
        objek_hari_produksi.sukajadi_21 = ayam_sukajadi
    elif jamnya == 22:
        objek_hari_produksi.antapani_22 = ayam_antapani
        objek_hari_produksi.jatinangor_22 = ayam_jatinangor
        objek_hari_produksi.metro_22 = ayam_metro
        objek_hari_produksi.sukapura_22 = ayam_sukapura
        objek_hari_produksi.sukabirus_22 = ayam_sukabirus
        objek_hari_produksi.unjani_22 = ayam_unjani
        objek_hari_produksi.cisitu_22 = ayam_cisitu
        objek_hari_produksi.sukajadi_22 = ayam_sukajadi
    elif jamnya == 23:
        objek_hari_produksi.antapani_23 = ayam_antapani
        objek_hari_produksi.jatinangor_23 = ayam_jatinangor
        objek_hari_produksi.metro_23 = ayam_metro
        objek_hari_produksi.sukapura_23 = ayam_sukapura
        objek_hari_produksi.sukabirus_23 = ayam_sukabirus
        objek_hari_produksi.unjani_23 = ayam_unjani
        objek_hari_produksi.cisitu_23 = ayam_cisitu
        objek_hari_produksi.sukajadi_23 = ayam_sukajadi
    elif jamnya == 24:
        objek_hari_produksi.antapani_24 = ayam_antapani
        objek_hari_produksi.jatinangor_24 = ayam_jatinangor
        objek_hari_produksi.metro_24 = ayam_metro
        objek_hari_produksi.sukapura_24 = ayam_sukapura
        objek_hari_produksi.sukabirus_24 = ayam_sukabirus
        objek_hari_produksi.unjani_24 = ayam_unjani
        objek_hari_produksi.cisitu_24 = ayam_cisitu
        objek_hari_produksi.sukajadi_24 = ayam_sukajadi

    objek_hari_produksi.dieksekusi = True
    objek_hari_produksi.save()

def eksekusi(tanggal, puasa=False):
    if not puasa:
        jamnya = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    else:
        jamnya = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 1, 2, 3]

    for jam in jamnya:
        eksekusi_struk_sehari(tanggal, jam)

def cek_hari():
    hari_ini = date.today()
    kemarin = hari_ini - timedelta(days=1)
    hp = HariProduksi.objects.filter(hari=kemarin)
    if not hp:
        p = HariProduksi(
            hari = kemarin,
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
        if (kemarin <= date(2021, 5, 12)) and (kemarin >= date(2021, 4, 13)):
            eksekusi(kemarin, puasa=True)
        else:
            eksekusi(kemarin, puasa=False)

    kemarin = hari_ini - timedelta(days=2)
    hp = HariProduksi.objects.filter(hari=kemarin)
    if not hp:
        p = HariProduksi(
            hari = kemarin,
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
        if (kemarin <= date(2021, 5, 12)) and (kemarin >= date(2021, 4, 13)):
            eksekusi(kemarin, puasa=True)
        else:
            eksekusi(kemarin, puasa=False)

    kemarin = hari_ini - timedelta(days=3)
    hp = HariProduksi.objects.filter(hari=kemarin)
    if not hp:
        p = HariProduksi(
            hari = kemarin,
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
        if (kemarin <= date(2021, 5, 12)) and (kemarin >= date(2021, 4, 13)):
            eksekusi(kemarin, puasa=True)
        else:
            eksekusi(kemarin, puasa=False)

def percantik_float(angkanya):
    hasil = "{:.2f}".format(angkanya)
    return float(hasil)

def rekomendasi_stok_hari(seminggu_lalu, dua_minggu_lalu):
    ratarata = (seminggu_lalu + dua_minggu_lalu)/2
    deviasi = stat.stdev([seminggu_lalu, dua_minggu_lalu])
    konstanta = 3
    hasil = ratarata + (deviasi * konstanta)
    return percantik_float(hasil)

def query_home_operation():
    rumus_hari = {
        "0" : "Senin",
        "1" : "Selasa",
        "2" : "Rabu",
        "3" : "Kamis",
        "4" : "Jumat",
        "5" : "Sabtu",
        "6" : "Minggu",
    }
    cek_hari()
    
    hari_ini_hari_apa = rumus_hari[str(date.today().weekday())]
    satu_minggu_lalu = date.today() - timedelta(days=7)
    dua_minggu_lalu = date.today() - timedelta(days=14)

    q = [HariProduksi.objects.get(hari=satu_minggu_lalu), HariProduksi.objects.get(hari=dua_minggu_lalu)]

    querynya = {
            "Hari" : hari_ini_hari_apa,
            "dua_minggu_sebelum" : q[1].hari,
            "seminggu_sebelum" : q[0].hari,
            "Tanggal" : date.today(),
            "Antapani" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                [ "1:00", rekomendasi_stok_hari(q[0].antapani_1, q[1].antapani_1), q[0].antapani_1, q[1].antapani_1, percantik_float(stat.stdev([q[0].antapani_1, q[1].antapani_1])) ],
                [ "2:00", rekomendasi_stok_hari(q[0].antapani_2, q[1].antapani_2), q[0].antapani_2, q[1].antapani_2, percantik_float(stat.stdev([q[0].antapani_2, q[1].antapani_2])) ],
                [ "3:00", rekomendasi_stok_hari(q[0].antapani_3, q[1].antapani_3), q[0].antapani_3, q[1].antapani_3, percantik_float(stat.stdev([q[0].antapani_3, q[1].antapani_3])) ],
                [ "9:00", rekomendasi_stok_hari(q[0].antapani_9, q[1].antapani_9), q[0].antapani_9, q[1].antapani_9, percantik_float(stat.stdev([q[0].antapani_9, q[1].antapani_9])) ],
                [ "10:00", rekomendasi_stok_hari(q[0].antapani_10, q[1].antapani_10), q[0].antapani_10, q[1].antapani_10, percantik_float(stat.stdev([q[0].antapani_10, q[1].antapani_10])) ],
                [ "11:00", rekomendasi_stok_hari(q[0].antapani_11, q[1].antapani_11), q[0].antapani_11, q[1].antapani_11, percantik_float(stat.stdev([q[0].antapani_11, q[1].antapani_11])) ],
                [ "12:00", rekomendasi_stok_hari(q[0].antapani_12, q[1].antapani_12), q[0].antapani_12, q[1].antapani_12, percantik_float(stat.stdev([q[0].antapani_12, q[1].antapani_12])) ],
                [ "13:00", rekomendasi_stok_hari(q[0].antapani_13, q[1].antapani_13), q[0].antapani_13, q[1].antapani_13, percantik_float(stat.stdev([q[0].antapani_13, q[1].antapani_13])) ],
                [ "14:00", rekomendasi_stok_hari(q[0].antapani_14, q[1].antapani_14), q[0].antapani_14, q[1].antapani_14, percantik_float(stat.stdev([q[0].antapani_14, q[1].antapani_14])) ],
                [ "15:00", rekomendasi_stok_hari(q[0].antapani_15, q[1].antapani_15), q[0].antapani_15, q[1].antapani_15, percantik_float(stat.stdev([q[0].antapani_15, q[1].antapani_15])) ],
                [ "16:00", rekomendasi_stok_hari(q[0].antapani_16, q[1].antapani_16), q[0].antapani_16, q[1].antapani_16, percantik_float(stat.stdev([q[0].antapani_16, q[1].antapani_16])) ],
                [ "17:00", rekomendasi_stok_hari(q[0].antapani_17, q[1].antapani_17), q[0].antapani_17, q[1].antapani_17, percantik_float(stat.stdev([q[0].antapani_17, q[1].antapani_17])) ],
                [ "18:00", rekomendasi_stok_hari(q[0].antapani_18, q[1].antapani_18), q[0].antapani_18, q[1].antapani_18, percantik_float(stat.stdev([q[0].antapani_18, q[1].antapani_18])) ],
                [ "19:00", rekomendasi_stok_hari(q[0].antapani_19, q[1].antapani_19), q[0].antapani_19, q[1].antapani_19, percantik_float(stat.stdev([q[0].antapani_19, q[1].antapani_19])) ],
                [ "20:00", rekomendasi_stok_hari(q[0].antapani_20, q[1].antapani_20), q[0].antapani_20, q[1].antapani_20, percantik_float(stat.stdev([q[0].antapani_20, q[1].antapani_20])) ],
                [ "21:00",rekomendasi_stok_hari(q[0].antapani_21, q[1].antapani_21), q[0].antapani_21, q[1].antapani_21, percantik_float(stat.stdev([q[0].antapani_21, q[1].antapani_21])) ],
                [ "22:00",rekomendasi_stok_hari(q[0].antapani_22, q[1].antapani_22), q[0].antapani_22, q[1].antapani_22, percantik_float(stat.stdev([q[0].antapani_22, q[1].antapani_22])) ],
                [ "23:00",rekomendasi_stok_hari(q[0].antapani_23, q[1].antapani_23), q[0].antapani_23, q[1].antapani_23, percantik_float(stat.stdev([q[0].antapani_23, q[1].antapani_23])) ],
                [ "24:00",rekomendasi_stok_hari(q[0].antapani_24, q[1].antapani_24), q[0].antapani_24, q[1].antapani_24, percantik_float(stat.stdev([q[0].antapani_24, q[1].antapani_24])) ],   
            ],
       
            "Jatinangor" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                [ "1:00", rekomendasi_stok_hari(q[0].jatinangor_1, q[1].jatinangor_1), q[0].jatinangor_1, q[1].jatinangor_1, percantik_float(stat.stdev([q[0].jatinangor_1, q[1].jatinangor_1])) ],
                [ "2:00", rekomendasi_stok_hari(q[0].jatinangor_2, q[1].jatinangor_2), q[0].jatinangor_2, q[1].jatinangor_2, percantik_float(stat.stdev([q[0].jatinangor_2, q[1].jatinangor_2])) ],
                [ "3:00", rekomendasi_stok_hari(q[0].jatinangor_3, q[1].jatinangor_3), q[0].jatinangor_3, q[1].jatinangor_3, percantik_float(stat.stdev([q[0].jatinangor_3, q[1].jatinangor_3])) ],
                [ "9:00", rekomendasi_stok_hari(q[0].jatinangor_9, q[1].jatinangor_9), q[0].jatinangor_9, q[1].jatinangor_9, percantik_float(stat.stdev([q[0].jatinangor_9, q[1].jatinangor_9])) ],
                [ "10:00", rekomendasi_stok_hari(q[0].jatinangor_10, q[1].jatinangor_10), q[0].jatinangor_10, q[1].jatinangor_10, percantik_float(stat.stdev([q[0].jatinangor_10, q[1].jatinangor_10])) ],
                [ "11:00", rekomendasi_stok_hari(q[0].jatinangor_11, q[1].jatinangor_11), q[0].jatinangor_11, q[1].jatinangor_11, percantik_float(stat.stdev([q[0].jatinangor_11, q[1].jatinangor_11])) ],
                [ "12:00", rekomendasi_stok_hari(q[0].jatinangor_12, q[1].jatinangor_12), q[0].jatinangor_12, q[1].jatinangor_12, percantik_float(stat.stdev([q[0].jatinangor_12, q[1].jatinangor_12])) ],
                [ "13:00", rekomendasi_stok_hari(q[0].jatinangor_13, q[1].jatinangor_13), q[0].jatinangor_13, q[1].jatinangor_13, percantik_float(stat.stdev([q[0].jatinangor_13, q[1].jatinangor_13])) ],
                [ "14:00", rekomendasi_stok_hari(q[0].jatinangor_14, q[1].jatinangor_14), q[0].jatinangor_14, q[1].jatinangor_14, percantik_float(stat.stdev([q[0].jatinangor_14, q[1].jatinangor_14])) ],
                [ "15:00", rekomendasi_stok_hari(q[0].jatinangor_15, q[1].jatinangor_15), q[0].jatinangor_15, q[1].jatinangor_15, percantik_float(stat.stdev([q[0].jatinangor_15, q[1].jatinangor_15])) ],
                [ "16:00", rekomendasi_stok_hari(q[0].jatinangor_16, q[1].jatinangor_16), q[0].jatinangor_16, q[1].jatinangor_16, percantik_float(stat.stdev([q[0].jatinangor_16, q[1].jatinangor_16])) ],
                [ "17:00", rekomendasi_stok_hari(q[0].jatinangor_17, q[1].jatinangor_17), q[0].jatinangor_17, q[1].jatinangor_17, percantik_float(stat.stdev([q[0].jatinangor_17, q[1].jatinangor_17])) ],
                [ "18:00", rekomendasi_stok_hari(q[0].jatinangor_18, q[1].jatinangor_18), q[0].jatinangor_18, q[1].jatinangor_18, percantik_float(stat.stdev([q[0].jatinangor_18, q[1].jatinangor_18])) ],
                [ "19:00", rekomendasi_stok_hari(q[0].jatinangor_19, q[1].jatinangor_19), q[0].jatinangor_19, q[1].jatinangor_19, percantik_float(stat.stdev([q[0].jatinangor_19, q[1].jatinangor_19])) ],
                [ "20:00", rekomendasi_stok_hari(q[0].jatinangor_20, q[1].jatinangor_20), q[0].jatinangor_20, q[1].jatinangor_20, percantik_float(stat.stdev([q[0].jatinangor_20, q[1].jatinangor_20])) ],
                [ "21:00", rekomendasi_stok_hari(q[0].jatinangor_21, q[1].jatinangor_21), q[0].jatinangor_21, q[1].jatinangor_21, percantik_float(stat.stdev([q[0].jatinangor_21, q[1].jatinangor_21])) ],
                [ "22:00", rekomendasi_stok_hari(q[0].jatinangor_22, q[1].jatinangor_22), q[0].jatinangor_22, q[1].jatinangor_22, percantik_float(stat.stdev([q[0].jatinangor_22, q[1].jatinangor_22])) ],
                [ "23:00", rekomendasi_stok_hari(q[0].jatinangor_23, q[1].jatinangor_23), q[0].jatinangor_23, q[1].jatinangor_23, percantik_float(stat.stdev([q[0].jatinangor_23, q[1].jatinangor_23])) ],
                [ "24:00", rekomendasi_stok_hari(q[0].jatinangor_24, q[1].jatinangor_24), q[0].jatinangor_24, q[1].jatinangor_24, percantik_float(stat.stdev([q[0].jatinangor_24, q[1].jatinangor_24])) ],
            ],

            "Metro" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                [ "1:00", rekomendasi_stok_hari(q[0].metro_1, q[1].metro_1), q[0].metro_1, q[1].metro_1, percantik_float(stat.stdev([q[0].metro_1, q[1].metro_1])) ],
                [ "2:00", rekomendasi_stok_hari(q[0].metro_2, q[1].metro_2), q[0].metro_2, q[1].metro_2, percantik_float(stat.stdev([q[0].metro_2, q[1].metro_2])) ],
                [ "3:00", rekomendasi_stok_hari(q[0].metro_3, q[1].metro_3), q[0].metro_3, q[1].metro_3, percantik_float(stat.stdev([q[0].metro_3, q[1].metro_3])) ],
                [ "9:00", rekomendasi_stok_hari(q[0].metro_9, q[1].metro_9), q[0].metro_9, q[1].metro_9, percantik_float(stat.stdev([q[0].metro_9, q[1].metro_9])) ],
                [ "10:00", rekomendasi_stok_hari(q[0].metro_10, q[1].metro_10), q[0].metro_10, q[1].metro_10, percantik_float(stat.stdev([q[0].metro_10, q[1].metro_10])) ],
                [ "11:00", rekomendasi_stok_hari(q[0].metro_11, q[1].metro_11), q[0].metro_11, q[1].metro_11, percantik_float(stat.stdev([q[0].metro_11, q[1].metro_11])) ],
                [ "12:00", rekomendasi_stok_hari(q[0].metro_12, q[1].metro_12), q[0].metro_12, q[1].metro_12, percantik_float(stat.stdev([q[0].metro_12, q[1].metro_12])) ],
                [ "13:00", rekomendasi_stok_hari(q[0].metro_13, q[1].metro_13), q[0].metro_13, q[1].metro_13, percantik_float(stat.stdev([q[0].metro_13, q[1].metro_13])) ],
                [ "14:00", rekomendasi_stok_hari(q[0].metro_14, q[1].metro_14), q[0].metro_14, q[1].metro_14, percantik_float(stat.stdev([q[0].metro_14, q[1].metro_14])) ],
                [ "15:00", rekomendasi_stok_hari(q[0].metro_15, q[1].metro_15), q[0].metro_15, q[1].metro_15, percantik_float(stat.stdev([q[0].metro_15, q[1].metro_15])) ],
                [ "16:00", rekomendasi_stok_hari(q[0].metro_16, q[1].metro_16), q[0].metro_16, q[1].metro_16, percantik_float(stat.stdev([q[0].metro_16, q[1].metro_16])) ],
                [ "17:00", rekomendasi_stok_hari(q[0].metro_17, q[1].metro_17), q[0].metro_17, q[1].metro_17, percantik_float(stat.stdev([q[0].metro_17, q[1].metro_17])) ],
                [ "18:00", rekomendasi_stok_hari(q[0].metro_18, q[1].metro_18), q[0].metro_18, q[1].metro_18, percantik_float(stat.stdev([q[0].metro_18, q[1].metro_18])) ],
                [ "19:00", rekomendasi_stok_hari(q[0].metro_19, q[1].metro_19), q[0].metro_19, q[1].metro_19, percantik_float(stat.stdev([q[0].metro_19, q[1].metro_19])) ],
                [ "20:00", rekomendasi_stok_hari(q[0].metro_20, q[1].metro_20), q[0].metro_20, q[1].metro_20, percantik_float(stat.stdev([q[0].metro_20, q[1].metro_20])) ],
                [ "21:00", rekomendasi_stok_hari(q[0].metro_21, q[1].metro_21), q[0].metro_21, q[1].metro_21, percantik_float(stat.stdev([q[0].metro_21, q[1].metro_21])) ],
                [ "22:00", rekomendasi_stok_hari(q[0].metro_22, q[1].metro_22), q[0].metro_22, q[1].metro_22, percantik_float(stat.stdev([q[0].metro_22, q[1].metro_22])) ],
                [ "23:00", rekomendasi_stok_hari(q[0].metro_23, q[1].metro_23), q[0].metro_23, q[1].metro_23, percantik_float(stat.stdev([q[0].metro_23, q[1].metro_23])) ],
                [ "24:00", rekomendasi_stok_hari(q[0].metro_24, q[1].metro_24), q[0].metro_24, q[1].metro_24, percantik_float(stat.stdev([q[0].metro_24, q[1].metro_24])) ],
            ],
    
            "Sukapura" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                [ "1:00", rekomendasi_stok_hari(q[0].sukapura_1, q[1].sukapura_1), q[0].sukapura_1, q[1].sukapura_1, percantik_float(stat.stdev([q[0].sukapura_1, q[1].sukapura_1])) ],
                [ "2:00", rekomendasi_stok_hari(q[0].sukapura_2, q[1].sukapura_2), q[0].sukapura_2, q[1].sukapura_2, percantik_float(stat.stdev([q[0].sukapura_2, q[1].sukapura_2])) ],
                [ "3:00", rekomendasi_stok_hari(q[0].sukapura_3, q[1].sukapura_3), q[0].sukapura_3, q[1].sukapura_3, percantik_float(stat.stdev([q[0].sukapura_3, q[1].sukapura_3])) ],
                [ "9:00", rekomendasi_stok_hari(q[0].sukapura_9, q[1].sukapura_9), q[0].sukapura_9, q[1].sukapura_9, percantik_float(stat.stdev([q[0].sukapura_9, q[1].sukapura_9])) ],
                [ "10:00", rekomendasi_stok_hari(q[0].sukapura_10, q[1].sukapura_10), q[0].sukapura_10, q[1].sukapura_10, percantik_float(stat.stdev([q[0].sukapura_10, q[1].sukapura_10])) ],
                [ "11:00", rekomendasi_stok_hari(q[0].sukapura_11, q[1].sukapura_11), q[0].sukapura_11, q[1].sukapura_11, percantik_float(stat.stdev([q[0].sukapura_11, q[1].sukapura_11])) ],
                [ "12:00", rekomendasi_stok_hari(q[0].sukapura_12, q[1].sukapura_12), q[0].sukapura_12, q[1].sukapura_12, percantik_float(stat.stdev([q[0].sukapura_12, q[1].sukapura_12])) ],
                [ "13:00", rekomendasi_stok_hari(q[0].sukapura_13, q[1].sukapura_13), q[0].sukapura_13, q[1].sukapura_13, percantik_float(stat.stdev([q[0].sukapura_13, q[1].sukapura_13])) ],
                [ "14:00", rekomendasi_stok_hari(q[0].sukapura_14, q[1].sukapura_14), q[0].sukapura_14, q[1].sukapura_14, percantik_float(stat.stdev([q[0].sukapura_14, q[1].sukapura_14])) ],
                [ "15:00", rekomendasi_stok_hari(q[0].sukapura_15, q[1].sukapura_15), q[0].sukapura_15, q[1].sukapura_15, percantik_float(stat.stdev([q[0].sukapura_15, q[1].sukapura_15])) ],
                [ "16:00", rekomendasi_stok_hari(q[0].sukapura_16, q[1].sukapura_16), q[0].sukapura_16, q[1].sukapura_16, percantik_float(stat.stdev([q[0].sukapura_16, q[1].sukapura_16])) ],
                [ "17:00", rekomendasi_stok_hari(q[0].sukapura_17, q[1].sukapura_17), q[0].sukapura_17, q[1].sukapura_17, percantik_float(stat.stdev([q[0].sukapura_17, q[1].sukapura_17])) ],
                [ "18:00", rekomendasi_stok_hari(q[0].sukapura_18, q[1].sukapura_18), q[0].sukapura_18, q[1].sukapura_18, percantik_float(stat.stdev([q[0].sukapura_18, q[1].sukapura_18])) ],
                [ "19:00", rekomendasi_stok_hari(q[0].sukapura_19, q[1].sukapura_19), q[0].sukapura_19, q[1].sukapura_19, percantik_float(stat.stdev([q[0].sukapura_19, q[1].sukapura_19])) ],
                [ "20:00", rekomendasi_stok_hari(q[0].sukapura_20, q[1].sukapura_20), q[0].sukapura_20, q[1].sukapura_20, percantik_float(stat.stdev([q[0].sukapura_20, q[1].sukapura_20])) ],
                [ "21:00", rekomendasi_stok_hari(q[0].sukapura_21, q[1].sukapura_21), q[0].sukapura_21, q[1].sukapura_21, percantik_float(stat.stdev([q[0].sukapura_21, q[1].sukapura_21])) ],
                [ "22:00", rekomendasi_stok_hari(q[0].sukapura_22, q[1].sukapura_22), q[0].sukapura_22, q[1].sukapura_22, percantik_float(stat.stdev([q[0].sukapura_22, q[1].sukapura_22])) ],
                [ "23:00", rekomendasi_stok_hari(q[0].sukapura_23, q[1].sukapura_23), q[0].sukapura_23, q[1].sukapura_23, percantik_float(stat.stdev([q[0].sukapura_23, q[1].sukapura_23])) ],
                [ "24:00", rekomendasi_stok_hari(q[0].sukapura_24, q[1].sukapura_24), q[0].sukapura_24, q[1].sukapura_24, percantik_float(stat.stdev([q[0].sukapura_24, q[1].sukapura_24])) ],
            ],

            "Sukabirus" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                [ "1:00", rekomendasi_stok_hari(q[0].sukabirus_1, q[1].sukabirus_1), q[0].sukabirus_1, q[1].sukabirus_1, percantik_float(stat.stdev([q[0].sukabirus_1, q[1].sukabirus_1])) ],
                [ "2:00", rekomendasi_stok_hari(q[0].sukabirus_2, q[1].sukabirus_2), q[0].sukabirus_2, q[1].sukabirus_2, percantik_float(stat.stdev([q[0].sukabirus_2, q[1].sukabirus_2])) ],
                [ "3:00", rekomendasi_stok_hari(q[0].sukabirus_3, q[1].sukabirus_3), q[0].sukabirus_3, q[1].sukabirus_3, percantik_float(stat.stdev([q[0].sukabirus_3, q[1].sukabirus_3])) ],
                [ "9:00", rekomendasi_stok_hari(q[0].sukabirus_9, q[1].sukabirus_9), q[0].sukabirus_9, q[1].sukabirus_9, percantik_float(stat.stdev([q[0].sukabirus_9, q[1].sukabirus_9])) ],
                [ "10:00", rekomendasi_stok_hari(q[0].sukabirus_10, q[1].sukabirus_10), q[0].sukabirus_10, q[1].sukabirus_10, percantik_float(stat.stdev([q[0].sukabirus_10, q[1].sukabirus_10])) ],
                [ "11:00", rekomendasi_stok_hari(q[0].sukabirus_11, q[1].sukabirus_11), q[0].sukabirus_11, q[1].sukabirus_11, percantik_float(stat.stdev([q[0].sukabirus_11, q[1].sukabirus_11])) ],
                [ "12:00", rekomendasi_stok_hari(q[0].sukabirus_12, q[1].sukabirus_12), q[0].sukabirus_12, q[1].sukabirus_12, percantik_float(stat.stdev([q[0].sukabirus_12, q[1].sukabirus_12])) ],
                [ "13:00", rekomendasi_stok_hari(q[0].sukabirus_13, q[1].sukabirus_13), q[0].sukabirus_13, q[1].sukabirus_13, percantik_float(stat.stdev([q[0].sukabirus_13, q[1].sukabirus_13])) ],
                [ "14:00", rekomendasi_stok_hari(q[0].sukabirus_14, q[1].sukabirus_14), q[0].sukabirus_14, q[1].sukabirus_14, percantik_float(stat.stdev([q[0].sukabirus_14, q[1].sukabirus_14])) ],
                [ "15:00", rekomendasi_stok_hari(q[0].sukabirus_15, q[1].sukabirus_15), q[0].sukabirus_15, q[1].sukabirus_15, percantik_float(stat.stdev([q[0].sukabirus_15, q[1].sukabirus_15])) ],
                [ "16:00", rekomendasi_stok_hari(q[0].sukabirus_16, q[1].sukabirus_16), q[0].sukabirus_16, q[1].sukabirus_16, percantik_float(stat.stdev([q[0].sukabirus_16, q[1].sukabirus_16])) ],
                [ "17:00", rekomendasi_stok_hari(q[0].sukabirus_17, q[1].sukabirus_17), q[0].sukabirus_17, q[1].sukabirus_17, percantik_float(stat.stdev([q[0].sukabirus_17, q[1].sukabirus_17])) ],
                [ "18:00", rekomendasi_stok_hari(q[0].sukabirus_18, q[1].sukabirus_18), q[0].sukabirus_18, q[1].sukabirus_18, percantik_float(stat.stdev([q[0].sukabirus_18, q[1].sukabirus_18])) ],
                [ "19:00", rekomendasi_stok_hari(q[0].sukabirus_19, q[1].sukabirus_19), q[0].sukabirus_19, q[1].sukabirus_19, percantik_float(stat.stdev([q[0].sukabirus_19, q[1].sukabirus_19])) ],
                [ "20:00", rekomendasi_stok_hari(q[0].sukabirus_20, q[1].sukabirus_20), q[0].sukabirus_20, q[1].sukabirus_20, percantik_float(stat.stdev([q[0].sukabirus_20, q[1].sukabirus_20])) ],
                [ "21:00", rekomendasi_stok_hari(q[0].sukabirus_21, q[1].sukabirus_21), q[0].sukabirus_21, q[1].sukabirus_21, percantik_float(stat.stdev([q[0].sukabirus_21, q[1].sukabirus_21])) ],
                [ "22:00", rekomendasi_stok_hari(q[0].sukabirus_22, q[1].sukabirus_22), q[0].sukabirus_22, q[1].sukabirus_22, percantik_float(stat.stdev([q[0].sukabirus_22, q[1].sukabirus_22])) ],
                [ "23:00", rekomendasi_stok_hari(q[0].sukabirus_23, q[1].sukabirus_23), q[0].sukabirus_23, q[1].sukabirus_23, percantik_float(stat.stdev([q[0].sukabirus_23, q[1].sukabirus_23])) ],
                [ "24:00", rekomendasi_stok_hari(q[0].sukabirus_24, q[1].sukabirus_24), q[0].sukabirus_24, q[1].sukabirus_24, percantik_float(stat.stdev([q[0].sukabirus_24, q[1].sukabirus_24])) ],
            ],

            "Unjani" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                [ "1:00", rekomendasi_stok_hari(q[0].unjani_1, q[1].unjani_1), q[0].unjani_1, q[1].unjani_1, percantik_float(stat.stdev([q[0].unjani_1, q[1].unjani_1])) ],
                [ "2:00", rekomendasi_stok_hari(q[0].unjani_2, q[1].unjani_2), q[0].unjani_2, q[1].unjani_2, percantik_float(stat.stdev([q[0].unjani_2, q[1].unjani_2])) ],
                [ "3:00", rekomendasi_stok_hari(q[0].unjani_3, q[1].unjani_3), q[0].unjani_3, q[1].unjani_3, percantik_float(stat.stdev([q[0].unjani_3, q[1].unjani_3])) ],
                [ "9:00", rekomendasi_stok_hari(q[0].unjani_9, q[1].unjani_9), q[0].unjani_9, q[1].unjani_9, percantik_float(stat.stdev([q[0].unjani_9, q[1].unjani_9])) ],
                [ "10:00", rekomendasi_stok_hari(q[0].unjani_10, q[1].unjani_10), q[0].unjani_10, q[1].unjani_10, percantik_float(stat.stdev([q[0].unjani_10, q[1].unjani_10])) ],
                [ "11:00", rekomendasi_stok_hari(q[0].unjani_11, q[1].unjani_11), q[0].unjani_11, q[1].unjani_11, percantik_float(stat.stdev([q[0].unjani_11, q[1].unjani_11])) ],
                [ "12:00", rekomendasi_stok_hari(q[0].unjani_12, q[1].unjani_12), q[0].unjani_12, q[1].unjani_12, percantik_float(stat.stdev([q[0].unjani_12, q[1].unjani_12])) ],
                [ "13:00", rekomendasi_stok_hari(q[0].unjani_13, q[1].unjani_13), q[0].unjani_13, q[1].unjani_13, percantik_float(stat.stdev([q[0].unjani_13, q[1].unjani_13])) ],
                [ "14:00", rekomendasi_stok_hari(q[0].unjani_14, q[1].unjani_14), q[0].unjani_14, q[1].unjani_14, percantik_float(stat.stdev([q[0].unjani_14, q[1].unjani_14])) ],
                [ "15:00", rekomendasi_stok_hari(q[0].unjani_15, q[1].unjani_15), q[0].unjani_15, q[1].unjani_15, percantik_float(stat.stdev([q[0].unjani_15, q[1].unjani_15])) ],
                [ "16:00", rekomendasi_stok_hari(q[0].unjani_16, q[1].unjani_16), q[0].unjani_16, q[1].unjani_16, percantik_float(stat.stdev([q[0].unjani_16, q[1].unjani_16])) ],
                [ "17:00", rekomendasi_stok_hari(q[0].unjani_17, q[1].unjani_17), q[0].unjani_17, q[1].unjani_17, percantik_float(stat.stdev([q[0].unjani_17, q[1].unjani_17])) ],
                [ "18:00", rekomendasi_stok_hari(q[0].unjani_18, q[1].unjani_18), q[0].unjani_18, q[1].unjani_18, percantik_float(stat.stdev([q[0].unjani_18, q[1].unjani_18])) ],
                [ "19:00", rekomendasi_stok_hari(q[0].unjani_19, q[1].unjani_19), q[0].unjani_19, q[1].unjani_19, percantik_float(stat.stdev([q[0].unjani_19, q[1].unjani_19])) ],
                [ "20:00", rekomendasi_stok_hari(q[0].unjani_20, q[1].unjani_20), q[0].unjani_20, q[1].unjani_20, percantik_float(stat.stdev([q[0].unjani_20, q[1].unjani_20])) ],
                [ "21:00", rekomendasi_stok_hari(q[0].unjani_21, q[1].unjani_21), q[0].unjani_21, q[1].unjani_21, percantik_float(stat.stdev([q[0].unjani_21, q[1].unjani_21])) ],
                [ "22:00", rekomendasi_stok_hari(q[0].unjani_22, q[1].unjani_22), q[0].unjani_22, q[1].unjani_22, percantik_float(stat.stdev([q[0].unjani_22, q[1].unjani_22])) ],
                [ "23:00", rekomendasi_stok_hari(q[0].unjani_23, q[1].unjani_23), q[0].unjani_23, q[1].unjani_23, percantik_float(stat.stdev([q[0].unjani_23, q[1].unjani_23])) ],
                [ "24:00", rekomendasi_stok_hari(q[0].unjani_24, q[1].unjani_24), q[0].unjani_24, q[1].unjani_24, percantik_float(stat.stdev([q[0].unjani_24, q[1].unjani_24])) ],
            ],

            "Cisitu" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                [ "1:00", rekomendasi_stok_hari(q[0].unjani_1, q[1].unjani_1), q[0].unjani_1, q[1].unjani_1, percantik_float(stat.stdev([q[0].unjani_1, q[1].unjani_1])) ],
                [ "2:00", rekomendasi_stok_hari(q[0].unjani_2, q[1].unjani_2), q[0].unjani_2, q[1].unjani_2, percantik_float(stat.stdev([q[0].unjani_2, q[1].unjani_2])) ],
                [ "3:00", rekomendasi_stok_hari(q[0].unjani_3, q[1].unjani_3), q[0].unjani_3, q[1].unjani_3, percantik_float(stat.stdev([q[0].unjani_3, q[1].unjani_3])) ],
                [ "9:00", rekomendasi_stok_hari(q[0].unjani_9, q[1].unjani_9), q[0].unjani_9, q[1].unjani_9, percantik_float(stat.stdev([q[0].unjani_9, q[1].unjani_9])) ],
                [ "10:00", rekomendasi_stok_hari(q[0].unjani_10, q[1].unjani_10), q[0].unjani_10, q[1].unjani_10, percantik_float(stat.stdev([q[0].unjani_10, q[1].unjani_10])) ],
                [ "11:00", rekomendasi_stok_hari(q[0].unjani_11, q[1].unjani_11), q[0].unjani_11, q[1].unjani_11, percantik_float(stat.stdev([q[0].unjani_11, q[1].unjani_11])) ],
                [ "12:00", rekomendasi_stok_hari(q[0].unjani_12, q[1].unjani_12), q[0].unjani_12, q[1].unjani_12, percantik_float(stat.stdev([q[0].unjani_12, q[1].unjani_12])) ],
                [ "13:00", rekomendasi_stok_hari(q[0].unjani_13, q[1].unjani_13), q[0].unjani_13, q[1].unjani_13, percantik_float(stat.stdev([q[0].unjani_13, q[1].unjani_13])) ],
                [ "14:00", rekomendasi_stok_hari(q[0].unjani_14, q[1].unjani_14), q[0].unjani_14, q[1].unjani_14, percantik_float(stat.stdev([q[0].unjani_14, q[1].unjani_14])) ],
                [ "15:00", rekomendasi_stok_hari(q[0].unjani_15, q[1].unjani_15), q[0].unjani_15, q[1].unjani_15, percantik_float(stat.stdev([q[0].unjani_15, q[1].unjani_15])) ],
                [ "16:00", rekomendasi_stok_hari(q[0].unjani_16, q[1].unjani_16), q[0].unjani_16, q[1].unjani_16, percantik_float(stat.stdev([q[0].unjani_16, q[1].unjani_16])) ],
                [ "17:00", rekomendasi_stok_hari(q[0].unjani_17, q[1].unjani_17), q[0].unjani_17, q[1].unjani_17, percantik_float(stat.stdev([q[0].unjani_17, q[1].unjani_17])) ],
                [ "18:00", rekomendasi_stok_hari(q[0].unjani_18, q[1].unjani_18), q[0].unjani_18, q[1].unjani_18, percantik_float(stat.stdev([q[0].unjani_18, q[1].unjani_18])) ],
                [ "19:00", rekomendasi_stok_hari(q[0].unjani_19, q[1].unjani_19), q[0].unjani_19, q[1].unjani_19, percantik_float(stat.stdev([q[0].unjani_19, q[1].unjani_19])) ],
                [ "20:00", rekomendasi_stok_hari(q[0].unjani_20, q[1].unjani_20), q[0].unjani_20, q[1].unjani_20, percantik_float(stat.stdev([q[0].unjani_20, q[1].unjani_20])) ],
                [ "21:00", rekomendasi_stok_hari(q[0].unjani_21, q[1].unjani_21), q[0].unjani_21, q[1].unjani_21, percantik_float(stat.stdev([q[0].unjani_21, q[1].unjani_21])) ],
                [ "22:00", rekomendasi_stok_hari(q[0].unjani_22, q[1].unjani_22), q[0].unjani_22, q[1].unjani_22, percantik_float(stat.stdev([q[0].unjani_22, q[1].unjani_22])) ],
                [ "23:00", rekomendasi_stok_hari(q[0].unjani_23, q[1].unjani_23), q[0].unjani_23, q[1].unjani_23, percantik_float(stat.stdev([q[0].unjani_23, q[1].unjani_23])) ],
                [ "24:00", rekomendasi_stok_hari(q[0].unjani_24, q[1].unjani_24), q[0].unjani_24, q[1].unjani_24, percantik_float(stat.stdev([q[0].unjani_24, q[1].unjani_24])) ],
            ],

            "Sukajadi" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                [ "1:00", rekomendasi_stok_hari(q[0].sukajadi_1, q[1].sukajadi_1), q[0].sukajadi_1, q[1].sukajadi_1, percantik_float(stat.stdev([q[0].sukajadi_1, q[1].sukajadi_1])) ],
                [ "2:00", rekomendasi_stok_hari(q[0].sukajadi_2, q[1].sukajadi_2), q[0].sukajadi_2, q[1].sukajadi_2, percantik_float(stat.stdev([q[0].sukajadi_2, q[1].sukajadi_2])) ],
                [ "3:00", rekomendasi_stok_hari(q[0].sukajadi_3, q[1].sukajadi_3), q[0].sukajadi_3, q[1].sukajadi_3, percantik_float(stat.stdev([q[0].sukajadi_3, q[1].sukajadi_3])) ],
                [ "9:00", rekomendasi_stok_hari(q[0].sukajadi_9, q[1].sukajadi_9), q[0].sukajadi_9, q[1].sukajadi_9, percantik_float(stat.stdev([q[0].sukajadi_9, q[1].sukajadi_9])) ],
                [ "10:00", rekomendasi_stok_hari(q[0].sukajadi_10, q[1].sukajadi_10), q[0].sukajadi_10, q[1].sukajadi_10, percantik_float(stat.stdev([q[0].sukajadi_10, q[1].sukajadi_10])) ],
                [ "11:00", rekomendasi_stok_hari(q[0].sukajadi_11, q[1].sukajadi_11), q[0].sukajadi_11, q[1].sukajadi_11, percantik_float(stat.stdev([q[0].sukajadi_11, q[1].sukajadi_11])) ],
                [ "12:00", rekomendasi_stok_hari(q[0].sukajadi_12, q[1].sukajadi_12), q[0].sukajadi_12, q[1].sukajadi_12, percantik_float(stat.stdev([q[0].sukajadi_12, q[1].sukajadi_12])) ],
                [ "13:00", rekomendasi_stok_hari(q[0].sukajadi_13, q[1].sukajadi_13), q[0].sukajadi_13, q[1].sukajadi_13, percantik_float(stat.stdev([q[0].sukajadi_13, q[1].sukajadi_13])) ],
                [ "14:00", rekomendasi_stok_hari(q[0].sukajadi_14, q[1].sukajadi_14), q[0].sukajadi_14, q[1].sukajadi_14, percantik_float(stat.stdev([q[0].sukajadi_14, q[1].sukajadi_14])) ],
                [ "15:00", rekomendasi_stok_hari(q[0].sukajadi_15, q[1].sukajadi_15), q[0].sukajadi_15, q[1].sukajadi_15, percantik_float(stat.stdev([q[0].sukajadi_15, q[1].sukajadi_15])) ],
                [ "16:00", rekomendasi_stok_hari(q[0].sukajadi_16, q[1].sukajadi_16), q[0].sukajadi_16, q[1].sukajadi_16, percantik_float(stat.stdev([q[0].sukajadi_16, q[1].sukajadi_16])) ],
                [ "17:00", rekomendasi_stok_hari(q[0].sukajadi_17, q[1].sukajadi_17), q[0].sukajadi_17, q[1].sukajadi_17, percantik_float(stat.stdev([q[0].sukajadi_17, q[1].sukajadi_17])) ],
                [ "18:00", rekomendasi_stok_hari(q[0].sukajadi_18, q[1].sukajadi_18), q[0].sukajadi_18, q[1].sukajadi_18, percantik_float(stat.stdev([q[0].sukajadi_18, q[1].sukajadi_18])) ],
                [ "19:00", rekomendasi_stok_hari(q[0].sukajadi_19, q[1].sukajadi_19), q[0].sukajadi_19, q[1].sukajadi_19, percantik_float(stat.stdev([q[0].sukajadi_19, q[1].sukajadi_19])) ],
                [ "20:00", rekomendasi_stok_hari(q[0].sukajadi_20, q[1].sukajadi_20), q[0].sukajadi_20, q[1].sukajadi_20, percantik_float(stat.stdev([q[0].sukajadi_20, q[1].sukajadi_20])) ],
                [ "21:00", rekomendasi_stok_hari(q[0].sukajadi_21, q[1].sukajadi_21), q[0].sukajadi_21, q[1].sukajadi_21, percantik_float(stat.stdev([q[0].sukajadi_21, q[1].sukajadi_21])) ],
                [ "22:00", rekomendasi_stok_hari(q[0].sukajadi_22, q[1].sukajadi_22), q[0].sukajadi_22, q[1].sukajadi_22, percantik_float(stat.stdev([q[0].sukajadi_22, q[1].sukajadi_22])) ],
                [ "23:00", rekomendasi_stok_hari(q[0].sukajadi_23, q[1].sukajadi_23), q[0].sukajadi_23, q[1].sukajadi_23, percantik_float(stat.stdev([q[0].sukajadi_23, q[1].sukajadi_23])) ],
                [ "24:00", rekomendasi_stok_hari(q[0].sukajadi_24, q[1].sukajadi_24), q[0].sukajadi_24, q[1].sukajadi_24, percantik_float(stat.stdev([q[0].sukajadi_24, q[1].sukajadi_24])) ],
            ],
        }

    return querynya

    