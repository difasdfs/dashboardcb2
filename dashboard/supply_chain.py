from .models import TanggalWeekendWeekdays, PemakaianAyam, AssemblyProduct
from datetime import date, timedelta, datetime
import requests
import json
import pytz

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

def periksa_hari_dalam_pemakaian_ayam():
    kemarin = date.today() - timedelta(days=1)
    kemarin_lusa = date.today() - timedelta(days=2)
    tiga_hari_lalu =  date.today() - timedelta(days=3)

    pa = PemakaianAyam.objects.filter(tanggal=tiga_hari_lalu)
    if not pa:
        p = PemakaianAyam(
            tanggal = tiga_hari_lalu,
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

    pa = PemakaianAyam.objects.filter(tanggal=kemarin_lusa)
    if not pa:
        p = PemakaianAyam(
            tanggal = kemarin_lusa,
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
    
    pa = PemakaianAyam.objects.filter(tanggal=kemarin)
    if not pa:
        p = PemakaianAyam(
            tanggal = kemarin,
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

def awal_akhir_hari_utc(hari):

    """ Menerima hari (date) dan mengembalikan awal akhir dan akhir hari berformat (string) ISO 8601 """

    awal_hari = datetime(hari.year, hari.month, hari.day, 0, 0, 1, tzinfo=pytz.UTC) - timedelta(hours=7)
    akhir_hari = datetime(hari.year, hari.month, hari.day, 23, 59, 59, tzinfo=pytz.UTC) - timedelta(hours=7)

    string_awal_hari = awal_hari.isoformat()[:-6] + ".000Z"
    string_akhir_hari = akhir_hari.isoformat()[:-6] + ".000Z"

    return string_awal_hari, string_akhir_hari

def eksekusi_struk_sehari(tanggalnya):
    objek_pemakaian_ayam = PemakaianAyam.objects.get(tanggal=tanggalnya)
    awal_hari, akhir_hari = awal_akhir_hari_utc( tanggalnya )
    baseUrl = 'https://api.loyverse.com/v1.0/receipts'
    access_token = '4a3e5665ac324711b13d677c8c05cac8'
    header = {'Authorization' : 'Bearer ' + access_token}
    payload = {
        "created_at_min" : awal_hari,
        "created_at_max" : akhir_hari,
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
    objek_pemakaian_ayam.pemakaian_ayam = ayam_antapani + ayam_sukajadi + ayam_cisitu + ayam_jatinangor + ayam_metro + ayam_sukabirus + ayam_unjani + ayam_sukapura
    objek_pemakaian_ayam.pemakaian_ayam_antapani = ayam_antapani
    objek_pemakaian_ayam.pemakaian_ayam_jatinangor = ayam_jatinangor
    objek_pemakaian_ayam.pemakaian_ayam_metro = ayam_metro
    objek_pemakaian_ayam.pemakaian_ayam_sukapura = ayam_sukapura
    objek_pemakaian_ayam.pemakaian_ayam_sukabirus = ayam_sukabirus
    objek_pemakaian_ayam.pemakaian_ayam_unjani = ayam_unjani
    objek_pemakaian_ayam.pemakaian_ayam_cisitu = ayam_cisitu
    objek_pemakaian_ayam.pemakaian_ayam_sukajadi = ayam_sukajadi
    objek_pemakaian_ayam.dieksekusi = True
    objek_pemakaian_ayam.save()

def saring_tanggal_weekend_weekdays():

    """ Mengembalikan (date) 16 tanggal weekend sejak kemarin dan 35 tanggal weekday sejak kemarin """

    hari_kemarin = date.today() - timedelta(days=1)
    hari_lalu = date.today() - timedelta(days=70)

    tanggal_weekend = TanggalWeekendWeekdays.objects.filter(weekend=True, tanggal__range=[hari_lalu, hari_kemarin]).order_by('-tanggal')[:16]
    tanggal_weekday = TanggalWeekendWeekdays.objects.filter(weekend=False, tanggal__range=[hari_lalu, hari_kemarin]).order_by('-tanggal')[:35]
    
    return tanggal_weekend, tanggal_weekday
