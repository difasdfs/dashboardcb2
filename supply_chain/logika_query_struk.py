from datetime import timedelta
from .models import StrukSold

import pytz

def main(waktu_awal, waktu_akhir):
    waktu_akhir_default_utc = pytz.utc.localize(waktu_akhir - timedelta(hours=7))
    waktu_awal_default_utc = pytz.utc.localize(waktu_awal - timedelta(hours=7))

    ss = StrukSold.objects.filter(waktu_struk__range=[waktu_awal_default_utc, waktu_akhir_default_utc])

    data_ayam = 0
    data_chicken_skin =0
    data_paper_cost_takeaway_l = 0
    data_paper_cost_takeaway_m =0
    data_paper_cost_takeaway_paper_bag = 0
    data_paper_cost_dine_in_paper_tray = 0
    data_topping_crisbar = 0
    data_topping_saus_gravy = 0
    data_topping_matah = 0
    data_topping_mamah = 0
    data_topping_tomat = 0
    data_topping_manis = 0
    data_topping_goang = 0
    data_topping_keju = 0
    data_tahu_crispy = 0
    data_tempe_crispy = 0
    data_terong_crispy =0
    data_telur_sayur = 0
    data_kol_crispy = 0
    data_kerupuk = 0
    data_sigulmer_manis_biscuit =0
    data_perkedel = 0
    data_nasi_dine_in = 0
    data_es_teh_dine_in = 0
    data_lemon_tea_dine_in =0
    data_milo_dine_in =0
    data_orange_dine_in =0
    data_nasi_takeaway =0
    data_es_teh_takeaway = 0
    data_lemon_tea_takeaway = 0
    data_milo_takeaway = 0
    data_orange_takeaway = 0
    data_air_mineral =0
    data_wings = 0

    for s in ss:
        data_ayam += s.jumlah_ayam
        data_chicken_skin += s.jumlah_chicken_skin
        data_paper_cost_takeaway_l += s.jumlah_paper_cost_takeaway_l
        data_paper_cost_takeaway_m += s.jumlah_paper_cost_takeaway_m
        data_paper_cost_takeaway_paper_bag += s.jumlah_paper_cost_takeaway_m
        data_paper_cost_dine_in_paper_tray += s.jumlah_paper_cost_dine_in_paper_tray
        data_topping_crisbar += s.jumlah_topping_crisbar
        data_topping_saus_gravy += s.jumlah_topping_saus_gravy
        data_topping_matah += s.jumlah_topping_matah
        data_topping_mamah += s.jumlah_topping_mamah
        data_topping_tomat += s.jumlah_topping_tomat
        data_topping_manis += s.jumlah_topping_manis
        data_topping_goang += s.jumlah_topping_goang
        data_topping_keju += s.jumlah_topping_keju
        data_tahu_crispy += s.jumlah_tahu_crispy
        data_tempe_crispy += s.jumlah_tempe_crispy
        data_terong_crispy += s.jumlah_terong_crispy
        data_telur_sayur += s.jumlah_telur_sayur
        data_kol_crispy += s.jumlah_kol_crispy
        data_kerupuk += s.jumlah_kerupuk
        data_sigulmer_manis_biscuit += s.jumlah_sigulmer_manis_biscuit
        data_perkedel += s.jumlah_perkedel
        data_nasi_dine_in += s.jumlah_nasi_dine_in
        data_es_teh_dine_in += s.jumlah_es_teh_dine_in
        data_lemon_tea_dine_in += s.jumlah_lemon_tea_dine_in
        data_milo_dine_in += s.jumlah_milo_dine_in
        data_orange_dine_in += s.jumlah_orange_dine_in
        data_nasi_takeaway += s.jumlah_nasi_takeaway
        data_es_teh_takeaway += s.jumlah_es_teh_takeaway
        data_lemon_tea_takeaway += s.jumlah_lemon_tea_takeaway
        data_milo_takeaway += s.jumlah_milo_takeaway
        data_orange_takeaway += s.jumlah_orange_takeaway
        data_air_mineral += s.jumlah_air_mineral
        data_wings += s.jumlah_wings

    data_struk = {
        "ayam" : data_ayam,
        "chicken_skin" : data_chicken_skin,
        "paper_cost_takeaway_l" : data_paper_cost_takeaway_l,
        "paper_cost_takeaway_m" : data_paper_cost_takeaway_m,
        "paper_cost_takeaway_paper_bag" : data_paper_cost_takeaway_paper_bag,
        "paper_cost_dine_in_paper_tray" : data_paper_cost_dine_in_paper_tray,
        "topping_crisbar" : data_topping_crisbar,
        "topping_saus_gravy" : data_topping_saus_gravy,
        "topping_matah" : data_topping_matah,
        "topping_mamah" : data_topping_mamah,
        "topping_tomat" : data_topping_tomat,
        "topping_manis" : data_topping_manis,
        "topping_goang" : data_topping_goang,
        "topping_keju" : data_topping_keju,
        "tahu_crispy" : data_tahu_crispy,
        "tempe_crispy" : data_tempe_crispy,
        "terong_crispy" : data_terong_crispy,
        "telur_sayur" : data_telur_sayur,
        "kol_crispy" : data_kol_crispy,
        "kerupuk" : data_kerupuk,
        "sigulmer_manis_biscuit" : data_sigulmer_manis_biscuit,
        "perkedel" : data_perkedel,
        "nasi_dine_in" : data_nasi_dine_in,
        "es_teh_dine_in" : data_es_teh_dine_in,
        "lemon_tea_dine_in" : data_lemon_tea_dine_in,
        "milo_dine_in" : data_milo_dine_in,
        "orange_dine_in" : data_orange_dine_in,
        "nasi_takeaway" : data_nasi_takeaway,
        "es_teh_takeaway" : data_es_teh_takeaway,
        "lemon_tea_takeaway" : data_lemon_tea_takeaway,
        "milo_takeaway" : data_milo_takeaway,
        "orange_takeaway" : data_orange_takeaway,
        "air_mineral" : data_air_mineral,
        "wings" : data_wings,
    }

    return data_struk