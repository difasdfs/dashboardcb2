from .models import HariProduksi, AssemblyProduct
from datetime import datetime, timedelta, date
import statistics as stat
import pytz
import requests
import json
import math

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
        jamnya = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0]
    else:
        jamnya = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0, 1, 2, 3]

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

def rekomendasi_stok_hari(seminggu_lalu, dua_minggu_lalu, tiga_minggu_lalu=0, empat_minggu_lalu=0):
    if tiga_minggu_lalu == 0:
        ratarata = (seminggu_lalu+dua_minggu_lalu)/2
        deviasi = stat.stdev([seminggu_lalu, dua_minggu_lalu])
    elif empat_minggu_lalu == 0:
        ratarata = (seminggu_lalu+dua_minggu_lalu+tiga_minggu_lalu)/3
        deviasi = stat.stdev([seminggu_lalu, dua_minggu_lalu,tiga_minggu_lalu])
    else:
        ratarata = (seminggu_lalu+dua_minggu_lalu+tiga_minggu_lalu+empat_minggu_lalu)/4
        deviasi = stat.stdev([seminggu_lalu, dua_minggu_lalu, tiga_minggu_lalu+empat_minggu_lalu])
    
    konstanta = 1
    hasil = ratarata + (deviasi * konstanta)

    return math.ceil(hasil)

def query_produksi_ayam(harinya):
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
    hari_ini_hari_apa = rumus_hari[str(harinya.weekday())]
    satu_minggu_lalu = harinya - timedelta(days=7)
    dua_minggu_lalu = harinya - timedelta(days=14)
    tiga_minggu_lalu = harinya - timedelta(days=21)

    q = [HariProduksi.objects.get(hari=satu_minggu_lalu), HariProduksi.objects.get(hari=dua_minggu_lalu), HariProduksi.objects.get(hari=tiga_minggu_lalu)]

    querynya = {
            "Hari" : hari_ini_hari_apa,
            "Tanggal" : harinya,
            "Antapani" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                rekomendasi_stok_hari(q[0].antapani_1, q[1].antapani_1, q[2].antapani_1),
                rekomendasi_stok_hari(q[0].antapani_2, q[1].antapani_2, q[2].antapani_2),
                rekomendasi_stok_hari(q[0].antapani_3, q[1].antapani_3, q[2].antapani_3),
                rekomendasi_stok_hari(q[0].antapani_9, q[1].antapani_9, q[2].antapani_9),
                rekomendasi_stok_hari(q[0].antapani_10, q[1].antapani_10, q[2].antapani_10),
                rekomendasi_stok_hari(q[0].antapani_11, q[1].antapani_11, q[2].antapani_11),
                rekomendasi_stok_hari(q[0].antapani_12, q[1].antapani_12, q[2].antapani_12),
                rekomendasi_stok_hari(q[0].antapani_13, q[1].antapani_13, q[2].antapani_13),
                rekomendasi_stok_hari(q[0].antapani_14, q[1].antapani_14, q[2].antapani_14),
                rekomendasi_stok_hari(q[0].antapani_15, q[1].antapani_15, q[2].antapani_15),
                rekomendasi_stok_hari(q[0].antapani_16, q[1].antapani_16, q[2].antapani_16),
                rekomendasi_stok_hari(q[0].antapani_17, q[1].antapani_17, q[2].antapani_17),
                rekomendasi_stok_hari(q[0].antapani_18, q[1].antapani_18, q[2].antapani_18),
                rekomendasi_stok_hari(q[0].antapani_19, q[1].antapani_19, q[2].antapani_19),
                rekomendasi_stok_hari(q[0].antapani_20, q[1].antapani_20, q[2].antapani_20),
                rekomendasi_stok_hari(q[0].antapani_21, q[1].antapani_21, q[2].antapani_21),
                rekomendasi_stok_hari(q[0].antapani_22, q[1].antapani_22, q[2].antapani_22),
                rekomendasi_stok_hari(q[0].antapani_23, q[1].antapani_23, q[2].antapani_23),
                rekomendasi_stok_hari(q[0].antapani_24, q[1].antapani_24, q[2].antapani_24),   
            ],
       
            "Jatinangor" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                rekomendasi_stok_hari(q[0].jatinangor_1, q[1].jatinangor_1, q[2].jatinangor_1),
                rekomendasi_stok_hari(q[0].jatinangor_2, q[1].jatinangor_2, q[2].jatinangor_2),
                rekomendasi_stok_hari(q[0].jatinangor_3, q[1].jatinangor_3, q[2].jatinangor_3),
                rekomendasi_stok_hari(q[0].jatinangor_9, q[1].jatinangor_9, q[2].jatinangor_9),
                rekomendasi_stok_hari(q[0].jatinangor_10, q[1].jatinangor_10, q[2].jatinangor_10),
                rekomendasi_stok_hari(q[0].jatinangor_11, q[1].jatinangor_11, q[2].jatinangor_11),
                rekomendasi_stok_hari(q[0].jatinangor_12, q[1].jatinangor_12, q[2].jatinangor_12),
                rekomendasi_stok_hari(q[0].jatinangor_13, q[1].jatinangor_13, q[2].jatinangor_13),
                rekomendasi_stok_hari(q[0].jatinangor_14, q[1].jatinangor_14, q[2].jatinangor_14),
                rekomendasi_stok_hari(q[0].jatinangor_15, q[1].jatinangor_15, q[2].jatinangor_15),
                rekomendasi_stok_hari(q[0].jatinangor_16, q[1].jatinangor_16, q[2].jatinangor_16),
                rekomendasi_stok_hari(q[0].jatinangor_17, q[1].jatinangor_17, q[2].jatinangor_17),
                rekomendasi_stok_hari(q[0].jatinangor_18, q[1].jatinangor_18, q[2].jatinangor_18),
                rekomendasi_stok_hari(q[0].jatinangor_19, q[1].jatinangor_19, q[2].jatinangor_19),
                rekomendasi_stok_hari(q[0].jatinangor_20, q[1].jatinangor_20, q[2].jatinangor_20),
                rekomendasi_stok_hari(q[0].jatinangor_21, q[1].jatinangor_21, q[2].jatinangor_21),
                rekomendasi_stok_hari(q[0].jatinangor_22, q[1].jatinangor_22, q[2].jatinangor_22),
                rekomendasi_stok_hari(q[0].jatinangor_23, q[1].jatinangor_23, q[2].jatinangor_23),
                rekomendasi_stok_hari(q[0].jatinangor_24, q[1].jatinangor_24, q[2].jatinangor_24),
            ],

            "Metro" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                rekomendasi_stok_hari(q[0].metro_1, q[1].metro_1, q[2].metro_1),
                rekomendasi_stok_hari(q[0].metro_2, q[1].metro_2, q[2].metro_2),
                rekomendasi_stok_hari(q[0].metro_3, q[1].metro_3, q[2].metro_3),
                rekomendasi_stok_hari(q[0].metro_9, q[1].metro_9, q[2].metro_9),
                rekomendasi_stok_hari(q[0].metro_10, q[1].metro_10, q[2].metro_10),
                rekomendasi_stok_hari(q[0].metro_11, q[1].metro_11, q[2].metro_11),
                rekomendasi_stok_hari(q[0].metro_12, q[1].metro_12, q[2].metro_12),
                rekomendasi_stok_hari(q[0].metro_13, q[1].metro_13, q[2].metro_13),
                rekomendasi_stok_hari(q[0].metro_14, q[1].metro_14, q[2].metro_14),
                rekomendasi_stok_hari(q[0].metro_15, q[1].metro_15, q[2].metro_15),
                rekomendasi_stok_hari(q[0].metro_16, q[1].metro_16, q[2].metro_16),
                rekomendasi_stok_hari(q[0].metro_17, q[1].metro_17, q[2].metro_17),
                rekomendasi_stok_hari(q[0].metro_18, q[1].metro_18, q[2].metro_18),
                rekomendasi_stok_hari(q[0].metro_19, q[1].metro_19, q[2].metro_19),
                rekomendasi_stok_hari(q[0].metro_20, q[1].metro_20, q[2].metro_20),
                rekomendasi_stok_hari(q[0].metro_21, q[1].metro_21, q[2].metro_21),
                rekomendasi_stok_hari(q[0].metro_22, q[1].metro_22, q[2].metro_22),
                rekomendasi_stok_hari(q[0].metro_23, q[1].metro_23, q[2].metro_23),
                rekomendasi_stok_hari(q[0].metro_24, q[1].metro_24, q[2].metro_24),
            ],
    
            "Sukapura" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                rekomendasi_stok_hari(q[0].sukapura_1, q[1].sukapura_1, q[2].sukapura_1),
                rekomendasi_stok_hari(q[0].sukapura_2, q[1].sukapura_2, q[2].sukapura_2),
                rekomendasi_stok_hari(q[0].sukapura_3, q[1].sukapura_3, q[2].sukapura_3),
                rekomendasi_stok_hari(q[0].sukapura_9, q[1].sukapura_9, q[2].sukapura_9),
                rekomendasi_stok_hari(q[0].sukapura_10, q[1].sukapura_10, q[2].sukapura_10),
                rekomendasi_stok_hari(q[0].sukapura_11, q[1].sukapura_11, q[2].sukapura_11),
                rekomendasi_stok_hari(q[0].sukapura_12, q[1].sukapura_12, q[2].sukapura_12),
                rekomendasi_stok_hari(q[0].sukapura_13, q[1].sukapura_13, q[2].sukapura_13),
                rekomendasi_stok_hari(q[0].sukapura_14, q[1].sukapura_14, q[2].sukapura_14),
                rekomendasi_stok_hari(q[0].sukapura_15, q[1].sukapura_15, q[2].sukapura_15),
                rekomendasi_stok_hari(q[0].sukapura_16, q[1].sukapura_16, q[2].sukapura_16),
                rekomendasi_stok_hari(q[0].sukapura_17, q[1].sukapura_17, q[2].sukapura_17),
                rekomendasi_stok_hari(q[0].sukapura_18, q[1].sukapura_18, q[2].sukapura_18),
                rekomendasi_stok_hari(q[0].sukapura_19, q[1].sukapura_19, q[2].sukapura_19),
                rekomendasi_stok_hari(q[0].sukapura_20, q[1].sukapura_20, q[2].sukapura_20),
                rekomendasi_stok_hari(q[0].sukapura_21, q[1].sukapura_21, q[2].sukapura_21),
                rekomendasi_stok_hari(q[0].sukapura_22, q[1].sukapura_22, q[2].sukapura_22),
                rekomendasi_stok_hari(q[0].sukapura_23, q[1].sukapura_23, q[2].sukapura_23),
                rekomendasi_stok_hari(q[0].sukapura_24, q[1].sukapura_24, q[2].sukapura_24),
            ],

            "Sukabirus" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                rekomendasi_stok_hari(q[0].sukabirus_1, q[1].sukabirus_1, q[2].sukabirus_1),
                rekomendasi_stok_hari(q[0].sukabirus_2, q[1].sukabirus_2, q[2].sukabirus_2),
                rekomendasi_stok_hari(q[0].sukabirus_3, q[1].sukabirus_3, q[2].sukabirus_3),
                rekomendasi_stok_hari(q[0].sukabirus_9, q[1].sukabirus_9, q[2].sukabirus_9),
                rekomendasi_stok_hari(q[0].sukabirus_10, q[1].sukabirus_10, q[2].sukabirus_10),
                rekomendasi_stok_hari(q[0].sukabirus_11, q[1].sukabirus_11, q[2].sukabirus_11),
                rekomendasi_stok_hari(q[0].sukabirus_12, q[1].sukabirus_12, q[2].sukabirus_12),
                rekomendasi_stok_hari(q[0].sukabirus_13, q[1].sukabirus_13, q[2].sukabirus_13),
                rekomendasi_stok_hari(q[0].sukabirus_14, q[1].sukabirus_14, q[2].sukabirus_14),
                rekomendasi_stok_hari(q[0].sukabirus_15, q[1].sukabirus_15, q[2].sukabirus_15),
                rekomendasi_stok_hari(q[0].sukabirus_16, q[1].sukabirus_16, q[2].sukabirus_16),
                rekomendasi_stok_hari(q[0].sukabirus_17, q[1].sukabirus_17, q[2].sukabirus_17),
                rekomendasi_stok_hari(q[0].sukabirus_18, q[1].sukabirus_18, q[2].sukabirus_18),
                rekomendasi_stok_hari(q[0].sukabirus_19, q[1].sukabirus_19, q[2].sukabirus_19),
                rekomendasi_stok_hari(q[0].sukabirus_20, q[1].sukabirus_20, q[2].sukabirus_20),
                rekomendasi_stok_hari(q[0].sukabirus_21, q[1].sukabirus_21, q[2].sukabirus_21),
                rekomendasi_stok_hari(q[0].sukabirus_22, q[1].sukabirus_22, q[2].sukabirus_22),
                rekomendasi_stok_hari(q[0].sukabirus_23, q[1].sukabirus_23, q[2].sukabirus_23),
                rekomendasi_stok_hari(q[0].sukabirus_24, q[1].sukabirus_24, q[2].sukabirus_24),
            ],

            "Unjani" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                rekomendasi_stok_hari(q[0].unjani_1, q[1].unjani_1, q[2].unjani_1),
                rekomendasi_stok_hari(q[0].unjani_2, q[1].unjani_2, q[2].unjani_2),
                rekomendasi_stok_hari(q[0].unjani_3, q[1].unjani_3, q[2].unjani_3),
                rekomendasi_stok_hari(q[0].unjani_9, q[1].unjani_9, q[2].unjani_9),
                rekomendasi_stok_hari(q[0].unjani_10, q[1].unjani_10, q[2].unjani_10),
                rekomendasi_stok_hari(q[0].unjani_11, q[1].unjani_11, q[2].unjani_11),
                rekomendasi_stok_hari(q[0].unjani_12, q[1].unjani_12, q[2].unjani_12),
                rekomendasi_stok_hari(q[0].unjani_13, q[1].unjani_13, q[2].unjani_13),
                rekomendasi_stok_hari(q[0].unjani_14, q[1].unjani_14, q[2].unjani_14),
                rekomendasi_stok_hari(q[0].unjani_15, q[1].unjani_15, q[2].unjani_15),
                rekomendasi_stok_hari(q[0].unjani_16, q[1].unjani_16, q[2].unjani_16),
                rekomendasi_stok_hari(q[0].unjani_17, q[1].unjani_17, q[2].unjani_17),
                rekomendasi_stok_hari(q[0].unjani_18, q[1].unjani_18, q[2].unjani_18),
                rekomendasi_stok_hari(q[0].unjani_19, q[1].unjani_19, q[2].unjani_19),
                rekomendasi_stok_hari(q[0].unjani_20, q[1].unjani_20, q[2].unjani_20),
                rekomendasi_stok_hari(q[0].unjani_21, q[1].unjani_21, q[2].unjani_21),
                rekomendasi_stok_hari(q[0].unjani_22, q[1].unjani_22, q[2].unjani_22),
                rekomendasi_stok_hari(q[0].unjani_23, q[1].unjani_23, q[2].unjani_23),
                rekomendasi_stok_hari(q[0].unjani_24, q[1].unjani_24, q[2].unjani_24),
            ],

            "Cisitu" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                rekomendasi_stok_hari(q[0].cisitu_1, q[1].cisitu_1, q[2].cisitu_1),
                rekomendasi_stok_hari(q[0].cisitu_2, q[1].cisitu_2, q[2].cisitu_2),
                rekomendasi_stok_hari(q[0].cisitu_3, q[1].cisitu_3, q[2].cisitu_3),
                rekomendasi_stok_hari(q[0].cisitu_9, q[1].cisitu_9, q[2].cisitu_9),
                rekomendasi_stok_hari(q[0].cisitu_10, q[1].cisitu_10, q[2].cisitu_10),
                rekomendasi_stok_hari(q[0].cisitu_11, q[1].cisitu_11, q[2].cisitu_11),
                rekomendasi_stok_hari(q[0].cisitu_12, q[1].cisitu_12, q[2].cisitu_12),
                rekomendasi_stok_hari(q[0].cisitu_13, q[1].cisitu_13, q[2].cisitu_13),
                rekomendasi_stok_hari(q[0].cisitu_14, q[1].cisitu_14, q[2].cisitu_14),
                rekomendasi_stok_hari(q[0].cisitu_15, q[1].cisitu_15, q[2].cisitu_15),
                rekomendasi_stok_hari(q[0].cisitu_16, q[1].cisitu_16, q[2].cisitu_16),
                rekomendasi_stok_hari(q[0].cisitu_17, q[1].cisitu_17, q[2].cisitu_17),
                rekomendasi_stok_hari(q[0].cisitu_18, q[1].cisitu_18, q[2].cisitu_18),
                rekomendasi_stok_hari(q[0].cisitu_19, q[1].cisitu_19, q[2].cisitu_19),
                rekomendasi_stok_hari(q[0].cisitu_20, q[1].cisitu_20, q[2].cisitu_20),
                rekomendasi_stok_hari(q[0].cisitu_21, q[1].cisitu_21, q[2].cisitu_21),
                rekomendasi_stok_hari(q[0].unjani_22, q[1].unjani_22, q[2].cisitu_22),
                rekomendasi_stok_hari(q[0].unjani_23, q[1].unjani_23, q[2].cisitu_23),
                rekomendasi_stok_hari(q[0].cisitu_24, q[1].cisitu_24, q[2].cisitu_24),
            ],
            "Sukajadi" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                rekomendasi_stok_hari(q[0].sukajadi_1, q[1].sukajadi_1, q[2].sukajadi_1),
                rekomendasi_stok_hari(q[0].sukajadi_2, q[1].sukajadi_2, q[2].sukajadi_2),
                rekomendasi_stok_hari(q[0].sukajadi_3, q[1].sukajadi_3, q[2].sukajadi_3),
                rekomendasi_stok_hari(q[0].sukajadi_9, q[1].sukajadi_9, q[2].sukajadi_9),
                rekomendasi_stok_hari(q[0].sukajadi_10, q[1].sukajadi_10, q[2].sukajadi_10),
                rekomendasi_stok_hari(q[0].sukajadi_11, q[1].sukajadi_11, q[2].sukajadi_11),
                rekomendasi_stok_hari(q[0].sukajadi_12, q[1].sukajadi_12, q[2].sukajadi_12),
                rekomendasi_stok_hari(q[0].sukajadi_13, q[1].sukajadi_13, q[2].sukajadi_13),
                rekomendasi_stok_hari(q[0].sukajadi_14, q[1].sukajadi_14, q[2].sukajadi_14),
                rekomendasi_stok_hari(q[0].sukajadi_15, q[1].sukajadi_15, q[2].sukajadi_15),
                rekomendasi_stok_hari(q[0].sukajadi_16, q[1].sukajadi_16, q[2].sukajadi_16),
                rekomendasi_stok_hari(q[0].sukajadi_17, q[1].sukajadi_17, q[2].sukajadi_17),
                rekomendasi_stok_hari(q[0].sukajadi_18, q[1].sukajadi_18, q[2].sukajadi_18),
                rekomendasi_stok_hari(q[0].sukajadi_19, q[1].sukajadi_19, q[2].sukajadi_19),
                rekomendasi_stok_hari(q[0].sukajadi_20, q[1].sukajadi_20, q[2].sukajadi_20),
                rekomendasi_stok_hari(q[0].sukajadi_21, q[1].sukajadi_21, q[2].sukajadi_21),
                rekomendasi_stok_hari(q[0].sukajadi_22, q[1].sukajadi_22, q[2].sukajadi_22),
                rekomendasi_stok_hari(q[0].sukajadi_23, q[1].sukajadi_23, q[2].sukajadi_23),
                rekomendasi_stok_hari(q[0].sukajadi_24, q[1].sukajadi_24, q[2].sukajadi_24),
            ],
        }

    return querynya

def query_setelah_puasa(tanggal_hari_ini):
    a = tanggal_hari_ini.weekday() # integer
    if a == 0:
        tanggal = [date(2021, 4, 5), date(2021, 3, 29), date(2021, 3, 22), date(2021, 3, 15)]
        print('senin')
    elif a == 1:
        tanggal = [date(2021, 4, 6), date(2021, 3, 30), date(2021, 3, 23), date(2021, 3, 16)]
        print('selasa')
    elif a == 2:
        tanggal = [date(2021, 4, 7), date(2021, 3, 31), date(2021, 3, 24), date(2021, 3, 17)]
        print('rabu')
    elif a == 3:
        tanggal = [date(2021, 4, 8), date(2021, 4, 1), date(2021, 3, 25), date(2021, 3, 18)]
        print('kamis')
    elif a == 4:
        tanggal = [date(2021, 4, 9), date(2021, 4, 2), date(2021, 3, 26), date(2021, 3, 19)]
        print('jumat')
    elif a == 5:
        tanggal = [date(2021, 4, 10), date(2021, 4, 3), date(2021, 3, 27), date(2021, 3, 20)]
        print('sabtu')
    elif a == 6:
        tanggal = [date(2021, 4, 11), date(2021, 4, 4), date(2021, 3, 28), date(2021, 3, 21)]
        print('minggu')

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
    harinya = tanggal_hari_ini
    hari_ini_hari_apa = rumus_hari[str(harinya.weekday())]

    q = [HariProduksi.objects.get(hari=tanggal[0]), HariProduksi.objects.get(hari=tanggal[1]), HariProduksi.objects.get(hari=tanggal[2]), HariProduksi.objects.get(hari=tanggal[3])]

    querynya = {
            "Hari" : hari_ini_hari_apa,
            "Tanggal" : harinya,
            "Antapani" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                rekomendasi_stok_hari(q[0].antapani_1, q[1].antapani_1, q[2].antapani_1, q[3].antapani_1),
                rekomendasi_stok_hari(q[0].antapani_2, q[1].antapani_2, q[2].antapani_2, q[3].antapani_2),
                rekomendasi_stok_hari(q[0].antapani_3, q[1].antapani_3, q[2].antapani_3, q[3].antapani_3),
                rekomendasi_stok_hari(q[0].antapani_9, q[1].antapani_9, q[2].antapani_9, q[3].antapani_9),
                rekomendasi_stok_hari(q[0].antapani_10, q[1].antapani_10, q[2].antapani_10, q[3].antapani_10),
                rekomendasi_stok_hari(q[0].antapani_11, q[1].antapani_11, q[2].antapani_11, q[3].antapani_11),
                rekomendasi_stok_hari(q[0].antapani_12, q[1].antapani_12, q[2].antapani_12, q[3].antapani_12),
                rekomendasi_stok_hari(q[0].antapani_13, q[1].antapani_13, q[2].antapani_13, q[3].antapani_13),
                rekomendasi_stok_hari(q[0].antapani_14, q[1].antapani_14, q[2].antapani_14, q[3].antapani_14),
                rekomendasi_stok_hari(q[0].antapani_15, q[1].antapani_15, q[2].antapani_15, q[3].antapani_15),
                rekomendasi_stok_hari(q[0].antapani_16, q[1].antapani_16, q[2].antapani_16, q[3].antapani_16),
                rekomendasi_stok_hari(q[0].antapani_17, q[1].antapani_17, q[2].antapani_17, q[3].antapani_17),
                rekomendasi_stok_hari(q[0].antapani_18, q[1].antapani_18, q[2].antapani_18, q[3].antapani_18),
                rekomendasi_stok_hari(q[0].antapani_19, q[1].antapani_19, q[2].antapani_19, q[3].antapani_19),
                rekomendasi_stok_hari(q[0].antapani_20, q[1].antapani_20, q[2].antapani_20, q[3].antapani_20),
                rekomendasi_stok_hari(q[0].antapani_21, q[1].antapani_21, q[2].antapani_21, q[3].antapani_21),
                rekomendasi_stok_hari(q[0].antapani_22, q[1].antapani_22, q[2].antapani_22, q[3].antapani_22),
                rekomendasi_stok_hari(q[0].antapani_23, q[1].antapani_23, q[2].antapani_23, q[3].antapani_23),
                rekomendasi_stok_hari(q[0].antapani_24, q[1].antapani_24, q[2].antapani_24, q[3].antapani_24),   
            ],
       
            "Jatinangor" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                rekomendasi_stok_hari(q[0].jatinangor_1, q[1].jatinangor_1, q[2].jatinangor_1, q[3].jatinangor_1),
                rekomendasi_stok_hari(q[0].jatinangor_2, q[1].jatinangor_2, q[2].jatinangor_2, q[3].jatinangor_2),
                rekomendasi_stok_hari(q[0].jatinangor_3, q[1].jatinangor_3, q[2].jatinangor_3, q[3].jatinangor_3),
                rekomendasi_stok_hari(q[0].jatinangor_9, q[1].jatinangor_9, q[2].jatinangor_9, q[3].jatinangor_9),
                rekomendasi_stok_hari(q[0].jatinangor_10, q[1].jatinangor_10, q[2].jatinangor_10, q[3].jatinangor_10),
                rekomendasi_stok_hari(q[0].jatinangor_11, q[1].jatinangor_11, q[2].jatinangor_11, q[3].jatinangor_11),
                rekomendasi_stok_hari(q[0].jatinangor_12, q[1].jatinangor_12, q[2].jatinangor_12, q[3].jatinangor_12),
                rekomendasi_stok_hari(q[0].jatinangor_13, q[1].jatinangor_13, q[2].jatinangor_13, q[3].jatinangor_13),
                rekomendasi_stok_hari(q[0].jatinangor_14, q[1].jatinangor_14, q[2].jatinangor_14, q[3].jatinangor_14),
                rekomendasi_stok_hari(q[0].jatinangor_15, q[1].jatinangor_15, q[2].jatinangor_15, q[3].jatinangor_15),
                rekomendasi_stok_hari(q[0].jatinangor_16, q[1].jatinangor_16, q[2].jatinangor_16, q[3].jatinangor_16),
                rekomendasi_stok_hari(q[0].jatinangor_17, q[1].jatinangor_17, q[2].jatinangor_17, q[3].jatinangor_17),
                rekomendasi_stok_hari(q[0].jatinangor_18, q[1].jatinangor_18, q[2].jatinangor_18, q[3].jatinangor_18),
                rekomendasi_stok_hari(q[0].jatinangor_19, q[1].jatinangor_19, q[2].jatinangor_19, q[3].jatinangor_19),
                rekomendasi_stok_hari(q[0].jatinangor_20, q[1].jatinangor_20, q[2].jatinangor_20, q[3].jatinangor_20),
                rekomendasi_stok_hari(q[0].jatinangor_21, q[1].jatinangor_21, q[2].jatinangor_21, q[3].jatinangor_21),
                rekomendasi_stok_hari(q[0].jatinangor_22, q[1].jatinangor_22, q[2].jatinangor_22, q[3].jatinangor_22),
                rekomendasi_stok_hari(q[0].jatinangor_23, q[1].jatinangor_23, q[2].jatinangor_23, q[3].jatinangor_23),
                rekomendasi_stok_hari(q[0].jatinangor_24, q[1].jatinangor_24, q[2].jatinangor_24, q[3].jatinangor_24),
            ],

            "Metro" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                rekomendasi_stok_hari(q[0].metro_1, q[1].metro_1, q[2].metro_1, q[3].metro_1),
                rekomendasi_stok_hari(q[0].metro_2, q[1].metro_2, q[2].metro_2, q[3].metro_2),
                rekomendasi_stok_hari(q[0].metro_3, q[1].metro_3, q[2].metro_3, q[3].metro_3),
                rekomendasi_stok_hari(q[0].metro_9, q[1].metro_9, q[2].metro_9, q[3].metro_9),
                rekomendasi_stok_hari(q[0].metro_10, q[1].metro_10, q[2].metro_10, q[3].metro_10),
                rekomendasi_stok_hari(q[0].metro_11, q[1].metro_11, q[2].metro_11, q[3].metro_11),
                rekomendasi_stok_hari(q[0].metro_12, q[1].metro_12, q[2].metro_12, q[3].metro_12),
                rekomendasi_stok_hari(q[0].metro_13, q[1].metro_13, q[2].metro_13, q[3].metro_13),
                rekomendasi_stok_hari(q[0].metro_14, q[1].metro_14, q[2].metro_14, q[3].metro_14),
                rekomendasi_stok_hari(q[0].metro_15, q[1].metro_15, q[2].metro_15, q[3].metro_15),
                rekomendasi_stok_hari(q[0].metro_16, q[1].metro_16, q[2].metro_16, q[3].metro_16),
                rekomendasi_stok_hari(q[0].metro_17, q[1].metro_17, q[2].metro_17, q[3].metro_17),
                rekomendasi_stok_hari(q[0].metro_18, q[1].metro_18, q[2].metro_18, q[3].metro_18),
                rekomendasi_stok_hari(q[0].metro_19, q[1].metro_19, q[2].metro_19, q[3].metro_19),
                rekomendasi_stok_hari(q[0].metro_20, q[1].metro_20, q[2].metro_20, q[3].metro_20),
                rekomendasi_stok_hari(q[0].metro_21, q[1].metro_21, q[2].metro_21, q[3].metro_21),
                rekomendasi_stok_hari(q[0].metro_22, q[1].metro_22, q[2].metro_22, q[3].metro_22),
                rekomendasi_stok_hari(q[0].metro_23, q[1].metro_23, q[2].metro_23, q[3].metro_23),
                rekomendasi_stok_hari(q[0].metro_24, q[1].metro_24, q[2].metro_24, q[3].metro_24),
            ],
    
            "Sukapura" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                rekomendasi_stok_hari(q[0].sukapura_1, q[1].sukapura_1, q[2].sukapura_1, q[3].sukapura_1),
                rekomendasi_stok_hari(q[0].sukapura_2, q[1].sukapura_2, q[2].sukapura_2, q[3].sukapura_2),
                rekomendasi_stok_hari(q[0].sukapura_3, q[1].sukapura_3, q[2].sukapura_3, q[3].sukapura_3),
                rekomendasi_stok_hari(q[0].sukapura_9, q[1].sukapura_9, q[2].sukapura_9, q[3].sukapura_9),
                rekomendasi_stok_hari(q[0].sukapura_10, q[1].sukapura_10, q[2].sukapura_10, q[3].sukapura_10),
                rekomendasi_stok_hari(q[0].sukapura_11, q[1].sukapura_11, q[2].sukapura_11, q[3].sukapura_11),
                rekomendasi_stok_hari(q[0].sukapura_12, q[1].sukapura_12, q[2].sukapura_12, q[3].sukapura_12),
                rekomendasi_stok_hari(q[0].sukapura_13, q[1].sukapura_13, q[2].sukapura_13, q[3].sukapura_13),
                rekomendasi_stok_hari(q[0].sukapura_14, q[1].sukapura_14, q[2].sukapura_14, q[3].sukapura_14),
                rekomendasi_stok_hari(q[0].sukapura_15, q[1].sukapura_15, q[2].sukapura_15, q[3].sukapura_15),
                rekomendasi_stok_hari(q[0].sukapura_16, q[1].sukapura_16, q[2].sukapura_16, q[3].sukapura_16),
                rekomendasi_stok_hari(q[0].sukapura_17, q[1].sukapura_17, q[2].sukapura_17, q[3].sukapura_17),
                rekomendasi_stok_hari(q[0].sukapura_18, q[1].sukapura_18, q[2].sukapura_18, q[3].sukapura_18),
                rekomendasi_stok_hari(q[0].sukapura_19, q[1].sukapura_19, q[2].sukapura_19, q[3].sukapura_19),
                rekomendasi_stok_hari(q[0].sukapura_20, q[1].sukapura_20, q[2].sukapura_20, q[3].sukapura_20),
                rekomendasi_stok_hari(q[0].sukapura_21, q[1].sukapura_21, q[2].sukapura_21, q[3].sukapura_21),
                rekomendasi_stok_hari(q[0].sukapura_22, q[1].sukapura_22, q[2].sukapura_22, q[3].sukapura_22),
                rekomendasi_stok_hari(q[0].sukapura_23, q[1].sukapura_23, q[2].sukapura_23, q[3].sukapura_23),
                rekomendasi_stok_hari(q[0].sukapura_24, q[1].sukapura_24, q[2].sukapura_24, q[3].sukapura_24),
            ],

            "Sukabirus" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                rekomendasi_stok_hari(q[0].sukabirus_1, q[1].sukabirus_1, q[2].sukabirus_1, q[3].sukabirus_1),
                rekomendasi_stok_hari(q[0].sukabirus_2, q[1].sukabirus_2, q[2].sukabirus_2, q[3].sukabirus_2),
                rekomendasi_stok_hari(q[0].sukabirus_3, q[1].sukabirus_3, q[2].sukabirus_3, q[3].sukabirus_3),
                rekomendasi_stok_hari(q[0].sukabirus_9, q[1].sukabirus_9, q[2].sukabirus_9, q[3].sukabirus_9),
                rekomendasi_stok_hari(q[0].sukabirus_10, q[1].sukabirus_10, q[2].sukabirus_10, q[3].sukabirus_10),
                rekomendasi_stok_hari(q[0].sukabirus_11, q[1].sukabirus_11, q[2].sukabirus_11, q[3].sukabirus_11),
                rekomendasi_stok_hari(q[0].sukabirus_12, q[1].sukabirus_12, q[2].sukabirus_12, q[3].sukabirus_12),
                rekomendasi_stok_hari(q[0].sukabirus_13, q[1].sukabirus_13, q[2].sukabirus_13, q[3].sukabirus_13),
                rekomendasi_stok_hari(q[0].sukabirus_14, q[1].sukabirus_14, q[2].sukabirus_14, q[3].sukabirus_14),
                rekomendasi_stok_hari(q[0].sukabirus_15, q[1].sukabirus_15, q[2].sukabirus_15, q[3].sukabirus_15),
                rekomendasi_stok_hari(q[0].sukabirus_16, q[1].sukabirus_16, q[2].sukabirus_16, q[3].sukabirus_16),
                rekomendasi_stok_hari(q[0].sukabirus_17, q[1].sukabirus_17, q[2].sukabirus_17, q[3].sukabirus_17),
                rekomendasi_stok_hari(q[0].sukabirus_18, q[1].sukabirus_18, q[2].sukabirus_18, q[3].sukabirus_18),
                rekomendasi_stok_hari(q[0].sukabirus_19, q[1].sukabirus_19, q[2].sukabirus_19, q[3].sukabirus_19),
                rekomendasi_stok_hari(q[0].sukabirus_20, q[1].sukabirus_20, q[2].sukabirus_20, q[3].sukabirus_20),
                rekomendasi_stok_hari(q[0].sukabirus_21, q[1].sukabirus_21, q[2].sukabirus_21, q[3].sukabirus_21),
                rekomendasi_stok_hari(q[0].sukabirus_22, q[1].sukabirus_22, q[2].sukabirus_22, q[3].sukabirus_22),
                rekomendasi_stok_hari(q[0].sukabirus_23, q[1].sukabirus_23, q[2].sukabirus_23, q[3].sukabirus_23),
                rekomendasi_stok_hari(q[0].sukabirus_24, q[1].sukabirus_24, q[2].sukabirus_24, q[3].sukabirus_24),
            ],

            "Unjani" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                rekomendasi_stok_hari(q[0].unjani_1, q[1].unjani_1, q[2].unjani_1, q[3].unjani_1),
                rekomendasi_stok_hari(q[0].unjani_2, q[1].unjani_2, q[2].unjani_2, q[3].unjani_2),
                rekomendasi_stok_hari(q[0].unjani_3, q[1].unjani_3, q[2].unjani_3, q[3].unjani_3),
                rekomendasi_stok_hari(q[0].unjani_9, q[1].unjani_9, q[2].unjani_9, q[3].unjani_9),
                rekomendasi_stok_hari(q[0].unjani_10, q[1].unjani_10, q[2].unjani_10, q[3].unjani_10),
                rekomendasi_stok_hari(q[0].unjani_11, q[1].unjani_11, q[2].unjani_11, q[3].unjani_11),
                rekomendasi_stok_hari(q[0].unjani_12, q[1].unjani_12, q[2].unjani_12, q[3].unjani_12),
                rekomendasi_stok_hari(q[0].unjani_13, q[1].unjani_13, q[2].unjani_13, q[3].unjani_13),
                rekomendasi_stok_hari(q[0].unjani_14, q[1].unjani_14, q[2].unjani_14, q[3].unjani_14),
                rekomendasi_stok_hari(q[0].unjani_15, q[1].unjani_15, q[2].unjani_15, q[3].unjani_15),
                rekomendasi_stok_hari(q[0].unjani_16, q[1].unjani_16, q[2].unjani_16, q[3].unjani_16),
                rekomendasi_stok_hari(q[0].unjani_17, q[1].unjani_17, q[2].unjani_17, q[3].unjani_17),
                rekomendasi_stok_hari(q[0].unjani_18, q[1].unjani_18, q[2].unjani_18, q[3].unjani_18),
                rekomendasi_stok_hari(q[0].unjani_19, q[1].unjani_19, q[2].unjani_19, q[3].unjani_19),
                rekomendasi_stok_hari(q[0].unjani_20, q[1].unjani_20, q[2].unjani_20, q[3].unjani_20),
                rekomendasi_stok_hari(q[0].unjani_21, q[1].unjani_21, q[2].unjani_21, q[3].unjani_21),
                rekomendasi_stok_hari(q[0].unjani_22, q[1].unjani_22, q[2].unjani_22, q[3].unjani_22),
                rekomendasi_stok_hari(q[0].unjani_23, q[1].unjani_23, q[2].unjani_23, q[3].unjani_23),
                rekomendasi_stok_hari(q[0].unjani_24, q[1].unjani_24, q[2].unjani_24, q[3].unjani_24),
            ],

            "Cisitu" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                rekomendasi_stok_hari(q[0].cisitu_1, q[1].cisitu_1, q[2].cisitu_1, q[3].cisitu_1),
                rekomendasi_stok_hari(q[0].cisitu_2, q[1].cisitu_2, q[2].cisitu_2, q[3].cisitu_2),
                rekomendasi_stok_hari(q[0].cisitu_3, q[1].cisitu_3, q[2].cisitu_3, q[3].cisitu_3),
                rekomendasi_stok_hari(q[0].cisitu_9, q[1].cisitu_9, q[2].cisitu_9, q[3].cisitu_9),
                rekomendasi_stok_hari(q[0].cisitu_10, q[1].cisitu_10, q[2].cisitu_10, q[3].cisitu_10),
                rekomendasi_stok_hari(q[0].cisitu_11, q[1].cisitu_11, q[2].cisitu_11, q[3].cisitu_11),
                rekomendasi_stok_hari(q[0].cisitu_12, q[1].cisitu_12, q[2].cisitu_12, q[3].cisitu_12),
                rekomendasi_stok_hari(q[0].cisitu_13, q[1].cisitu_13, q[2].cisitu_13, q[3].cisitu_13),
                rekomendasi_stok_hari(q[0].cisitu_14, q[1].cisitu_14, q[2].cisitu_14, q[3].cisitu_14),
                rekomendasi_stok_hari(q[0].cisitu_15, q[1].cisitu_15, q[2].cisitu_15, q[3].cisitu_15),
                rekomendasi_stok_hari(q[0].cisitu_16, q[1].cisitu_16, q[2].cisitu_16, q[3].cisitu_16),
                rekomendasi_stok_hari(q[0].cisitu_17, q[1].cisitu_17, q[2].cisitu_17, q[3].cisitu_17),
                rekomendasi_stok_hari(q[0].cisitu_18, q[1].cisitu_18, q[2].cisitu_18, q[3].cisitu_18),
                rekomendasi_stok_hari(q[0].cisitu_19, q[1].cisitu_19, q[2].cisitu_19, q[3].cisitu_19),
                rekomendasi_stok_hari(q[0].cisitu_20, q[1].cisitu_20, q[2].cisitu_20, q[3].cisitu_20),
                rekomendasi_stok_hari(q[0].cisitu_21, q[1].cisitu_21, q[2].cisitu_21, q[3].cisitu_21),
                rekomendasi_stok_hari(q[0].unjani_22, q[1].unjani_22, q[2].cisitu_22, q[3].cisitu_22),
                rekomendasi_stok_hari(q[0].unjani_23, q[1].unjani_23, q[2].cisitu_23, q[3].cisitu_23),
                rekomendasi_stok_hari(q[0].cisitu_24, q[1].cisitu_24, q[2].cisitu_24, q[3].cisitu_24),
            ],
            "Sukajadi" : 
            [   
                # rekomendasi stok, seminggu lalu, 2 minggu lalu, standar deviasi
                rekomendasi_stok_hari(q[0].sukajadi_1, q[1].sukajadi_1, q[2].sukajadi_1, q[3].sukajadi_1),
                rekomendasi_stok_hari(q[0].sukajadi_2, q[1].sukajadi_2, q[2].sukajadi_2, q[3].sukajadi_2),
                rekomendasi_stok_hari(q[0].sukajadi_3, q[1].sukajadi_3, q[2].sukajadi_3, q[3].sukajadi_3),
                rekomendasi_stok_hari(q[0].sukajadi_9, q[1].sukajadi_9, q[2].sukajadi_9, q[3].sukajadi_9),
                rekomendasi_stok_hari(q[0].sukajadi_10, q[1].sukajadi_10, q[2].sukajadi_10, q[3].sukajadi_10),
                rekomendasi_stok_hari(q[0].sukajadi_11, q[1].sukajadi_11, q[2].sukajadi_11, q[3].sukajadi_11),
                rekomendasi_stok_hari(q[0].sukajadi_12, q[1].sukajadi_12, q[2].sukajadi_12, q[3].sukajadi_12),
                rekomendasi_stok_hari(q[0].sukajadi_13, q[1].sukajadi_13, q[2].sukajadi_13, q[3].sukajadi_13),
                rekomendasi_stok_hari(q[0].sukajadi_14, q[1].sukajadi_14, q[2].sukajadi_14, q[3].sukajadi_14),
                rekomendasi_stok_hari(q[0].sukajadi_15, q[1].sukajadi_15, q[2].sukajadi_15, q[3].sukajadi_15),
                rekomendasi_stok_hari(q[0].sukajadi_16, q[1].sukajadi_16, q[2].sukajadi_16, q[3].sukajadi_16),
                rekomendasi_stok_hari(q[0].sukajadi_17, q[1].sukajadi_17, q[2].sukajadi_17, q[3].sukajadi_17),
                rekomendasi_stok_hari(q[0].sukajadi_18, q[1].sukajadi_18, q[2].sukajadi_18, q[3].sukajadi_18),
                rekomendasi_stok_hari(q[0].sukajadi_19, q[1].sukajadi_19, q[2].sukajadi_19, q[3].sukajadi_19),
                rekomendasi_stok_hari(q[0].sukajadi_20, q[1].sukajadi_20, q[2].sukajadi_20, q[3].sukajadi_20),
                rekomendasi_stok_hari(q[0].sukajadi_21, q[1].sukajadi_21, q[2].sukajadi_21, q[3].sukajadi_21),
                rekomendasi_stok_hari(q[0].sukajadi_22, q[1].sukajadi_22, q[2].sukajadi_22, q[3].sukajadi_22),
                rekomendasi_stok_hari(q[0].sukajadi_23, q[1].sukajadi_23, q[2].sukajadi_23, q[3].sukajadi_23),
                rekomendasi_stok_hari(q[0].sukajadi_24, q[1].sukajadi_24, q[2].sukajadi_24, q[3].sukajadi_24),
            ],
        }

    return querynya

def coba_query():
    hari_0 = query_setelah_puasa(date.today())
    hari_1 = query_setelah_puasa(date.today() + timedelta(days=1))
    hari_2 = query_setelah_puasa(date.today() + timedelta(days=2))
    hari_3 = query_setelah_puasa(date.today() + timedelta(days=3))
    hari_4 = query_setelah_puasa(date.today() + timedelta(days=4))
    hari_5 = query_setelah_puasa(date.today() + timedelta(days=5))
    hari_6 = query_setelah_puasa(date.today() + timedelta(days=6))

    header = [
        "Jam", 
        [hari_0["Hari"], hari_0["Tanggal"]], 
        [hari_1["Hari"], hari_1["Tanggal"]], 
        [hari_2["Hari"], hari_2["Tanggal"]], 
        [hari_3["Hari"], hari_3["Tanggal"]],
        [hari_4["Hari"], hari_4["Tanggal"]],
        [hari_5["Hari"], hari_5["Tanggal"]],
        [hari_6["Hari"], hari_6["Tanggal"]],
        ]

    isi = {
        "Antapani" :
        [ 
            [ "9:00", hari_0["Antapani"][3], hari_1["Antapani"][3], hari_2["Antapani"][3], hari_3["Antapani"][3], hari_4["Antapani"][3], hari_5["Antapani"][3], hari_6["Antapani"][3] ],
            [ "10:00", hari_0["Antapani"][4], hari_1["Antapani"][4], hari_2["Antapani"][4], hari_3["Antapani"][4], hari_4["Antapani"][4], hari_5["Antapani"][4], hari_6["Antapani"][4] ],
            [ "11:00", hari_0["Antapani"][5], hari_1["Antapani"][5], hari_2["Antapani"][5], hari_3["Antapani"][5], hari_4["Antapani"][5], hari_5["Antapani"][5], hari_6["Antapani"][5] ],
            [ "12:00", hari_0["Antapani"][6], hari_1["Antapani"][6], hari_2["Antapani"][6], hari_3["Antapani"][6], hari_4["Antapani"][6], hari_5["Antapani"][6], hari_6["Antapani"][6] ],
            [ "13:00", hari_0["Antapani"][7], hari_1["Antapani"][7], hari_2["Antapani"][7], hari_3["Antapani"][7], hari_4["Antapani"][7], hari_5["Antapani"][7], hari_6["Antapani"][7] ],
            [ "14:00", hari_0["Antapani"][8], hari_1["Antapani"][8], hari_2["Antapani"][8], hari_3["Antapani"][8], hari_4["Antapani"][8], hari_5["Antapani"][8], hari_6["Antapani"][8] ],
            [ "15:00", hari_0["Antapani"][9], hari_1["Antapani"][9], hari_2["Antapani"][9], hari_3["Antapani"][9], hari_4["Antapani"][9], hari_5["Antapani"][9], hari_6["Antapani"][9] ],
            [ "16:00", hari_0["Antapani"][10], hari_1["Antapani"][10], hari_2["Antapani"][10], hari_3["Antapani"][10], hari_4["Antapani"][10], hari_5["Antapani"][10], hari_6["Antapani"][10] ],
            [ "17:00", hari_0["Antapani"][11], hari_1["Antapani"][11], hari_2["Antapani"][11], hari_3["Antapani"][11], hari_4["Antapani"][11], hari_5["Antapani"][11], hari_6["Antapani"][11] ],
            [ "18:00", hari_0["Antapani"][12], hari_1["Antapani"][12], hari_2["Antapani"][12], hari_3["Antapani"][12], hari_4["Antapani"][12], hari_5["Antapani"][12], hari_6["Antapani"][12] ],
            [ "19:00", hari_0["Antapani"][13], hari_1["Antapani"][13], hari_2["Antapani"][13], hari_3["Antapani"][13], hari_4["Antapani"][13], hari_5["Antapani"][13], hari_6["Antapani"][13] ],
            [ "20:00", hari_0["Antapani"][14], hari_1["Antapani"][14], hari_2["Antapani"][14], hari_3["Antapani"][14], hari_4["Antapani"][14], hari_5["Antapani"][14], hari_6["Antapani"][14] ],
            [ "21:00", hari_0["Antapani"][15], hari_1["Antapani"][15], hari_2["Antapani"][15], hari_3["Antapani"][15], hari_4["Antapani"][15], hari_5["Antapani"][15], hari_6["Antapani"][15] ],
            [ "22:00", hari_0["Antapani"][16], hari_1["Antapani"][16], hari_2["Antapani"][16], hari_3["Antapani"][16], hari_4["Antapani"][16], hari_5["Antapani"][16], hari_6["Antapani"][16] ],
            [ "23:00", hari_0["Antapani"][17], hari_1["Antapani"][17], hari_2["Antapani"][17], hari_3["Antapani"][17], hari_4["Antapani"][17], hari_5["Antapani"][17], hari_6["Antapani"][17] ],
            [ "24:00", hari_0["Antapani"][18], hari_1["Antapani"][18], hari_2["Antapani"][18], hari_3["Antapani"][18], hari_4["Antapani"][18], hari_5["Antapani"][18], hari_6["Antapani"][18] ],
        ],

        "Jatinangor" : 
        [
            [ "9:00", hari_0["Jatinangor"][3], hari_1["Jatinangor"][3], hari_2["Jatinangor"][3], hari_3["Jatinangor"][3], hari_4["Jatinangor"][3], hari_5["Jatinangor"][3], hari_6["Jatinangor"][3] ],
            [ "10:00", hari_0["Jatinangor"][4], hari_1["Jatinangor"][4], hari_2["Jatinangor"][4], hari_3["Jatinangor"][4], hari_4["Jatinangor"][4], hari_5["Jatinangor"][4], hari_6["Jatinangor"][4] ],
            [ "11:00", hari_0["Jatinangor"][5], hari_1["Jatinangor"][5], hari_2["Jatinangor"][5], hari_3["Jatinangor"][5], hari_4["Jatinangor"][5], hari_5["Jatinangor"][5], hari_6["Jatinangor"][5] ],
            [ "12:00", hari_0["Jatinangor"][6], hari_1["Jatinangor"][6], hari_2["Jatinangor"][6], hari_3["Jatinangor"][6], hari_4["Jatinangor"][6], hari_5["Jatinangor"][6], hari_6["Jatinangor"][6] ],
            [ "13:00", hari_0["Jatinangor"][7], hari_1["Jatinangor"][7], hari_2["Jatinangor"][7], hari_3["Jatinangor"][7], hari_4["Jatinangor"][7], hari_5["Jatinangor"][7], hari_6["Jatinangor"][7] ],
            [ "14:00", hari_0["Jatinangor"][8], hari_1["Jatinangor"][8], hari_2["Jatinangor"][8], hari_3["Jatinangor"][8], hari_4["Jatinangor"][8], hari_5["Jatinangor"][8], hari_6["Jatinangor"][8] ],
            [ "15:00", hari_0["Jatinangor"][9], hari_1["Jatinangor"][9], hari_2["Jatinangor"][9], hari_3["Jatinangor"][9], hari_4["Jatinangor"][9], hari_5["Jatinangor"][9], hari_6["Jatinangor"][9] ],
            [ "16:00", hari_0["Jatinangor"][10], hari_1["Jatinangor"][10], hari_2["Jatinangor"][10], hari_3["Jatinangor"][10], hari_4["Jatinangor"][10], hari_5["Jatinangor"][10], hari_6["Jatinangor"][10] ],
            [ "17:00", hari_0["Jatinangor"][11], hari_1["Jatinangor"][11], hari_2["Jatinangor"][11], hari_3["Jatinangor"][11], hari_4["Jatinangor"][11], hari_5["Jatinangor"][11], hari_6["Jatinangor"][11] ],
            [ "18:00", hari_0["Jatinangor"][12], hari_1["Jatinangor"][12], hari_2["Jatinangor"][12], hari_3["Jatinangor"][12], hari_4["Jatinangor"][12], hari_5["Jatinangor"][12], hari_6["Jatinangor"][12] ],
            [ "19:00", hari_0["Jatinangor"][13], hari_1["Jatinangor"][13], hari_2["Jatinangor"][13], hari_3["Jatinangor"][13], hari_4["Jatinangor"][13], hari_5["Jatinangor"][13], hari_6["Jatinangor"][13] ],
            [ "20:00", hari_0["Jatinangor"][14], hari_1["Jatinangor"][14], hari_2["Jatinangor"][14], hari_3["Jatinangor"][14], hari_4["Jatinangor"][14], hari_5["Jatinangor"][14], hari_6["Jatinangor"][14] ],
            [ "21:00", hari_0["Jatinangor"][15], hari_1["Jatinangor"][15], hari_2["Jatinangor"][15], hari_3["Jatinangor"][15], hari_4["Jatinangor"][15], hari_5["Jatinangor"][15], hari_6["Jatinangor"][15] ],
            [ "22:00", hari_0["Jatinangor"][16], hari_1["Jatinangor"][16], hari_2["Jatinangor"][16], hari_3["Jatinangor"][16], hari_4["Jatinangor"][16], hari_5["Jatinangor"][16], hari_6["Jatinangor"][16] ],
            [ "23:00", hari_0["Jatinangor"][17], hari_1["Jatinangor"][17], hari_2["Jatinangor"][17], hari_3["Jatinangor"][17], hari_4["Jatinangor"][17], hari_5["Jatinangor"][17], hari_6["Jatinangor"][17] ],
            [ "24:00", hari_0["Jatinangor"][18], hari_1["Jatinangor"][18], hari_2["Jatinangor"][18], hari_3["Jatinangor"][18], hari_4["Jatinangor"][18], hari_5["Jatinangor"][18], hari_6["Jatinangor"][18] ],
        ],

        "Metro" :
        [
            [ "9:00", hari_0["Metro"][3], hari_1["Metro"][3], hari_2["Metro"][3], hari_3["Metro"][3], hari_4["Metro"][3], hari_5["Metro"][3], hari_6["Metro"][3] ],
            [ "10:00", hari_0["Metro"][4], hari_1["Metro"][4], hari_2["Metro"][4], hari_3["Metro"][4], hari_4["Metro"][4], hari_5["Metro"][4], hari_6["Metro"][4] ],
            [ "11:00", hari_0["Metro"][5], hari_1["Metro"][5], hari_2["Metro"][5], hari_3["Metro"][5], hari_4["Metro"][5], hari_5["Metro"][5], hari_6["Metro"][5] ],
            [ "12:00", hari_0["Metro"][6], hari_1["Metro"][6], hari_2["Metro"][6], hari_3["Metro"][6], hari_4["Metro"][6], hari_5["Metro"][6], hari_6["Metro"][6] ],
            [ "13:00", hari_0["Metro"][7], hari_1["Metro"][7], hari_2["Metro"][7], hari_3["Metro"][7], hari_4["Metro"][7], hari_5["Metro"][7], hari_6["Metro"][7] ],
            [ "14:00", hari_0["Metro"][8], hari_1["Metro"][8], hari_2["Metro"][8], hari_3["Metro"][8], hari_4["Metro"][8], hari_5["Metro"][8], hari_6["Metro"][8] ],
            [ "15:00", hari_0["Metro"][9], hari_1["Metro"][9], hari_2["Metro"][9], hari_3["Metro"][9], hari_4["Metro"][9], hari_5["Metro"][9], hari_6["Metro"][9] ],
            [ "16:00", hari_0["Metro"][10], hari_1["Metro"][10], hari_2["Metro"][10], hari_3["Metro"][10], hari_4["Metro"][10], hari_5["Metro"][10], hari_6["Metro"][10] ],
            [ "17:00", hari_0["Metro"][11], hari_1["Metro"][11], hari_2["Metro"][11], hari_3["Metro"][11], hari_4["Metro"][11], hari_5["Metro"][11], hari_6["Metro"][11] ],
            [ "18:00", hari_0["Metro"][12], hari_1["Metro"][12], hari_2["Metro"][12], hari_3["Metro"][12], hari_4["Metro"][12], hari_5["Metro"][12], hari_6["Metro"][12] ],
            [ "19:00", hari_0["Metro"][13], hari_1["Metro"][13], hari_2["Metro"][13], hari_3["Metro"][13], hari_4["Metro"][13], hari_5["Metro"][13], hari_6["Metro"][13] ],
            [ "20:00", hari_0["Metro"][14], hari_1["Metro"][14], hari_2["Metro"][14], hari_3["Metro"][14], hari_4["Metro"][14], hari_5["Metro"][14], hari_6["Metro"][14] ],
            [ "21:00", hari_0["Metro"][15], hari_1["Metro"][15], hari_2["Metro"][15], hari_3["Metro"][15], hari_4["Metro"][15], hari_5["Metro"][15], hari_6["Metro"][15] ],
            [ "22:00", hari_0["Metro"][16], hari_1["Metro"][16], hari_2["Metro"][16], hari_3["Metro"][16], hari_4["Metro"][16], hari_5["Metro"][16], hari_6["Metro"][16] ],
            [ "23:00", hari_0["Metro"][17], hari_1["Metro"][17], hari_2["Metro"][17], hari_3["Metro"][17], hari_4["Metro"][17], hari_5["Metro"][17], hari_6["Metro"][17] ],
            [ "24:00", hari_0["Metro"][18], hari_1["Metro"][18], hari_2["Metro"][18], hari_3["Metro"][18], hari_4["Metro"][18], hari_5["Metro"][18], hari_6["Metro"][18] ],
        ],

        "Sukapura" : 
        [
            [ "9:00", hari_0["Sukapura"][3], hari_1["Sukapura"][3], hari_2["Sukapura"][3], hari_3["Sukapura"][3], hari_4["Sukapura"][3], hari_5["Sukapura"][3], hari_6["Sukapura"][3] ],
            [ "10:00", hari_0["Sukapura"][4], hari_1["Sukapura"][4], hari_2["Sukapura"][4], hari_3["Sukapura"][4], hari_4["Sukapura"][4], hari_5["Sukapura"][4], hari_6["Sukapura"][4] ],
            [ "11:00", hari_0["Sukapura"][5], hari_1["Sukapura"][5], hari_2["Sukapura"][5], hari_3["Sukapura"][5], hari_4["Sukapura"][5], hari_5["Sukapura"][5], hari_6["Sukapura"][5] ],
            [ "12:00", hari_0["Sukapura"][6], hari_1["Sukapura"][6], hari_2["Sukapura"][6], hari_3["Sukapura"][6], hari_4["Sukapura"][6], hari_5["Sukapura"][6], hari_6["Sukapura"][6] ],
            [ "13:00", hari_0["Sukapura"][7], hari_1["Sukapura"][7], hari_2["Sukapura"][7], hari_3["Sukapura"][7], hari_4["Sukapura"][7], hari_5["Sukapura"][7], hari_6["Sukapura"][7] ],
            [ "14:00", hari_0["Sukapura"][8], hari_1["Sukapura"][8], hari_2["Sukapura"][8], hari_3["Sukapura"][8], hari_4["Sukapura"][8], hari_5["Sukapura"][8], hari_6["Sukapura"][8] ],
            [ "15:00", hari_0["Sukapura"][9], hari_1["Sukapura"][9], hari_2["Sukapura"][9], hari_3["Sukapura"][9], hari_4["Sukapura"][9], hari_5["Sukapura"][9], hari_6["Sukapura"][9] ],
            [ "16:00", hari_0["Sukapura"][10], hari_1["Sukapura"][10], hari_2["Sukapura"][10], hari_3["Sukapura"][10], hari_4["Sukapura"][10], hari_5["Sukapura"][10], hari_6["Sukapura"][10] ],
            [ "17:00", hari_0["Sukapura"][11], hari_1["Sukapura"][11], hari_2["Sukapura"][11], hari_3["Sukapura"][11], hari_4["Sukapura"][11], hari_5["Sukapura"][11], hari_6["Sukapura"][11] ],
            [ "18:00", hari_0["Sukapura"][12], hari_1["Sukapura"][12], hari_2["Sukapura"][12], hari_3["Sukapura"][12], hari_4["Sukapura"][12], hari_5["Sukapura"][12], hari_6["Sukapura"][12] ],
            [ "19:00", hari_0["Sukapura"][13], hari_1["Sukapura"][13], hari_2["Sukapura"][13], hari_3["Sukapura"][13], hari_4["Sukapura"][13], hari_5["Sukapura"][13], hari_6["Sukapura"][13] ],
            [ "20:00", hari_0["Sukapura"][14], hari_1["Sukapura"][14], hari_2["Sukapura"][14], hari_3["Sukapura"][14], hari_4["Sukapura"][14], hari_5["Sukapura"][14], hari_6["Sukapura"][14] ],
            [ "21:00", hari_0["Sukapura"][15], hari_1["Sukapura"][15], hari_2["Sukapura"][15], hari_3["Sukapura"][15], hari_4["Sukapura"][15], hari_5["Sukapura"][15], hari_6["Sukapura"][15] ],
            [ "22:00", hari_0["Sukapura"][16], hari_1["Sukapura"][16], hari_2["Sukapura"][16], hari_3["Sukapura"][16], hari_4["Sukapura"][16], hari_5["Sukapura"][16], hari_6["Sukapura"][16] ],
            [ "23:00", hari_0["Sukapura"][17], hari_1["Sukapura"][17], hari_2["Sukapura"][17], hari_3["Sukapura"][17], hari_4["Sukapura"][17], hari_5["Sukapura"][17], hari_6["Sukapura"][17] ],
            [ "24:00", hari_0["Sukapura"][18], hari_1["Sukapura"][18], hari_2["Sukapura"][18], hari_3["Sukapura"][18], hari_4["Sukapura"][18], hari_5["Sukapura"][18], hari_6["Sukapura"][18] ],
        ],

        "Sukabirus" : 
        [
            [ "9:00", hari_0["Sukabirus"][3], hari_1["Sukabirus"][3], hari_2["Sukabirus"][3], hari_3["Sukabirus"][3], hari_4["Sukabirus"][3], hari_5["Sukabirus"][3], hari_6["Sukabirus"][3] ],
            [ "10:00", hari_0["Sukabirus"][4], hari_1["Sukabirus"][4], hari_2["Sukabirus"][4], hari_3["Sukabirus"][4], hari_4["Sukabirus"][4], hari_5["Sukabirus"][4], hari_6["Sukabirus"][4] ],
            [ "11:00", hari_0["Sukabirus"][5], hari_1["Sukabirus"][5], hari_2["Sukabirus"][5], hari_3["Sukabirus"][5], hari_4["Sukabirus"][5], hari_5["Sukabirus"][5], hari_6["Sukabirus"][5] ],
            [ "12:00", hari_0["Sukabirus"][6], hari_1["Sukabirus"][6], hari_2["Sukabirus"][6], hari_3["Sukabirus"][6], hari_4["Sukabirus"][6], hari_5["Sukabirus"][6], hari_6["Sukabirus"][6] ],
            [ "13:00", hari_0["Sukabirus"][7], hari_1["Sukabirus"][7], hari_2["Sukabirus"][7], hari_3["Sukabirus"][7], hari_4["Sukabirus"][7], hari_5["Sukabirus"][7], hari_6["Sukabirus"][7] ],
            [ "14:00", hari_0["Sukabirus"][8], hari_1["Sukabirus"][8], hari_2["Sukabirus"][8], hari_3["Sukabirus"][8], hari_4["Sukabirus"][8], hari_5["Sukabirus"][8], hari_6["Sukabirus"][8] ],
            [ "15:00", hari_0["Sukabirus"][9], hari_1["Sukabirus"][9], hari_2["Sukabirus"][9], hari_3["Sukabirus"][9], hari_4["Sukabirus"][9], hari_5["Sukabirus"][9], hari_6["Sukabirus"][9] ],
            [ "16:00", hari_0["Sukabirus"][10], hari_1["Sukabirus"][10], hari_2["Sukabirus"][10], hari_3["Sukabirus"][10], hari_4["Sukabirus"][10], hari_5["Sukabirus"][10], hari_6["Sukabirus"][10] ],
            [ "17:00", hari_0["Sukabirus"][11], hari_1["Sukabirus"][11], hari_2["Sukabirus"][11], hari_3["Sukabirus"][11], hari_4["Sukabirus"][11], hari_5["Sukabirus"][11], hari_6["Sukabirus"][11] ],
            [ "18:00", hari_0["Sukabirus"][12], hari_1["Sukabirus"][12], hari_2["Sukabirus"][12], hari_3["Sukabirus"][12], hari_4["Sukabirus"][12], hari_5["Sukabirus"][12], hari_6["Sukabirus"][12] ],
            [ "19:00", hari_0["Sukabirus"][13], hari_1["Sukabirus"][13], hari_2["Sukabirus"][13], hari_3["Sukabirus"][13], hari_4["Sukabirus"][13], hari_5["Sukabirus"][13], hari_6["Sukabirus"][13] ],
            [ "20:00", hari_0["Sukabirus"][14], hari_1["Sukabirus"][14], hari_2["Sukabirus"][14], hari_3["Sukabirus"][14], hari_4["Sukabirus"][14], hari_5["Sukabirus"][14], hari_6["Sukabirus"][14] ],
            [ "21:00", hari_0["Sukabirus"][15], hari_1["Sukabirus"][15], hari_2["Sukabirus"][15], hari_3["Sukabirus"][15], hari_4["Sukabirus"][15], hari_5["Sukabirus"][15], hari_6["Sukabirus"][15] ],
            [ "22:00", hari_0["Sukabirus"][16], hari_1["Sukabirus"][16], hari_2["Sukabirus"][16], hari_3["Sukabirus"][16], hari_4["Sukabirus"][16], hari_5["Sukabirus"][16], hari_6["Sukabirus"][16] ],
            [ "23:00", hari_0["Sukabirus"][17], hari_1["Sukabirus"][17], hari_2["Sukabirus"][17], hari_3["Sukabirus"][17], hari_4["Sukabirus"][17], hari_5["Sukabirus"][17], hari_6["Sukabirus"][17] ],
            [ "24:00", hari_0["Sukabirus"][18], hari_1["Sukabirus"][18], hari_2["Sukabirus"][18], hari_3["Sukabirus"][18], hari_4["Sukabirus"][18], hari_5["Sukabirus"][18], hari_6["Sukabirus"][18] ],
        ],

        "Unjani" : 
        [
            [ "9:00", hari_0["Unjani"][3], hari_1["Unjani"][3], hari_2["Unjani"][3], hari_3["Unjani"][3], hari_4["Unjani"][3], hari_5["Unjani"][3], hari_6["Unjani"][3] ],
            [ "10:00", hari_0["Unjani"][4], hari_1["Unjani"][4], hari_2["Unjani"][4], hari_3["Unjani"][4], hari_4["Unjani"][4], hari_5["Unjani"][4], hari_6["Unjani"][4] ],
            [ "11:00", hari_0["Unjani"][5], hari_1["Unjani"][5], hari_2["Unjani"][5], hari_3["Unjani"][5], hari_4["Unjani"][5], hari_5["Unjani"][5], hari_6["Unjani"][5] ],
            [ "12:00", hari_0["Unjani"][6], hari_1["Unjani"][6], hari_2["Unjani"][6], hari_3["Unjani"][6], hari_4["Unjani"][6], hari_5["Unjani"][6], hari_6["Unjani"][6] ],
            [ "13:00", hari_0["Unjani"][7], hari_1["Unjani"][7], hari_2["Unjani"][7], hari_3["Unjani"][7], hari_4["Unjani"][7], hari_5["Unjani"][7], hari_6["Unjani"][7] ],
            [ "14:00", hari_0["Unjani"][8], hari_1["Unjani"][8], hari_2["Unjani"][8], hari_3["Unjani"][8], hari_4["Unjani"][8], hari_5["Unjani"][8], hari_6["Unjani"][8] ],
            [ "15:00", hari_0["Unjani"][9], hari_1["Unjani"][9], hari_2["Unjani"][9], hari_3["Unjani"][9], hari_4["Unjani"][9], hari_5["Unjani"][9], hari_6["Unjani"][9] ],
            [ "16:00", hari_0["Unjani"][10], hari_1["Unjani"][10], hari_2["Unjani"][10], hari_3["Unjani"][10], hari_4["Unjani"][10], hari_5["Unjani"][10], hari_6["Unjani"][10] ],
            [ "17:00", hari_0["Unjani"][11], hari_1["Unjani"][11], hari_2["Unjani"][11], hari_3["Unjani"][11], hari_4["Unjani"][11], hari_5["Unjani"][11], hari_6["Unjani"][11] ],
            [ "18:00", hari_0["Unjani"][12], hari_1["Unjani"][12], hari_2["Unjani"][12], hari_3["Unjani"][12], hari_4["Unjani"][12], hari_5["Unjani"][12], hari_6["Unjani"][12] ],
            [ "19:00", hari_0["Unjani"][13], hari_1["Unjani"][13], hari_2["Unjani"][13], hari_3["Unjani"][13], hari_4["Unjani"][13], hari_5["Unjani"][13], hari_6["Unjani"][13] ],
            [ "20:00", hari_0["Unjani"][14], hari_1["Unjani"][14], hari_2["Unjani"][14], hari_3["Unjani"][14], hari_4["Unjani"][14], hari_5["Unjani"][14], hari_6["Unjani"][14] ],
            [ "21:00", hari_0["Unjani"][15], hari_1["Unjani"][15], hari_2["Unjani"][15], hari_3["Unjani"][15], hari_4["Unjani"][15], hari_5["Unjani"][15], hari_6["Unjani"][15] ],
            [ "22:00", hari_0["Unjani"][16], hari_1["Unjani"][16], hari_2["Unjani"][16], hari_3["Unjani"][16], hari_4["Unjani"][16], hari_5["Unjani"][16], hari_6["Unjani"][16] ],
            [ "23:00", hari_0["Unjani"][17], hari_1["Unjani"][17], hari_2["Unjani"][17], hari_3["Unjani"][17], hari_4["Unjani"][17], hari_5["Unjani"][17], hari_6["Unjani"][17] ],
            [ "24:00", hari_0["Unjani"][18], hari_1["Unjani"][18], hari_2["Unjani"][18], hari_3["Unjani"][18], hari_4["Unjani"][18], hari_5["Unjani"][18], hari_6["Unjani"][18] ],
        ],

        "Cisitu" : 
        [
            [ "9:00", hari_0["Cisitu"][3], hari_1["Cisitu"][3], hari_2["Cisitu"][3], hari_3["Cisitu"][3], hari_4["Cisitu"][3], hari_5["Cisitu"][3], hari_6["Cisitu"][3] ],
            [ "10:00", hari_0["Cisitu"][4], hari_1["Cisitu"][4], hari_2["Cisitu"][4], hari_3["Cisitu"][4], hari_4["Cisitu"][4], hari_5["Cisitu"][4], hari_6["Cisitu"][4] ],
            [ "11:00", hari_0["Cisitu"][5], hari_1["Cisitu"][5], hari_2["Cisitu"][5], hari_3["Cisitu"][5], hari_4["Cisitu"][5], hari_5["Cisitu"][5], hari_6["Cisitu"][5] ],
            [ "12:00", hari_0["Cisitu"][6], hari_1["Cisitu"][6], hari_2["Cisitu"][6], hari_3["Cisitu"][6], hari_4["Cisitu"][6], hari_5["Cisitu"][6], hari_6["Cisitu"][6] ],
            [ "13:00", hari_0["Cisitu"][7], hari_1["Cisitu"][7], hari_2["Cisitu"][7], hari_3["Cisitu"][7], hari_4["Cisitu"][7], hari_5["Cisitu"][7], hari_6["Cisitu"][7] ],
            [ "14:00", hari_0["Cisitu"][8], hari_1["Cisitu"][8], hari_2["Cisitu"][8], hari_3["Cisitu"][8], hari_4["Cisitu"][8], hari_5["Cisitu"][8], hari_6["Cisitu"][8] ],
            [ "15:00", hari_0["Cisitu"][9], hari_1["Cisitu"][9], hari_2["Cisitu"][9], hari_3["Cisitu"][9], hari_4["Cisitu"][9], hari_5["Cisitu"][9], hari_6["Cisitu"][9] ],
            [ "16:00", hari_0["Cisitu"][10], hari_1["Cisitu"][10], hari_2["Cisitu"][10], hari_3["Cisitu"][10], hari_4["Cisitu"][10], hari_5["Cisitu"][10], hari_6["Cisitu"][10] ],
            [ "17:00", hari_0["Cisitu"][11], hari_1["Cisitu"][11], hari_2["Cisitu"][11], hari_3["Cisitu"][11], hari_4["Cisitu"][11], hari_5["Cisitu"][11], hari_6["Cisitu"][11] ],
            [ "18:00", hari_0["Cisitu"][12], hari_1["Cisitu"][12], hari_2["Cisitu"][12], hari_3["Cisitu"][12], hari_4["Cisitu"][12], hari_5["Cisitu"][12], hari_6["Cisitu"][12] ],
            [ "19:00", hari_0["Cisitu"][13], hari_1["Cisitu"][13], hari_2["Cisitu"][13], hari_3["Cisitu"][13], hari_4["Cisitu"][13], hari_5["Cisitu"][13], hari_6["Cisitu"][13] ],
            [ "20:00", hari_0["Cisitu"][14], hari_1["Cisitu"][14], hari_2["Cisitu"][14], hari_3["Cisitu"][14], hari_4["Cisitu"][14], hari_5["Cisitu"][14], hari_6["Cisitu"][14] ],
            [ "21:00", hari_0["Cisitu"][15], hari_1["Cisitu"][15], hari_2["Cisitu"][15], hari_3["Cisitu"][15], hari_4["Cisitu"][15], hari_5["Cisitu"][15], hari_6["Cisitu"][15] ],
            [ "22:00", hari_0["Cisitu"][16], hari_1["Cisitu"][16], hari_2["Cisitu"][16], hari_3["Cisitu"][16], hari_4["Cisitu"][16], hari_5["Cisitu"][16], hari_6["Cisitu"][16] ],
            [ "23:00", hari_0["Cisitu"][17], hari_1["Cisitu"][17], hari_2["Cisitu"][17], hari_3["Cisitu"][17], hari_4["Cisitu"][17], hari_5["Cisitu"][17], hari_6["Cisitu"][17] ],
            [ "24:00", hari_0["Cisitu"][18], hari_1["Cisitu"][18], hari_2["Cisitu"][18], hari_3["Cisitu"][18], hari_4["Cisitu"][18], hari_5["Cisitu"][18], hari_6["Cisitu"][18] ],
        ],

        "Sukajadi" : 
        [
            [ "9:00", hari_0["Sukajadi"][3], hari_1["Sukajadi"][3], hari_2["Sukajadi"][3], hari_3["Sukajadi"][3], hari_4["Sukajadi"][3], hari_5["Sukajadi"][3], hari_6["Sukajadi"][3] ],
            [ "10:00", hari_0["Sukajadi"][4], hari_1["Sukajadi"][4], hari_2["Sukajadi"][4], hari_3["Sukajadi"][4], hari_4["Sukajadi"][4], hari_5["Sukajadi"][4], hari_6["Sukajadi"][4] ],
            [ "11:00", hari_0["Sukajadi"][5], hari_1["Sukajadi"][5], hari_2["Sukajadi"][5], hari_3["Sukajadi"][5], hari_4["Sukajadi"][5], hari_5["Sukajadi"][5], hari_6["Sukajadi"][5] ],
            [ "12:00", hari_0["Sukajadi"][6], hari_1["Sukajadi"][6], hari_2["Sukajadi"][6], hari_3["Sukajadi"][6], hari_4["Sukajadi"][6], hari_5["Sukajadi"][6], hari_6["Sukajadi"][6] ],
            [ "13:00", hari_0["Sukajadi"][7], hari_1["Sukajadi"][7], hari_2["Sukajadi"][7], hari_3["Sukajadi"][7], hari_4["Sukajadi"][7], hari_5["Sukajadi"][7], hari_6["Sukajadi"][7] ],
            [ "14:00", hari_0["Sukajadi"][8], hari_1["Sukajadi"][8], hari_2["Sukajadi"][8], hari_3["Sukajadi"][8], hari_4["Sukajadi"][8], hari_5["Sukajadi"][8], hari_6["Sukajadi"][8] ],
            [ "15:00", hari_0["Sukajadi"][9], hari_1["Sukajadi"][9], hari_2["Sukajadi"][9], hari_3["Sukajadi"][9], hari_4["Sukajadi"][9], hari_5["Sukajadi"][9], hari_6["Sukajadi"][9] ],
            [ "16:00", hari_0["Sukajadi"][10], hari_1["Sukajadi"][10], hari_2["Sukajadi"][10], hari_3["Sukajadi"][10], hari_4["Sukajadi"][10], hari_5["Sukajadi"][10], hari_6["Sukajadi"][10] ],
            [ "17:00", hari_0["Sukajadi"][11], hari_1["Sukajadi"][11], hari_2["Sukajadi"][11], hari_3["Sukajadi"][11], hari_4["Sukajadi"][11], hari_5["Sukajadi"][11], hari_6["Sukajadi"][11] ],
            [ "18:00", hari_0["Sukajadi"][12], hari_1["Sukajadi"][12], hari_2["Sukajadi"][12], hari_3["Sukajadi"][12], hari_4["Sukajadi"][12], hari_5["Sukajadi"][12], hari_6["Sukajadi"][12] ],
            [ "19:00", hari_0["Sukajadi"][13], hari_1["Sukajadi"][13], hari_2["Sukajadi"][13], hari_3["Sukajadi"][13], hari_4["Sukajadi"][13], hari_5["Sukajadi"][13], hari_6["Sukajadi"][13] ],
            [ "20:00", hari_0["Sukajadi"][14], hari_1["Sukajadi"][14], hari_2["Sukajadi"][14], hari_3["Sukajadi"][14], hari_4["Sukajadi"][14], hari_5["Sukajadi"][14], hari_6["Sukajadi"][14] ],
            [ "21:00", hari_0["Sukajadi"][15], hari_1["Sukajadi"][15], hari_2["Sukajadi"][15], hari_3["Sukajadi"][15], hari_4["Sukajadi"][15], hari_5["Sukajadi"][15], hari_6["Sukajadi"][15] ],
            [ "22:00", hari_0["Sukajadi"][16], hari_1["Sukajadi"][16], hari_2["Sukajadi"][16], hari_3["Sukajadi"][16], hari_4["Sukajadi"][16], hari_5["Sukajadi"][16], hari_6["Sukajadi"][16] ],
            [ "23:00", hari_0["Sukajadi"][17], hari_1["Sukajadi"][17], hari_2["Sukajadi"][17], hari_3["Sukajadi"][17], hari_4["Sukajadi"][17], hari_5["Sukajadi"][17], hari_6["Sukajadi"][17] ],
            [ "24:00", hari_0["Sukajadi"][18], hari_1["Sukajadi"][18], hari_2["Sukajadi"][18], hari_3["Sukajadi"][18], hari_4["Sukajadi"][18], hari_5["Sukajadi"][18], hari_6["Sukajadi"][18] ],
        ],
        
    }

    return header, isi