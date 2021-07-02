import requests
import json

from .models import KategoriLoyverse

# votes_table = Votes.objects.filter(user_id=user_id, post_id= post_id).exists()

ACCESS_TOKEN = '4a3e5665ac324711b13d677c8c05cac8'

def main():

    baseUrl = 'https://api.loyverse.com/v1.0/categories'
    header = {'Authorization' : 'Bearer ' + ACCESS_TOKEN}
    payload = {
        'limit' : 250
        }
    respon = requests.get(baseUrl, headers=header, params=payload)
    hasil = json.loads(respon.text)

    # Perulangan tarik API
    while True:
        if "cursor" in hasil.keys():

            for kategori in hasil['categories']:
                idnya = kategori['id']
                namanya = kategori['name']

                if not KategoriLoyverse.objects.filter(id_loyverse=idnya, nama_kategori= namanya).exists():
                    kl = KategoriLoyverse(id_loyverse=idnya, nama_kategori= namanya)
                    kl.save()
                else:
                    continue

            respon = requests.get(baseUrl, headers=header, params={'cursor' : hasil['cursor']})
            hasil = json.loads(respon.text)
        else:
            
            for kategori in hasil['categories']:
                idnya = kategori['id']
                namanya = kategori['name']

                if not KategoriLoyverse.objects.filter(id_loyverse=idnya, nama_kategori= namanya).exists():
                    kl = KategoriLoyverse(id_loyverse=idnya, nama_kategori= namanya)
                    kl.save()
                else:
                    continue

            break
