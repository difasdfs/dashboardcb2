from dashboard.models import AssemblyProduct

def eksekusi_ini():
    file = open('semua_data_assembly_product.csv')

    for baris in file.readlines():

        kolom = baris.split(';')
        
        a = AssemblyProduct.objects.get(sku=kolom[0])

        sku = kolom[0]
        nama_produk = kolom[1]
        kategori = kolom[2]

        a.paper_cost_takeaway_l = int(kolom[3])
        a.paper_cost_takeaway_m = int(kolom[4])
        a.paper_cost_takeaway_paper_bag = int(kolom[5])
        a.paper_cost_dine_in_paper_tray = int(kolom[6])
        a.ayam = int(kolom[7])
        a.topping_crisbar = int(kolom[9])
        a.topping_saus_gravy = int(kolom[10])
        a.topping_matah = int(kolom[11])
        a.topping_mamah = int(kolom[12])
        a.topping_tomat = int(kolom[13])
        a.topping_manis = int(kolom[14])
        a.topping_goang = int(kolom[15])
        a.topping_keju = int(kolom[16])
        a.tahu_crispy = int(kolom[17])
        a.tempe_crispy = int(kolom[18])
        a.terong_crispy = int(kolom[19])
        a.telur_sayur = int(kolom[20])
        a.chicken_skin = int(kolom[21])
        a.kol_crispy = int(kolom[22])
        a.kerupuk = int(kolom[23])
        a.sigulmer_manis_biscuit = int(kolom[24])
        a.perkedel = int(kolom[25])
        a.nasi_dine_in = int(kolom[26])
        a.es_teh_dine_in = int(kolom[27])
        a.lemon_tea_dine_in = int(kolom[28])
        a.milo_dine_in = int(kolom[29])
        a.orange_dine_in = int(kolom[30])
        a.nasi_takeaway = int(kolom[31])
        a.es_teh_takeaway = int(kolom[32])
        a.lemon_tea_takeaway = int(kolom[33])
        a.milo_takeaway = int(kolom[34])
        a.orange_takeaway = int(kolom[35])
        a.air_mineral = int(kolom[36])
        a.save()

    file.close()