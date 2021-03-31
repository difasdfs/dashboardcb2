from .models import DataStruk, AverageCheck, NomorStrukTerakhir
import requests
import json
from datetime import datetime, timedelta, date
from django.utils import timezone
import pytz

# fungsi ini memiliki argumen id dari model AverageCheck, lalu mengupdate hampir seluruh atributnya
# berdasarkan ketersediaan DataStruk
def update_tc(id_objek_ac):
    ac = AverageCheck.objects.get(pk=id_objek_ac)
    struk = DataStruk.objects.filter(created_at__range=[ac.awal_hari, ac.akhir_hari])
    total_sales_dine_in_takeaway = 0
    total_check = 0
    total_sales_online = 0
    total_check_online = 0

    total_check_antapani = 0
    total_check_online_antapani = 0
    total_sales_antapani = 0
    total_sales_online_antapani = 0

    total_check_metro = 0
    total_check_online_metro = 0
    total_sales_metro = 0
    total_sales_online_metro = 0

    total_check_jatinangor = 0
    total_check_online_jatinangor = 0
    total_sales_jatinangor = 0
    total_sales_online_jatinangor = 0

    total_check_sukapura = 0
    total_check_online_sukapura = 0
    total_sales_sukapura = 0
    total_sales_online_sukapura = 0

    total_check_sukabirus = 0
    total_check_online_sukabirus = 0
    total_sales_sukabirus = 0
    total_sales_online_sukabirus = 0

    total_check_unjani = 0
    total_check_online_unjani = 0
    total_sales_unjani = 0
    total_sales_online_unjani = 0

    total_check_cisitu = 0
    total_check_online_cisitu = 0
    total_sales_cisitu = 0
    total_sales_online_cisitu = 0

    total_check_sukajadi = 0
    total_check_online_sukajadi = 0
    total_sales_sukajadi = 0
    total_sales_online_sukajadi = 0

    for s in struk:
        cabang = s.outlet
        if "FOOD" in s.nama_pembayaran:
            total_sales_online += s.money_amount
            total_check_online += 1

            if "Metro" in cabang:
                total_check_online_metro += 1
                total_sales_online_metro += s.money_amount
            elif "Antapani" in cabang:
                total_check_online_antapani += 1
                total_sales_online_antapani += s.money_amount
            elif "Jatinangor" in cabang:
                total_check_online_jatinangor += 1
                total_sales_online_jatinangor += s.money_amount
            elif "Sukapura" in cabang:
                total_check_online_sukapura += 1
                total_sales_online_sukapura += s.money_amount
            elif "Sukabirus" in cabang:
                total_check_online_sukabirus += 1
                total_sales_online_sukabirus += s.money_amount
            elif "Unjani" in cabang:
                total_check_online_unjani += 1
                total_sales_online_unjani += s.money_amount
            elif "Cisitu" in cabang:
                total_check_online_cisitu += 1
                total_sales_online_cisitu += s.money_amount
            elif "Sukajadi" in cabang:
                total_check_online_sukajadi += 1
                total_sales_online_sukajadi += s.money_amount

        else:
            total_sales_dine_in_takeaway += s.money_amount
            total_check +=1

            if "Metro" in cabang:
                total_check_metro += 1
                total_sales_metro += s.money_amount
            elif "Antapani" in cabang:
                total_check_antapani += 1
                total_sales_antapani += s.money_amount
            elif "Jatinangor" in cabang:
                total_check_jatinangor += 1
                total_sales_jatinangor += s.money_amount
            elif "Sukapura" in cabang:
                total_check_sukapura += 1
                total_sales_sukapura += s.money_amount
            elif "Sukabirus" in cabang:
                total_check_sukabirus += 1
                total_sales_sukabirus += s.money_amount
            elif "Unjani" in cabang:
                total_check_unjani += 1
                total_sales_unjani += s.money_amount
            elif "Cisitu" in cabang:
                total_check_cisitu += 1
                total_sales_cisitu += s.money_amount
            elif "Sukajadi" in cabang:
                total_check_sukajadi += 1
                total_sales_sukajadi += s.money_amount
    
    # OFFLINE
    if total_check == 0:
        ac.average_check = 0
    else: 
        ac.average_check = total_sales_dine_in_takeaway / total_check

    if total_check_antapani == 0:
        ac.average_check_antapani = 0
    else:
        ac.average_check_antapani = total_sales_antapani / total_check_antapani

    if total_check_metro == 0:
        ac.average_check_metro = 0
    else:
        ac.average_check_metro = total_sales_metro / total_check_metro
    
    if total_check_antapani == 0:
        ac.average_check_antapani = 0
    else:
        ac.average_check_antapani = total_sales_antapani / total_check_antapani

    if total_check_jatinangor == 0:
        ac.average_check_jatinangor = 0
    else:
        ac.average_check_jatinangor = total_sales_jatinangor / total_check_jatinangor

    if total_check_sukabirus == 0:
        ac.average_check_sukabirus = 0
    else:
        ac.average_check_sukabirus = total_sales_sukabirus / total_check_sukabirus

    if total_check_sukapura == 0:
        ac.average_check_sukapura = 0
    else:
        ac.average_check_sukapura = total_sales_sukapura / total_check_sukapura

    if total_check_unjani == 0:
        ac.average_check_unjani = 0
    else:
        ac.average_check_unjani = total_sales_unjani / total_check_unjani

    if total_check_cisitu == 0:
        ac.average_check_cisitu = 0
    else:
        ac.average_check_cisitu = total_sales_cisitu / total_check_cisitu
    
    if total_check_sukajadi == 0:
        ac.average_check_sukajadi = 0
    else:
        ac.average_check_sukajadi = total_sales_sukajadi / total_check_sukajadi

    # ONLINE
    if total_check_online == 0:
        ac.average_check_online = 0
    else: 
        ac.average_check_online = total_sales_online / total_check_online

    if total_check_online_antapani == 0:
        ac.average_check_online_antapani = 0
    else:
        ac.average_check_online_antapani = total_sales_online_antapani / total_check_online_antapani

    if total_check_online_metro == 0:
        ac.average_check_online_metro = 0
    else:
        ac.average_check_online_metro = total_sales_online_metro / total_check_online_metro

    if total_check_online_jatinangor == 0:
        ac.average_check_online_jatinangor = 0
    else:
        ac.average_check_online_jatinangor = total_sales_online_jatinangor / total_check_online_jatinangor

    if total_check_online_sukabirus == 0:
        ac.average_check_online_sukabirus = 0
    else:
        ac.average_check_online_sukabirus = total_sales_online_sukabirus / total_check_online_sukabirus

    if total_check_online_sukapura == 0:
        ac.average_check_online_sukapura = 0
    else:
        ac.average_check_online_sukapura = total_sales_online_sukapura / total_check_online_sukapura

    if total_check_online_unjani == 0:
        ac.average_check_online_unjani = 0
    else:
        ac.average_check_online_unjani = total_sales_online_unjani / total_check_online_unjani

    if total_check_online_cisitu == 0:
        ac.average_check_online_cisitu = 0
    else:
        ac.average_check_online_cisitu = total_sales_online_cisitu / total_check_online_cisitu
    
    if total_check_online_sukajadi == 0:
        ac.average_check_online_sukajadi = 0
    else:
        ac.average_check_online_sukajadi = total_sales_online_sukajadi / total_check_online_sukajadi

    ac.total_sales = total_sales_dine_in_takeaway
    ac.total_sales_online = total_sales_online
    ac.total_sales_antapani = total_sales_antapani
    ac.total_sales_online_antapani = total_sales_online_antapani
    ac.total_sales_metro = total_sales_metro
    ac.total_sales_online_metro = total_sales_online_metro
    ac.total_sales_jatinangor = total_sales_jatinangor
    ac.total_sales_online_jatinangor = total_sales_online_jatinangor
    ac.total_sales_sukapura = total_sales_sukapura
    ac.total_sales_online_sukapura = total_sales_online_sukapura
    ac.total_sales_sukabirus = total_sales_sukabirus
    ac.total_sales_online_sukabirus = total_sales_online_sukabirus
    ac.total_sales_unjani = total_sales_unjani
    ac.total_sales_online_unjani = total_sales_online_unjani
    ac.total_sales_cisitu = total_sales_cisitu
    ac.total_sales_online_cisitu = total_sales_online_cisitu
    ac.total_sales_sukajadi = total_sales_sukajadi
    ac.total_sales_online_sukajadi = total_sales_online_sukajadi
    
    ac.total_check = total_check
    ac.total_check_antapani = total_check_antapani
    ac.total_check_metro = total_check_metro
    ac.total_check_jatinangor = total_check_jatinangor
    ac.total_check_sukapura = total_check_sukapura
    ac.total_check_sukabirus = total_check_sukabirus
    ac.total_check_unjani = total_check_unjani
    ac.total_check_cisitu = total_check_cisitu
    ac.total_check_sukajadi = total_check_sukajadi
    ac.total_check_online = total_check_online
    ac.total_check_online_antapani = total_check_online_antapani
    ac.total_check_online_metro = total_check_online_metro
    ac.total_check_online_jatinangor = total_check_online_jatinangor
    ac.total_check_online_sukapura = total_check_online_sukapura
    ac.total_check_online_sukabirus = total_check_online_sukabirus
    ac.total_check_online_unjani = total_check_online_unjani
    ac.total_check_online_cisitu = total_check_online_cisitu
    ac.total_check_online_sukajadi = total_check_online_sukajadi
    ac.save()

# fungsi ini berfungsi untuk mengupdate DataStruk berdasarkan last receipts dengan memanggil
# data melalui API loyverse
def refresh_tcav():
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

    nomor_struk_terakhir = NomorStrukTerakhir.objects.get(pk=1)

    baseUrl = 'https://api.loyverse.com/v1.0/receipts'
    access_token = '4a3e5665ac324711b13d677c8c05cac8'
    header = {'Authorization' : 'Bearer ' + access_token}
    payload = {
        "since_receipt_number" : nomor_struk_terakhir,
        'limit' : 250
    }
    respon = requests.get(baseUrl, headers=header, params=payload)
    hasil = json.loads(respon.text) # dictionary
    nomor_struk_terakhir.nomor_struk = hasil["receipts"][0]["receipt_number"]
    nomor_struk_terakhir.save()
    
    # return render(request, "index.html")
    while True:
        if "cursor" in hasil.keys():
            hasilnya = hasil["receipts"]
            for struk in hasilnya[::-1]:
                dibuat_pada = datetime.fromisoformat(struk["created_at"][:-1])
                d = DataStruk(
                    nomor_struk = struk["receipt_number"],
                    created_at = datetime(dibuat_pada.year, dibuat_pada.month, dibuat_pada.day, dibuat_pada.hour, dibuat_pada.minute, tzinfo=pytz.UTC),
                    outlet = rumus_id_outlet[struk["store_id"]],
                    nama_pembayaran = struk["payments"][0]["name"],
                    tipe_struk = struk["receipt_type"],
                    money_amount = struk["payments"][0]["money_amount"]
                )
                d.save()

            payload = {
                "cursor" : hasil["cursor"]
            }
            respon = requests.get(baseUrl, headers=header, params=payload)
            hasil = json.loads(respon.text)
        else:
            hasilnya = hasil["receipts"]
            for struk in hasilnya[::-1]:
                dibuat_pada = datetime.fromisoformat(struk["created_at"][:-1])
                d = DataStruk(
                    nomor_struk = struk["receipt_number"],
                    created_at = datetime(dibuat_pada.year, dibuat_pada.month, dibuat_pada.day, dibuat_pada.hour, dibuat_pada.minute, tzinfo=pytz.UTC),
                    outlet = rumus_id_outlet[struk["store_id"]],
                    nama_pembayaran = struk["payments"][0]["name"],
                    tipe_struk = struk["receipt_type"],
                    money_amount = struk["payments"][0]["money_amount"]
                )
                d.save()
            break

    # sekarang versi UTC
    # now = timezone.now() + timedelta(hours=7)
    # tanggal_sekarang = date(now.year, now.month, now.day)
    # cek_tanggal = AverageCheck.objects.filter(hari=tanggal_sekarang)

    # if not cek_tanggal:
    #     d = AverageCheck(hari=tanggal_sekarang)
    #     d.tentukan_awal_akhir_hari()
    #     d.save()
    
    # aw = AverageCheck.objects.filter(hari=tanggal_sekarang)[0]
    # update_tc(aw.id)