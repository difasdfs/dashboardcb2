from supply_chain.models import CabangLoyverse, StrukSold, NomorStrukSoldTerakhir
from dashboard.models import AssemblyProduct
from datetime import datetime

import requests
import json

def main():
    id_cabang_loyverse = {}
    object_cabang_loyverse = CabangLoyverse.objects.all()
    for objek in object_cabang_loyverse:
        id_cabang_loyverse[objek.id_loyverse] = objek.nama_cabang

    no_struk = "44-8294"
    baseUrl = 'https://api.loyverse.com/v1.0/receipts/'
    access_token = '4a3e5665ac324711b13d677c8c05cac8'
    header = {'Authorization' : 'Bearer ' + access_token}

    payload = {
        "since_receipt_number" : no_struk,
        'limit' : 250
        }

    respon = requests.get(baseUrl, headers=header, params=payload)
    hasil = json.loads(respon.text)

    i = 1
    while True:
        if "cursor" in hasil.keys():

            for struk in hasil['receipts']:

                if i == 1:
                    i += 1
                    n = NomorStrukSoldTerakhir(nomor_struk = struk['receipt_number'])
                    n.save()

                nomor_struk = struk['receipt_number']
                tipe_struk = struk['receipt_type']

                if "SALE" in tipe_struk:
                    pengali = 1
                else:
                    pengali = -1

                waktu_struk = struk['receipt_date'][:-1] + "+00:00"
                waktu_struk_datetime = datetime.fromisoformat(waktu_struk)
                print(struk['created_at'])

                # try except
                try:
                    outlet = id_cabang_loyverse[struk['store_id']]
                except:
                    outlet = struk['store_id']

                ayam = 0
                chicken_skin =0
                paper_cost_takeaway_l = 0
                paper_cost_takeaway_m =0
                paper_cost_takeaway_paper_bag = 0
                paper_cost_dine_in_paper_tray = 0
                topping_crisbar = 0
                topping_saus_gravy = 0
                topping_matah = 0
                topping_mamah = 0
                topping_tomat = 0
                topping_manis = 0
                topping_goang = 0
                topping_keju = 0
                tahu_crispy = 0
                tempe_crispy = 0
                terong_crispy =0
                telur_sayur = 0
                kol_crispy = 0
                kerupuk = 0
                sigulmer_manis_biscuit =0
                perkedel = 0
                nasi_dine_in = 0
                es_teh_dine_in = 0
                lemon_tea_dine_in =0
                milo_dine_in =0
                orange_dine_in =0
                nasi_takeaway =0
                es_teh_takeaway = 0
                lemon_tea_takeaway = 0
                milo_takeaway = 0
                orange_takeaway = 0
                air_mineral =0
                wings = 0

                for item in struk['line_items']:
                    skunya = item['sku']

                    try:
                        object_assembly = AssemblyProduct.objects.get(sku=skunya)
                    except:
                        continue

                    kuantitas = item['quantity']

                    ayam += object_assembly.ayam * kuantitas * pengali
                    chicken_skin += object_assembly.chicken_skin  * kuantitas * pengali
                    paper_cost_takeaway_l += object_assembly.paper_cost_takeaway_l * kuantitas * pengali
                    paper_cost_takeaway_m += object_assembly.paper_cost_takeaway_m * kuantitas * pengali
                    paper_cost_takeaway_paper_bag += object_assembly.paper_cost_takeaway_paper_bag * kuantitas * pengali
                    paper_cost_dine_in_paper_tray += object_assembly.paper_cost_dine_in_paper_tray * kuantitas * pengali
                    topping_crisbar += object_assembly.topping_crisbar * kuantitas * pengali
                    topping_saus_gravy += object_assembly.topping_saus_gravy * kuantitas * pengali
                    topping_matah += object_assembly.topping_matah * kuantitas * pengali
                    topping_mamah += object_assembly.topping_mamah * kuantitas * pengali
                    topping_tomat += object_assembly.topping_tomat * kuantitas * pengali
                    topping_manis += object_assembly.topping_manis * kuantitas * pengali
                    topping_goang += object_assembly.topping_goang * kuantitas * pengali
                    topping_keju += object_assembly.topping_keju * kuantitas * pengali
                    tahu_crispy += object_assembly.tahu_crispy * kuantitas * pengali
                    tempe_crispy += object_assembly.tempe_crispy * kuantitas * pengali
                    terong_crispy += object_assembly.terong_crispy * kuantitas * pengali
                    telur_sayur += object_assembly.telur_sayur * kuantitas * pengali
                    kol_crispy += object_assembly.kol_crispy * kuantitas * pengali
                    kerupuk += object_assembly.kerupuk * kuantitas * pengali
                    sigulmer_manis_biscuit += object_assembly.sigulmer_manis_biscuit * kuantitas * pengali
                    perkedel += object_assembly.perkedel * kuantitas * pengali
                    nasi_dine_in += object_assembly.nasi_dine_in * kuantitas * pengali
                    es_teh_dine_in += object_assembly.es_teh_dine_in * kuantitas * pengali
                    lemon_tea_dine_in += object_assembly.lemon_tea_dine_in * kuantitas * pengali
                    milo_dine_in += object_assembly.milo_dine_in * kuantitas * pengali
                    orange_dine_in += object_assembly.orange_dine_in * kuantitas * pengali
                    nasi_takeaway += object_assembly.nasi_takeaway * kuantitas * pengali
                    es_teh_takeaway += object_assembly.es_teh_takeaway * kuantitas * pengali
                    lemon_tea_takeaway += object_assembly.lemon_tea_takeaway * kuantitas * pengali
                    milo_takeaway += object_assembly.milo_takeaway * kuantitas * pengali
                    orange_takeaway += object_assembly.orange_takeaway * kuantitas * pengali
                    air_mineral += object_assembly.air_mineral * kuantitas * pengali
                    try:
                        wings += object_assembly.wings * kuantitas * pengali
                    except:
                        wings += 0 * kuantitas * pengali

                i += 1

                ss = StrukSold(
                    nomor_struk = nomor_struk,
                    nama_cabang = outlet,
                    waktu_struk = waktu_struk_datetime,
                    status = tipe_struk,

                    jumlah_ayam = ayam,
                    jumlah_chicken_skin = chicken_skin,
                    jumlah_paper_cost_takeaway_l = paper_cost_takeaway_l,
                    jumlah_paper_cost_takeaway_m = paper_cost_takeaway_m,
                    jumlah_paper_cost_takeaway_paper_bag = paper_cost_takeaway_paper_bag,
                    jumlah_paper_cost_dine_in_paper_tray = paper_cost_dine_in_paper_tray,
                    jumlah_topping_crisbar = topping_crisbar,
                    jumlah_topping_saus_gravy = topping_saus_gravy,
                    jumlah_topping_matah = topping_matah,
                    jumlah_topping_mamah = topping_mamah,
                    jumlah_topping_tomat = topping_tomat,
                    jumlah_topping_manis = topping_manis,
                    jumlah_topping_goang = topping_goang,
                    jumlah_topping_keju = topping_keju,
                    jumlah_tahu_crispy = tahu_crispy,
                    jumlah_tempe_crispy = tempe_crispy,
                    jumlah_terong_crispy = terong_crispy,
                    jumlah_telur_sayur = telur_sayur,
                    jumlah_kol_crispy = kol_crispy,
                    jumlah_kerupuk = kerupuk,
                    jumlah_sigulmer_manis_biscuit = sigulmer_manis_biscuit,
                    jumlah_perkedel = perkedel,
                    jumlah_nasi_dine_in = nasi_dine_in,
                    jumlah_es_teh_dine_in = es_teh_dine_in,
                    jumlah_lemon_tea_dine_in = lemon_tea_dine_in,
                    jumlah_milo_dine_in = milo_dine_in,
                    jumlah_orange_dine_in = orange_dine_in,
                    jumlah_nasi_takeaway = nasi_takeaway,
                    jumlah_es_teh_takeaway = es_teh_takeaway,
                    jumlah_lemon_tea_takeaway = lemon_tea_takeaway,
                    jumlah_milo_takeaway = milo_takeaway,
                    jumlah_orange_takeaway = orange_takeaway,
                    jumlah_air_mineral = air_mineral,
                    jumlah_wings = wings
                )
                ss.save()

            respon = requests.get(baseUrl, headers=header, params={"cursor" : hasil['cursor']})
            hasil = json.loads(respon.text)
        else:

            for struk in hasil['receipts']:

                if i == 1:
                    i += 1
                    n = NomorStrukSoldTerakhir(nomor_struk = struk['receipt_number'])
                    n.save()

                nomor_struk = struk['receipt_number']
                tipe_struk = struk['receipt_type']

                if "SALE" in tipe_struk:
                    pengali = 1
                else:
                    pengali = -1

                waktu_struk = struk['receipt_date'][:-1] + "+00:00"
                waktu_struk_datetime = datetime.fromisoformat(waktu_struk)
                print(struk['created_at'])

                # try except
                try:
                    outlet = id_cabang_loyverse[struk['store_id']]
                except:
                    outlet = struk['store_id']

                ayam = 0
                chicken_skin =0
                paper_cost_takeaway_l = 0
                paper_cost_takeaway_m =0
                paper_cost_takeaway_paper_bag = 0
                paper_cost_dine_in_paper_tray = 0
                topping_crisbar = 0
                topping_saus_gravy = 0
                topping_matah = 0
                topping_mamah = 0
                topping_tomat = 0
                topping_manis = 0
                topping_goang = 0
                topping_keju = 0
                tahu_crispy = 0
                tempe_crispy = 0
                terong_crispy =0
                telur_sayur = 0
                kol_crispy = 0
                kerupuk = 0
                sigulmer_manis_biscuit =0
                perkedel = 0
                nasi_dine_in = 0
                es_teh_dine_in = 0
                lemon_tea_dine_in =0
                milo_dine_in =0
                orange_dine_in =0
                nasi_takeaway =0
                es_teh_takeaway = 0
                lemon_tea_takeaway = 0
                milo_takeaway = 0
                orange_takeaway = 0
                air_mineral =0
                wings = 0

                for item in struk['line_items']:
                    skunya = item['sku']

                    try:
                        object_assembly = AssemblyProduct.objects.get(sku=skunya)
                    except:
                        continue

                    kuantitas = item['quantity']

                    ayam += object_assembly.ayam * kuantitas * pengali
                    chicken_skin += object_assembly.chicken_skin  * kuantitas * pengali
                    paper_cost_takeaway_l += object_assembly.paper_cost_takeaway_l * kuantitas * pengali
                    paper_cost_takeaway_m += object_assembly.paper_cost_takeaway_m * kuantitas * pengali
                    paper_cost_takeaway_paper_bag += object_assembly.paper_cost_takeaway_paper_bag * kuantitas * pengali
                    paper_cost_dine_in_paper_tray += object_assembly.paper_cost_dine_in_paper_tray * kuantitas * pengali
                    topping_crisbar += object_assembly.topping_crisbar * kuantitas * pengali
                    topping_saus_gravy += object_assembly.topping_saus_gravy * kuantitas * pengali
                    topping_matah += object_assembly.topping_matah * kuantitas * pengali
                    topping_mamah += object_assembly.topping_mamah * kuantitas * pengali
                    topping_tomat += object_assembly.topping_tomat * kuantitas * pengali
                    topping_manis += object_assembly.topping_manis * kuantitas * pengali
                    topping_goang += object_assembly.topping_goang * kuantitas * pengali
                    topping_keju += object_assembly.topping_keju * kuantitas * pengali
                    tahu_crispy += object_assembly.tahu_crispy * kuantitas * pengali
                    tempe_crispy += object_assembly.tempe_crispy * kuantitas * pengali
                    terong_crispy += object_assembly.terong_crispy * kuantitas * pengali
                    telur_sayur += object_assembly.telur_sayur * kuantitas * pengali
                    kol_crispy += object_assembly.kol_crispy * kuantitas * pengali
                    kerupuk += object_assembly.kerupuk * kuantitas * pengali
                    sigulmer_manis_biscuit += object_assembly.sigulmer_manis_biscuit * kuantitas * pengali
                    perkedel += object_assembly.perkedel * kuantitas * pengali
                    nasi_dine_in += object_assembly.nasi_dine_in * kuantitas * pengali
                    es_teh_dine_in += object_assembly.es_teh_dine_in * kuantitas * pengali
                    lemon_tea_dine_in += object_assembly.lemon_tea_dine_in * kuantitas * pengali
                    milo_dine_in += object_assembly.milo_dine_in * kuantitas * pengali
                    orange_dine_in += object_assembly.orange_dine_in * kuantitas * pengali
                    nasi_takeaway += object_assembly.nasi_takeaway * kuantitas * pengali
                    es_teh_takeaway += object_assembly.es_teh_takeaway * kuantitas * pengali
                    lemon_tea_takeaway += object_assembly.lemon_tea_takeaway * kuantitas * pengali
                    milo_takeaway += object_assembly.milo_takeaway * kuantitas * pengali
                    orange_takeaway += object_assembly.orange_takeaway * kuantitas * pengali
                    air_mineral += object_assembly.air_mineral * kuantitas * pengali
                    try:
                        wings += object_assembly.wings * kuantitas * pengali
                    except:
                        wings += 0 * kuantitas * pengali

                i += 1

                ss = StrukSold(
                    nomor_struk = nomor_struk,
                    nama_cabang = outlet,
                    waktu_struk = waktu_struk_datetime,
                    status = tipe_struk,

                    jumlah_ayam = ayam,
                    jumlah_chicken_skin = chicken_skin,
                    jumlah_paper_cost_takeaway_l = paper_cost_takeaway_l,
                    jumlah_paper_cost_takeaway_m = paper_cost_takeaway_m,
                    jumlah_paper_cost_takeaway_paper_bag = paper_cost_takeaway_paper_bag,
                    jumlah_paper_cost_dine_in_paper_tray = paper_cost_dine_in_paper_tray,
                    jumlah_topping_crisbar = topping_crisbar,
                    jumlah_topping_saus_gravy = topping_saus_gravy,
                    jumlah_topping_matah = topping_matah,
                    jumlah_topping_mamah = topping_mamah,
                    jumlah_topping_tomat = topping_tomat,
                    jumlah_topping_manis = topping_manis,
                    jumlah_topping_goang = topping_goang,
                    jumlah_topping_keju = topping_keju,
                    jumlah_tahu_crispy = tahu_crispy,
                    jumlah_tempe_crispy = tempe_crispy,
                    jumlah_terong_crispy = terong_crispy,
                    jumlah_telur_sayur = telur_sayur,
                    jumlah_kol_crispy = kol_crispy,
                    jumlah_kerupuk = kerupuk,
                    jumlah_sigulmer_manis_biscuit = sigulmer_manis_biscuit,
                    jumlah_perkedel = perkedel,
                    jumlah_nasi_dine_in = nasi_dine_in,
                    jumlah_es_teh_dine_in = es_teh_dine_in,
                    jumlah_lemon_tea_dine_in = lemon_tea_dine_in,
                    jumlah_milo_dine_in = milo_dine_in,
                    jumlah_orange_dine_in = orange_dine_in,
                    jumlah_nasi_takeaway = nasi_takeaway,
                    jumlah_es_teh_takeaway = es_teh_takeaway,
                    jumlah_lemon_tea_takeaway = lemon_tea_takeaway,
                    jumlah_milo_takeaway = milo_takeaway,
                    jumlah_orange_takeaway = orange_takeaway,
                    jumlah_air_mineral = air_mineral,
                    jumlah_wings = wings
                )
                ss.save()
            break