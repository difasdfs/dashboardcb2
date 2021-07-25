from datetime import datetime
from home_dashboard.models import DataStruk
import pytz
import requests
import json

outlet = {
    'a3adef0d-dc49-4b3b-82cc-09329bcd48b3' : 'Crisbar Kopo',
    'dc2497ed-963e-42ff-96a2-aeb7a8b65668' : 'Crisbar Metro Margahayu',
    'f0567abc-86a2-4f85-b027-82947b0a3983' : 'Crisbar Antapani',
    'fad4f949-711d-11ea-8d93-0603130a05b8' : 'Crisbar Sukabirus',
    'faa54a24-711d-11ea-8d93-0603130a05b8' : 'Crisbar Sukapura',
    'faa54a0c-711d-11ea-8d93-0603130a05b8' : 'Crisbar Sukajadi',
    'faa549f4-711d-11ea-8d93-0603130a05b8' : 'Crisbar Jatinangor',
    'faa545eb-711d-11ea-8d93-0603130a05b8' : 'Crisbar Unjani',
    'faa5442b-711d-11ea-8d93-0603130a05b8' : 'Crisbar Cisitu',
}

def main():

    nomor_struk = '33-17606'
    baseUrl = 'https://api.loyverse.com/v1.0/receipts/'
    access_token = '4a3e5665ac324711b13d677c8c05cac8'
    header = {'Authorization' : 'Bearer ' + access_token}

    payload = {
        "since_receipt_number" : nomor_struk,
        'limit' : 250
        }

    respon = requests.get(baseUrl, headers=header, params=payload)
    hasil = json.loads(respon.text)

    if "error" in hasil.keys():
        return 0

    while True:
        if "cursor" in hasil.keys():

            for struk in hasil['receipts']:

                try:
                    total_money = struk['total_money'] + (struk['payments'][1]['money_amount'] * -1)
                except:
                    total_money = struk['total_money']

                try:
                    store_id = outlet[struk['store_id']]
                except:
                    store_id = struk['store_id']

                try:
                    ds = DataStruk(
                        receipt_number = struk['receipt_number'],
                        receipt_type = struk['receipt_type'],
                        created_at = pytz.utc.localize(datetime.fromisoformat(struk['created_at'][:-1])),
                        receipt_date = pytz.utc.localize(datetime.fromisoformat(struk['receipt_date'][:-1])),
                        total_money = total_money,
                        total_tax = struk['total_tax'],
                        store_id = store_id,
                        dining_option = struk['dining_option'],
                        payments = struk['payments'][0]['name'],
                        )
                    ds.save()
                    print(datetime.fromisoformat(struk['created_at'][:-1]))
                except:
                    print("Error")
                    print(datetime.fromisoformat(struk['created_at'][:-1]))
                    continue

            respon = requests.get(baseUrl, headers=header, params={'cursor' : hasil['cursor']})
            hasil = json.loads(respon.text)
        else:

            for struk in hasil['receipts']:

                try:
                    total_money = struk['total_money'] + (struk['payments'][1]['money_amount'] * -1)
                except:
                    total_money = struk['total_money']

                try:
                    store_id = outlet[struk['store_id']]
                except:
                    store_id = struk['store_id']

                try:
                    ds = DataStruk(
                        receipt_number = struk['receipt_number'],
                        receipt_type = struk['receipt_type'],
                        created_at = pytz.utc.localize(datetime.fromisoformat(struk['created_at'][:-1])),
                        receipt_date = pytz.utc.localize(datetime.fromisoformat(struk['receipt_date'][:-1])),
                        total_money = total_money,
                        total_tax = struk['total_tax'],
                        store_id = store_id,
                        dining_option = struk['dining_option'],
                        payments = struk['payments'][0]['name'],
                        )
                    ds.save()
                    print(datetime.fromisoformat(struk['created_at'][:-1]))
                except:
                    print("Error")
                    print(datetime.fromisoformat(struk['created_at'][:-1]))
                    continue

            break

# class DataStruk(models.Model):
#     receipt_number = models.CharField(max_length=100)
#     receipt_type = models.CharField(max_length=100)
#     created_at = models.DateTimeField()
#     receipt_date = models.DateTimeField()
#     total_money = models.IntegerField()
#     total_tax = models.IntegerField()
#     store_id = models.CharField(max_length=170)
#     dining_option = models.CharField(max_length=100)
#     payments = models.CharField(max_length=100)
#     total_money_filter = models.IntegerField()