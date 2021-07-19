from supply_chain.models import StrukSold
from datetime import date, timedelta, datetime
import pytz
import math

def main(isi_dict, cabang):

    # Fungsi ini menerima input sebuah dictionary yang kuncinya merupakan item yang dipilih dan valuenya adalah nilai opname onhand
    # juga ada nama cabang untuk query

    kemarin = date.today() - timedelta(days=1)
    tujuh_hari_lalu = kemarin - timedelta(days=6)

    akhir = datetime(kemarin.year, kemarin.month, kemarin.day, 23, 59, tzinfo=pytz.UTC) - timedelta(hours=7)
    awal = datetime(tujuh_hari_lalu.year, tujuh_hari_lalu.month, tujuh_hari_lalu.day, 8, 0, tzinfo=pytz.UTC) - timedelta(hours=7)

    data_demand = penjumlahan(StrukSold.objects.filter(waktu_struk__range=[awal, akhir], nama_cabang=cabang))

    # print(data_demand)

    hasil = {}
    kunci = isi_dict.keys()
    for k in kunci:
        stok_on_hand = isi_dict[k]
        demand = data_demand[k]
        minimal = demand["minimal"]
        maksimal = demand["maksimal"]
        satuan = demand["satuan"]
        nama_item = demand["nama_item"]

        if stok_on_hand > maksimal:
            continue

        po = math.ceil(maksimal - stok_on_hand)

        if (po < minimal) and (minimal - stok_on_hand > 0):
            po = math.ceil(minimal - stok_on_hand)
        elif po < minimal:
            po = minimal

        hasil[k] = {
            'total_po' : po,
            'satuan' : satuan,
            'nama_item' : nama_item
            }

    # print(hasil)

    return hasil

def penjumlahan(querynya):

    # print("Querynya : ")
    # print(querynya)

    jumlah_ayam = 0
    jumlah_chicken_skin = 0
    jumlah_paper_cost_takeaway_l = 0
    jumlah_paper_cost_takeaway_m = 0
    jumlah_paper_cost_takeaway_paper_bag = 0
    jumlah_paper_cost_dine_in_paper_tray = 0
    jumlah_topping_crisbar = 0
    jumlah_topping_saus_gravy = 0
    jumlah_topping_matah = 0
    jumlah_topping_mamah = 0
    jumlah_topping_tomat = 0
    jumlah_topping_manis = 0
    jumlah_topping_goang = 0
    jumlah_topping_keju = 0
    jumlah_tahu_crispy = 0
    jumlah_tempe_crispy = 0
    jumlah_terong_crispy = 0
    jumlah_telur_sayur = 0
    jumlah_kol_crispy = 0
    jumlah_kerupuk = 0
    jumlah_sigulmer_manis_biscuit = 0
    jumlah_perkedel = 0
    jumlah_nasi_dine_in = 0
    jumlah_es_teh_dine_in = 0
    jumlah_lemon_tea_dine_in = 0
    jumlah_milo_dine_in = 0
    jumlah_orange_dine_in = 0
    jumlah_nasi_takeaway = 0
    jumlah_es_teh_takeaway = 0
    jumlah_lemon_tea_takeaway = 0
    jumlah_milo_takeaway = 0
    jumlah_orange_takeaway = 0
    jumlah_air_mineral = 0
    jumlah_wings = 0

    for a in querynya:
        jumlah_ayam += a.jumlah_ayam
        jumlah_chicken_skin += a.jumlah_chicken_skin
        jumlah_paper_cost_takeaway_l += a.jumlah_paper_cost_takeaway_l
        jumlah_paper_cost_takeaway_m += a.jumlah_paper_cost_takeaway_m
        jumlah_paper_cost_takeaway_paper_bag += a.jumlah_paper_cost_takeaway_paper_bag
        jumlah_paper_cost_dine_in_paper_tray += a.jumlah_paper_cost_dine_in_paper_tray
        jumlah_topping_crisbar += a.jumlah_topping_crisbar
        jumlah_topping_saus_gravy += a.jumlah_topping_saus_gravy
        jumlah_topping_matah += a.jumlah_topping_matah
        jumlah_topping_mamah += a.jumlah_topping_mamah
        jumlah_topping_tomat += a.jumlah_topping_tomat
        jumlah_topping_manis += a.jumlah_topping_manis
        jumlah_topping_goang += a.jumlah_topping_goang
        jumlah_topping_keju += a.jumlah_topping_keju
        jumlah_tahu_crispy += a.jumlah_tahu_crispy
        jumlah_tempe_crispy += a.jumlah_tempe_crispy
        jumlah_terong_crispy += a.jumlah_terong_crispy
        jumlah_telur_sayur += a.jumlah_telur_sayur
        jumlah_kol_crispy += a.jumlah_kol_crispy
        jumlah_kerupuk += a.jumlah_kerupuk
        jumlah_sigulmer_manis_biscuit += a.jumlah_sigulmer_manis_biscuit
        jumlah_perkedel += a.jumlah_perkedel
        jumlah_nasi_dine_in += a.jumlah_nasi_dine_in
        jumlah_es_teh_dine_in += a.jumlah_es_teh_dine_in
        jumlah_lemon_tea_dine_in += a.jumlah_lemon_tea_dine_in
        jumlah_milo_dine_in += a.jumlah_milo_dine_in
        jumlah_orange_dine_in += a.jumlah_orange_dine_in
        jumlah_nasi_takeaway += a.jumlah_nasi_takeaway
        jumlah_es_teh_takeaway += a.jumlah_es_teh_takeaway
        jumlah_lemon_tea_takeaway += a.jumlah_lemon_tea_takeaway
        jumlah_milo_takeaway += a.jumlah_milo_takeaway
        jumlah_orange_takeaway += a.jumlah_orange_takeaway
        jumlah_air_mineral += a.jumlah_air_mineral
        jumlah_wings += a.jumlah_wings

    # Gram
    RJC10160201_beras_sania = (156 * jumlah_nasi_dine_in) + (140 * jumlah_nasi_takeaway)

    # Pcs
    SPD10010101_kertas_nasi = (1 * jumlah_nasi_takeaway)

    # Pcs
    BGP10010101_packaging_combo = (1 * jumlah_paper_cost_takeaway_l)

    # Pcs
    BGP10020101_packaging_ala_carte = (1 * jumlah_paper_cost_takeaway_m)

    # Pcs
    BGP10030101_packaging_paper_tray_dine_in = (1 * jumlah_paper_cost_dine_in_paper_tray)

    # Pcs
    BGP10040101_packaging_paper_bag_cokelat = (1 * jumlah_paper_cost_takeaway_paper_bag)

    # Pcs
    SPD10020101_paper_bowl_crisbee = (1 * jumlah_topping_saus_gravy)

    # Pcs
    SPD10020101_tutup_lid_paper_bowl = (1 * jumlah_topping_saus_gravy)

    # Bungkus
    FRS10010201_teh_sisri = (1.25 * jumlah_es_teh_dine_in) + (0.93750 * jumlah_es_teh_takeaway)

    # Gram
    KFL10010101_tepung = (80 * jumlah_ayam) + (17 * jumlah_tahu_crispy) + (17 * jumlah_tempe_crispy) + (17 * jumlah_terong_crispy) + (17 * jumlah_chicken_skin) + (17 * jumlah_kol_crispy)

    # ----------------------- BERSIHIN MINIMAL MAKSIMAL -----------------------
    if math.ceil(RJC10160201_beras_sania/1000/20) <= 5:
        demand_beras = 5
    else:
        demand_beras = math.ceil(RJC10160201_beras_sania/1000/20)

    if math.ceil(SPD10010101_kertas_nasi/1000/15) <= 1:
        demand_kertas_nasi = 1
    else:
        demand_kertas_nasi = math.ceil(SPD10010101_kertas_nasi/1000/15)

    if math.ceil(BGP10010101_packaging_combo/500/2) <= 1:
        demand_packaging_combo = 1
    else:
        demand_packaging_combo = math.ceil(BGP10010101_packaging_combo/500/2)
    
    if math.ceil(BGP10020101_packaging_ala_carte/500/3) <= 1:
        demand_packaging_ala_carte = 1
    else:
        demand_packaging_ala_carte = math.ceil(BGP10020101_packaging_ala_carte/500/3)

    if math.ceil(BGP10030101_packaging_paper_tray_dine_in/500/3) <= 1:
        demand_packaging_paper_tray_dine_in = 1
    else:
        demand_packaging_paper_tray_dine_in = math.ceil(BGP10030101_packaging_paper_tray_dine_in/500/3)

    if math.ceil(BGP10040101_packaging_paper_bag_cokelat/500/3) <= 1:
        demand_packaging_paper_bag_cokelat = 1
    else:
        demand_packaging_paper_bag_cokelat = math.ceil(BGP10040101_packaging_paper_bag_cokelat/500/3)

    if math.ceil(SPD10020101_paper_bowl_crisbee/1000) <= 1:
        demand_paper_bowl_crisbee = 1
    else:
        demand_paper_bowl_crisbee = math.ceil(SPD10020101_paper_bowl_crisbee/1000)
    
    if math.ceil(SPD10020101_tutup_lid_paper_bowl/1000) <= 1:
        demand_tutup_lid_paper_bowl = 1
    else:
        demand_tutup_lid_paper_bowl = math.ceil(SPD10020101_tutup_lid_paper_bowl/1000)

    if math.ceil(jumlah_topping_crisbar/50) <= 10:
        demand_topping_crisbar = 10
    else:
        demand_topping_crisbar = math.ceil(jumlah_topping_crisbar/50)

    if math.ceil(jumlah_topping_matah/30) <= 10:
        demand_topping_matah = 10
    else:
        demand_topping_matah = math.ceil(jumlah_topping_matah/30)

    if math.ceil(jumlah_topping_mamah/10) <= 10:
        demand_topping_mamah = 10
    else:
        demand_topping_mamah = math.ceil(jumlah_topping_mamah/10)

    if math.ceil(jumlah_topping_saus_gravy/30) <= 10:
        demand_topping_saus_gravy = 10
    else:
        demand_topping_saus_gravy = math.ceil(jumlah_topping_saus_gravy/30)

    if math.ceil(FRS10010201_teh_sisri/720) <= 1:
        demand_teh_sisri = 1
    else:
        demand_teh_sisri = math.ceil(FRS10010201_teh_sisri/720)

    if math.ceil(jumlah_sigulmer_manis_biscuit/144) <= 1:
        demand_sigulmer = 1
    else:
        demand_sigulmer = math.ceil(jumlah_sigulmer_manis_biscuit/144)

    if math.ceil(jumlah_perkedel/360) <= 1:
        demand_perkedel = 1
    else:
        demand_perkedel = math.ceil(jumlah_perkedel/360)

    if math.ceil(KFL10010101_tepung/1000/15) <= 5:
        demand_tepung = 5
    else:
        demand_tepung = math.ceil(KFL10010101_tepung/1000/15)

    if math.ceil(jumlah_ayam/960) <= 1:
        demand_sambal_sachet = 1
    else:
        demand_sambal_sachet = math.ceil(jumlah_ayam/960)
    # ----------------------- BERSIHIN MINIMAL MAKSIMAL -----------------------

    # jika maksimal dibawah minimal, pake minimal
    hasil = {
        "minyak_goreng" : { "minimal" : 0, "maksimal" : 7, "satuan" : "Dus", "nama_item" : "Minyak Goreng"},
        "tisu_livi_eco_multipurpose" : {"minimal" : 0,"maksimal" : 1, "satuan" : "Dus", "nama_item" : "Tisu Livi ECO Multipurpose 150's"},
        "tisu_livi_kitchen_towel" : {"minimal" : 0,"maksimal" : 1, "satuan" : "Dus", "nama_item" : "Tisu Livi Kitchen Towel"},
        "lakban_bening" : {"minimal" : 0,"maksimal" : 1, "satuan" : "Pack", "nama_item" : "Lakban Bening 1/2'"},
        "beras_sania" : {"minimal" : 5,"maksimal" : demand_beras, "satuan" : "Karung (20 Kg)", "nama_item" : "Beras Sania 20 Kg"},
        "kertas_roll_printer" : {"minimal" : 0,"maksimal" : 1, "satuan" : "Ball (2 Dus)", "nama_item" : "Dus Kertas Roll Printer"},
        "kertas_nasi_puas" : {"minimal" : 1,"maksimal" : demand_kertas_nasi, "satuan" : "Ball (15 Pack/7500lbr)", "nama_item" : "Kertas Nasi Puas"},
        "packaging_combo" : {"minimal" : 1,"maksimal" : demand_packaging_combo, "satuan" : "Ball (2 Pack/1000 pcs)", "nama_item" : "Packaging Combo"},
        "packaging_ala_carte" : {"minimal" : 1,"maksimal" : demand_packaging_ala_carte, "satuan" : "Ball (3 Pack/1500 pcs)", "nama_item" : "Packaging Ala Carte"},
        "packaging_paper_tray_dine_in" : {"minimal" : 1,"maksimal" : demand_packaging_paper_tray_dine_in, "satuan" : "Ball (3 Pack/1500 pcs)", "nama_item" : "Packaging Paper Tray Dine In"},
        "packaging_paper_bag_cokelat" : {"minimal" : 1,"maksimal" : demand_packaging_paper_bag_cokelat, "satuan" : "Ball (3 Pack/1500 pcs)", "nama_item" : "Packaging Paper Bag Cokelat"},
        "paper_bowl_crisbee_5oz" : {"minimal" : 1,"maksimal" : demand_paper_bowl_crisbee, "satuan" : "Ball (1 Dus/1000 pcs)", "nama_item" : "Paper Bowl Crisbee 5oz"},
        "tutup_lid_paper_bowl_5oz" : {"minimal" : 1,"maksimal" : demand_tutup_lid_paper_bowl, "satuan" : "Ball (1 Dus/1000 pcs)", "nama_item" : "Tutup Lid Paper Bowl 5oz"},
        "brccbs" : {"minimal" : 10,"maksimal" : demand_topping_crisbar, "satuan" : "Pack (50 Porsi)", "nama_item" : "BRCCBS 735 G (Crisbar)"},
        "srmatcs" : {"minimal" : 10,"maksimal" : demand_topping_matah, "satuan" : "Pack (30 Porsi)", "nama_item" : "SRMATCS 345 G (Matah)"},
        "srmamcs" : {"minimal" : 10,"maksimal" : demand_topping_mamah, "satuan" : "Pack (10 Porsi)", "nama_item" : "SRMAMCS 250 G (Mamah)"},
        "jrbcss" : {"minimal" : 10, "maksimal" : demand_topping_saus_gravy, "satuan" : "Pack (30 Porsi)", "nama_item" : "JRBCSS 573 G (Gravy Crisbee)"},
        "dus_teh_sisri" : {"minimal" : 1,"maksimal" : demand_teh_sisri, "satuan" : "Dus (720 Sachet)", "nama_item" : "Dus Teh Sisri"},
        "dus_silky_pudding" : {"minimal" : 1,"maksimal" : demand_sigulmer, "satuan" : "Ball (2 Dus/24 Box)", "nama_item" : "Dus Silky Pudding"},
        "dus_perkedelku" : {"minimal" : 1,"maksimal" : demand_perkedel, "satuan" : "Dus (120 Sachet)", "nama_item" : "Dus Perkedelku"},
        "sak_tepung_fc" : {"minimal" : 0,"maksimal" : 7, "satuan" : "Sak (15 Kg)", "nama_item" : "Sak Tepung FC"},
        "dus_sambal_sachet" : {"minimal" : 1,"maksimal" : demand_sambal_sachet, "satuan" : "Ball (2 Dus/960 Sachet)", "nama_item" : "Dus Sambal Sachet"},
    }

    return hasil