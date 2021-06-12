import requests
import json
from .models import IdCabangKopo, StrukTerakhir, Struk

def main():
    try:
        q = IdCabangKopo.objects.get(pk=1)
    except:
        q = IdCabangKopo(
            id_cabang = 'a3adef0d-dc49-4b3b-82cc-09329bcd48b3'
        )
        q.save()
    try:
        s = StrukTerakhir.objects.get(pk=1)
    except:
        s = StrukTerakhir(
            nomor_struk = "54-1027"
        )
        s.save()

    baseUrl = 'https://api.loyverse.com/v1.0/receipts'
    access_token = '4a3e5665ac324711b13d677c8c05cac8'
    header = {'Authorization' : 'Bearer ' + access_token}

    payload = {
            'since_receipt_number' : s.nomor_struk,
            'store_id' : q.id_cabang,
            'limit' : 250
        }

    respon = requests.get(baseUrl, headers=header, params=payload)
    hasil = json.loads(respon.text)

    i = 1

    while True:
        if "cursor" in hasil.keys():
            kumpulan_struk = hasil['receipts']
            
            for struk in kumpulan_struk:
                nomor_struknya = struk['receipt_number']
                dibuat_pada = struk['created_at']
                total_moneynya = struk['total_money']

                if i == 1:
                    s.nomor_struk = nomor_struknya
                    s.save()
                    i += 1

                nama_pembayaran = []
                for a in struk['payments']:
                    nama_pembayaran.append(a['name'])

                print(str(i) + '. ' + nomor_struknya + ' - ' + dibuat_pada + ' - ' + str(total_moneynya))
                print("Tipe total money : " + str(type(total_moneynya)))

                if "GRAB FOOD" in nama_pembayaran:
                    total_moneynya = total_moneynya*0.77
                elif "GO FOOD" in nama_pembayaran:
                    total_moneynya = total_moneynya*0.8 - 800
                elif ("GOPAY" in nama_pembayaran) or ("OVO" in nama_pembayaran) or ("SHOPEE PAY" in nama_pembayaran):
                    total_moneynya = total_moneynya*0.993
                elif "SHOPEE FOOD" in nama_pembayaran:
                    total_moneynya = total_moneynya*0.8
                else:
                    total_moneynya = total_moneynya - struk['total_tax']
                
                struk_baru = Struk(
                    nomor_struk = nomor_struknya,
                    created_at = dibuat_pada,
                    total_money = total_moneynya
                )
                struk_baru.save()
                i += 1
            respon = requests.get(baseUrl, headers=header, params={'cursor' : hasil['cursor']})
            hasil = json.loads(respon.text)
        else:
            kumpulan_struk = hasil['receipts']
            for struk in kumpulan_struk:
                nomor_struknya = struk['receipt_number']
                dibuat_pada = struk['created_at']
                total_moneynya = struk['total_money']

                if i == 1:
                    s.nomor_struk = nomor_struknya
                    s.save()
                    i += 1

                nama_pembayaran = []
                for a in struk['payments']:
                    nama_pembayaran.append(a['name'])

                print(str(i) + '. ' + nomor_struknya + ' - ' + dibuat_pada + ' - ' + str(total_moneynya))
                print("Tipe total money : " + str(type(total_moneynya)))

                if "GRAB FOOD" in nama_pembayaran:
                    total_moneynya = total_moneynya*0.77
                elif "GO FOOD" in nama_pembayaran:
                    total_moneynya = total_moneynya*0.8 - 800
                elif ("GOPAY" in nama_pembayaran) or ("OVO" in nama_pembayaran) or ("SHOPEE PAY" in nama_pembayaran):
                    total_moneynya = total_moneynya*0.993
                elif "SHOPEE FOOD" in nama_pembayaran:
                    total_moneynya = total_moneynya*0.8
                else:
                    total_moneynya = total_moneynya - struk['total_tax']
                
                struk_baru = Struk(
                    nomor_struk = nomor_struknya,
                    created_at = dibuat_pada,
                    total_money = total_moneynya
                )
                struk_baru.save()
                i += 1
            break