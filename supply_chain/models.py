from django.db import models

# Create your models here.

class KategoriLoyverse(models.Model):
    id_loyverse = models.CharField(max_length=80)
    nama_kategori = models.CharField(max_length=80)

    def __str__(self):
        return self.nama_kategori

class CabangLoyverse(models.Model):
    id_loyverse = models.CharField(max_length=80)
    nama_cabang = models.CharField(max_length=80)

    def __str__(self):
        return self.nama_cabang + " - " + self.id_loyverse

class NomorStrukSoldTerakhir(models.Model):
    nomor_struk = models.CharField(max_length=80)

    def __str__(self):
        return self.nomor_struk

class StrukSold(models.Model):
    nomor_struk = models.CharField(max_length=80)
    nama_cabang = models.CharField(max_length=80)
    waktu_struk = models.DateTimeField("Waktu Struk")
    status = models.CharField(max_length=80, null=True)

    jumlah_ayam = models.IntegerField(default=0)
    jumlah_chicken_skin = models.IntegerField(null=True, default=0)
    jumlah_paper_cost_takeaway_l = models.IntegerField(null=True, default=0)
    jumlah_paper_cost_takeaway_m = models.IntegerField(null=True, default=0)
    jumlah_paper_cost_takeaway_paper_bag = models.IntegerField(null=True, default=0)
    jumlah_paper_cost_dine_in_paper_tray = models.IntegerField(null=True, default=0)
    jumlah_topping_crisbar = models.IntegerField(null=True, default=0)
    jumlah_topping_saus_gravy = models.IntegerField(null=True, default=0)
    jumlah_topping_matah = models.IntegerField(null=True, default=0)
    jumlah_topping_mamah = models.IntegerField(null=True, default=0)
    jumlah_topping_tomat = models.IntegerField(null=True, default=0)
    jumlah_topping_manis = models.IntegerField(null=True, default=0)
    jumlah_topping_goang = models.IntegerField(null=True, default=0)
    jumlah_topping_keju = models.IntegerField(null=True, default=0)
    jumlah_tahu_crispy = models.IntegerField(null=True, default=0)
    jumlah_tempe_crispy = models.IntegerField(null=True, default=0)
    jumlah_terong_crispy = models.IntegerField(null=True, default=0)
    jumlah_telur_sayur = models.IntegerField(null=True, default=0)
    jumlah_kol_crispy = models.IntegerField(null=True, default=0)
    jumlah_kerupuk = models.IntegerField(null=True, default=0)
    jumlah_sigulmer_manis_biscuit = models.IntegerField(null=True, default=0)
    jumlah_perkedel = models.IntegerField(null=True, default=0)
    jumlah_nasi_dine_in = models.IntegerField(null=True, default=0)
    jumlah_es_teh_dine_in = models.IntegerField(null=True, default=0)
    jumlah_lemon_tea_dine_in = models.IntegerField(null=True, default=0)
    jumlah_milo_dine_in = models.IntegerField(null=True, default=0)
    jumlah_orange_dine_in = models.IntegerField(null=True, default=0)
    jumlah_nasi_takeaway = models.IntegerField(null=True, default=0)
    jumlah_es_teh_takeaway = models.IntegerField(null=True, default=0)
    jumlah_lemon_tea_takeaway = models.IntegerField(null=True, default=0)
    jumlah_milo_takeaway = models.IntegerField(null=True, default=0)
    jumlah_orange_takeaway = models.IntegerField(null=True, default=0)
    jumlah_air_mineral = models.IntegerField(null=True, default=0)
    jumlah_wings = models.IntegerField(null=True, default=0)

    level_0 = models.IntegerField(null=True, default=0)
    level_1 = models.IntegerField(null=True, default=0)
    level_2 = models.IntegerField(null=True, default=0)
    level_3 = models.IntegerField(null=True, default=0)
    level_4 = models.IntegerField(null=True, default=0)
    level_5 = models.IntegerField(null=True, default=0)
    level_max = models.IntegerField(null=True, default=0)

    geprek = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.nomor_struk