from .models import HariProduksi, AssemblyProduct
from datetime import datetime, timedelta
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

    objek_hari_produksi = HariProduksi.objects.get(tanggal=tanggalnya)
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

    for jam in jamnya():
        eksekusi_struk_sehari(tanggal, jam)