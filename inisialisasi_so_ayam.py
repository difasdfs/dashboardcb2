from dashboard.models import AssemblyProduct, PemakaianAyam
from datetime import datetime, timedelta
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
    'faa5442b-711d-11ea-8d93-0603130a05b8' : 'Crisbar Cisitu',
    'b7fdb533-4660-4eb1-b662-cc1c97d78d90' : 'Test IT'
}

def fungsi_inisialisasi():
    f = open("buat_chicken_skin.csv")
    for baris in f.readlines():
        baris = baris.split(',')
        a = AssemblyProduct.objects.get(pk=int(f[0]))
        a.chicken_skin = int(f[-1])
        a.save()
    f.close()

def api_chicken_skin():
    semua_objek_pemakaian_ayam = PemakaianAyam.objects.all()
    
    for objek_pemakaian_ayam in semua_objek_pemakaian_ayam:

        # pemakaian chicken skin pada tanggal ini
        pemakaian_chicken_skin = 0
        pemakaian_chicken_skin_antapani = 0
        pemakaian_chicken_skin_jatinangor = 0
        pemakaian_chicken_skin_metro = 0
        pemakaian_chicken_skin_sukapura = 0
        pemakaian_chicken_skin_sukabirus = 0
        pemakaian_chicken_skin_unjani = 0
        pemakaian_chicken_skin_cisitu = 0
        pemakaian_chicken_skin_sukajadi = 0

        tanggal = objek_pemakaian_ayam.tanggal
        awal_hari = (datetime(tanggal.year, tanggal.month, tanggal.day, 0, 0, 1) - timedelta(hours=7)).isoformat() + '.000Z'
        akhir_hari = (datetime(tanggal.year, tanggal.month, tanggal.day, 23, 59, 59) - timedelta(hours=7)).isoformat() + '.000Z'
        baseUrl = 'https://api.loyverse.com/v1.0/receipts/'
        access_token = '4a3e5665ac324711b13d677c8c05cac8'
        header = {'Authorization' : 'Bearer ' + access_token}
        payload = {
            'created_at_min' : awal_hari,
            'created_at_max' : akhir_hari,
            'limit' : 250
        }
        respon = requests.get(baseUrl, headers=header, params=payload)
        hasil = json.loads(respon.text)

        while True:
            if "cursor" in hasil.keys():
                kumpulan_struk = hasil['receipts']

                for struk in kumpulan_struk:
                    print(struk['created_at'])
                    outlet = rumus_id_outlet[struk['store_id']]
                    
                    for barang in struk['line_items']:
                        item = AssemblyProduct.objects.get(sku=barang['sku'])
                        banyaknya_chicken_skin = barang['quantity'] * item.chicken_skin
                        pemakaian_chicken_skin += banyaknya_chicken_skin

                        if "Antapani" in outlet:
                            pemakaian_chicken_skin_antapani += banyaknya_chicken_skin
                        elif "Jatinangor" in outlet:
                            pemakaian_chicken_skin_jatinangor += banyaknya_chicken_skin
                        elif "Metro" in outlet:
                            pemakaian_chicken_skin_metro += banyaknya_chicken_skin
                        elif "Sukapura" in outlet:
                            pemakaian_chicken_skin_sukapura += banyaknya_chicken_skin
                        elif "Sukabirus" in outlet:
                            pemakaian_chicken_skin_sukabirus += banyaknya_chicken_skin
                        elif "Unjani" in outlet:
                            pemakaian_chicken_skin_unjani += banyaknya_chicken_skin
                        elif "Cisitu" in outlet:
                            pemakaian_chicken_skin_cisitu += banyaknya_chicken_skin
                        elif "Sukajadi" in outlet:
                            pemakaian_chicken_skin_sukajadi += banyaknya_chicken_skin
                        else:
                            continue
                        
                respon = requests.get(baseUrl, headers=header, params={'cursor' : hasil['cursor']})
                hasil = json.loads(respon.text)

            else:
                kumpulan_struk = hasil['receipts']

                for struk in kumpulan_struk:
                    print(struk['created_at'])
                    outlet = rumus_id_outlet[struk['store_id']]

                    for barang in struk['line_items']:
                        item = AssemblyProduct.objects.get(sku=barang['sku'])
                        banyaknya_chicken_skin = barang['quantity'] * item.chicken_skin
                        pemakaian_chicken_skin += banyaknya_chicken_skin

                        if "Antapani" in outlet:
                            pemakaian_chicken_skin_antapani += banyaknya_chicken_skin
                        elif "Jatinangor" in outlet:
                            pemakaian_chicken_skin_jatinangor += banyaknya_chicken_skin
                        elif "Metro" in outlet:
                            pemakaian_chicken_skin_metro += banyaknya_chicken_skin
                        elif "Sukapura" in outlet:
                            pemakaian_chicken_skin_sukapura += banyaknya_chicken_skin
                        elif "Sukabirus" in outlet:
                            pemakaian_chicken_skin_sukabirus += banyaknya_chicken_skin
                        elif "Unjani" in outlet:
                            pemakaian_chicken_skin_unjani += banyaknya_chicken_skin
                        elif "Cisitu" in outlet:
                            pemakaian_chicken_skin_cisitu += banyaknya_chicken_skin
                        elif "Sukajadi" in outlet:
                            pemakaian_chicken_skin_sukajadi += banyaknya_chicken_skin
                        else:
                            continue

                break

            objek_pemakaian_ayam.pemakaian_chicken_skin = pemakaian_chicken_skin
            objek_pemakaian_ayam.pemakaian_chicken_skin_antapani = pemakaian_chicken_skin_antapani
            objek_pemakaian_ayam.pemakaian_chicken_skin_jatinangor = pemakaian_chicken_skin_jatinangor
            objek_pemakaian_ayam.pemakaian_chicken_skin_metro = pemakaian_chicken_skin_metro
            objek_pemakaian_ayam.pemakaian_chicken_skin_sukapura = pemakaian_chicken_skin_sukapura
            objek_pemakaian_ayam.pemakaian_chicken_skin_sukabirus = pemakaian_chicken_skin_sukabirus
            objek_pemakaian_ayam.pemakaian_chicken_skin_unjani = pemakaian_chicken_skin_unjani
            objek_pemakaian_ayam.pemakaian_chicken_skin_cisitu = pemakaian_chicken_skin_cisitu
            objek_pemakaian_ayam.pemakaian_chicken_skin_sukajadi = pemakaian_chicken_skin_sukajadi
            objek_pemakaian_ayam.save()