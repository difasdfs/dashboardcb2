from dashboard.models import AssemblyProduct
from .models import KategoriLoyverse
import requests
import json

def main():
    baseUrl = 'https://api.loyverse.com/v1.0/items'
    access_token = '4a3e5665ac324711b13d677c8c05cac8'
    header = {'Authorization' : 'Bearer ' + access_token}
    payload = {
        'limit' : 250
        }
    respon = requests.get(baseUrl, headers=header, params=payload)
    hasil = json.loads(respon.text)

    i = 0
    sku_ga_ada = []
    # Perulangan tarik API
    while True:
        if "cursor" in hasil.keys():

            for item in hasil['items']:
                idnya = item['id']
                namanya = item['item_name']
                
                object_kategorinya = KategoriLoyverse.objects.get(id_loyverse=item['category_id'])
                kategorinya = object_kategorinya.nama_kategori

                skunya = item['variants'][0]['sku']

                if not AssemblyProduct.objects.filter(sku=skunya, nama= namanya, kategori = kategorinya).exists():
                    # print(str(i) + ". " + namanya + " - " + skunya + " - " + kategorinya)
                    sku_ga_ada.append(
                        {"nama" : namanya, "sku" : skunya, "kategori" : kategorinya}
                    )
                else:
                    continue

                i += 1

            respon = requests.get(baseUrl, headers=header, params={'cursor' : hasil['cursor']})
            hasil = json.loads(respon.text)
        else:
            
            for item in hasil['items']:
                idnya = item['id']
                namanya = item['item_name']

                object_kategorinya = KategoriLoyverse.objects.get(id_loyverse=item['category_id'])
                kategorinya = object_kategorinya.nama_kategori

                skunya = item['variants'][0]['sku']

                if not AssemblyProduct.objects.filter(sku=skunya, nama= namanya, kategori = kategorinya).exists():
                    # print(str(i) + ". " + namanya + " - " + skunya + " - " + kategorinya)
                    sku_ga_ada.append(
                        {"nama" : namanya, "sku" : skunya, "kategori" : kategorinya}
                    )
                else:
                    continue

                i += 1

            break
    
    return sku_ga_ada