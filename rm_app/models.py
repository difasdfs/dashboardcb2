from django.db import models
from django.contrib.auth.models import User
# from dashboard.models import DataKaryawan

# Create your models here.
class Cabang(models.Model):
    nama_cabang = models.CharField(max_length=50)

    def __str__(self):
        return self.nama_cabang

class ProfilPengguna(models.Model):
    pengguna = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    cabang = models.ForeignKey(Cabang, on_delete=models.CASCADE)
    jabatan = models.CharField(max_length=50)

    def __str__(self):
        return self.pengguna.first_name + ' - ' + self.cabang.nama_cabang

# untuk query di halaman absen RM Apps
class AbsenTanggal(models.Model):
    tanggal = models.DateField()
    cabang = models.CharField(max_length=50)

    def __str__(self):
        return self.tanggal.strftime("%d %B %Y") + " - " + self.cabang

# untuk menyimpan data absen karyawan
class AbsenKaryawan(models.Model):

    STATUS_ABSEN = (
        ("Hadir", "Hadir"),
        ("Izin", "Izin"),
        ("Sakit", "Sakit"),
        ("Libur", "Libur"),
        ("Cuti", "Cuti"),
        ("Alpha", "Alpha"),
        ("WFH", "WFH"),
    )

    nik = models.CharField(max_length=10)
    tanggal = models.ForeignKey(AbsenTanggal, on_delete=models.CASCADE)
    absen = models.CharField(max_length=10, choices=STATUS_ABSEN)

class ShiftOperasional(models.Model):
    cabang = models.ForeignKey(Cabang, on_delete=models.CASCADE)
    kode = models.CharField(max_length=10)
    deskripsi = models.CharField(max_length=70)
    warna = models.CharField(max_length=12, null=True)

    def __str__(self):
        return self.cabang.nama_cabang + ' - ' + self.kode + ' - ' + self. deskripsi

class ProduksiAyam(models.Model):
    id_pelapor = models.IntegerField()
    cabang = models.ForeignKey(Cabang, on_delete=models.CASCADE)
    tanggal = models.DateField()
    waktu_lapor = models.DateTimeField()

    jam_9_ayam = models.IntegerField(default=0)
    jam_9_nasi = models.IntegerField(default=0)
    jam_9_teh = models.IntegerField(default=0)
    jam_9_milo = models.IntegerField(default=0)
    jam_9_orange = models.IntegerField(default=0)
    jam_9_lemontea = models.IntegerField(default=0)

    jam_10_ayam = models.IntegerField(default=0)
    jam_10_nasi = models.IntegerField(default=0)
    jam_10_teh = models.IntegerField(default=0)
    jam_10_milo = models.IntegerField(default=0)
    jam_10_orange = models.IntegerField(default=0)
    jam_10_lemontea = models.IntegerField(default=0)

    jam_11_ayam = models.IntegerField(default=0)
    jam_11_nasi = models.IntegerField(default=0)
    jam_11_teh = models.IntegerField(default=0)
    jam_11_milo = models.IntegerField(default=0)
    jam_11_orange = models.IntegerField(default=0)
    jam_11_lemontea = models.IntegerField(default=0)

    jam_12_ayam = models.IntegerField(default=0)
    jam_12_nasi = models.IntegerField(default=0)
    jam_12_teh = models.IntegerField(default=0)
    jam_12_milo = models.IntegerField(default=0)
    jam_12_orange = models.IntegerField(default=0)
    jam_12_lemontea = models.IntegerField(default=0)

    jam_13_ayam = models.IntegerField(default=0)
    jam_13_nasi = models.IntegerField(default=0)
    jam_13_teh = models.IntegerField(default=0)
    jam_13_milo = models.IntegerField(default=0)
    jam_13_orange = models.IntegerField(default=0)
    jam_13_lemontea = models.IntegerField(default=0)

    jam_14_ayam = models.IntegerField(default=0)
    jam_14_nasi = models.IntegerField(default=0)
    jam_14_teh = models.IntegerField(default=0)
    jam_14_milo = models.IntegerField(default=0)
    jam_14_orange = models.IntegerField(default=0)
    jam_14_lemontea = models.IntegerField(default=0)

    jam_15_ayam = models.IntegerField(default=0)
    jam_15_nasi = models.IntegerField(default=0)
    jam_15_teh = models.IntegerField(default=0)
    jam_15_milo = models.IntegerField(default=0)
    jam_15_orange = models.IntegerField(default=0)
    jam_15_lemontea = models.IntegerField(default=0)

    jam_16_ayam = models.IntegerField(default=0)
    jam_16_nasi = models.IntegerField(default=0)
    jam_16_teh = models.IntegerField(default=0)
    jam_16_milo = models.IntegerField(default=0)
    jam_16_orange = models.IntegerField(default=0)
    jam_16_lemontea = models.IntegerField(default=0)

    jam_17_ayam = models.IntegerField(default=0)
    jam_17_nasi = models.IntegerField(default=0)
    jam_17_teh = models.IntegerField(default=0)
    jam_17_milo = models.IntegerField(default=0)
    jam_17_orange = models.IntegerField(default=0)
    jam_17_lemontea = models.IntegerField(default=0)

    jam_18_ayam = models.IntegerField(default=0)
    jam_18_nasi = models.IntegerField(default=0)
    jam_18_teh = models.IntegerField(default=0)
    jam_18_milo = models.IntegerField(default=0)
    jam_18_orange = models.IntegerField(default=0)
    jam_18_lemontea = models.IntegerField(default=0)

    jam_19_ayam = models.IntegerField(default=0)
    jam_19_nasi = models.IntegerField(default=0)
    jam_19_teh = models.IntegerField(default=0)
    jam_19_milo = models.IntegerField(default=0)
    jam_19_orange = models.IntegerField(default=0)
    jam_19_lemontea = models.IntegerField(default=0)

    jam_20_ayam = models.IntegerField(default=0)
    jam_20_nasi = models.IntegerField(default=0)
    jam_20_teh = models.IntegerField(default=0)
    jam_20_milo = models.IntegerField(default=0)
    jam_20_orange = models.IntegerField(default=0)
    jam_20_lemontea = models.IntegerField(default=0)

    jam_21_ayam = models.IntegerField(default=0)
    jam_21_nasi = models.IntegerField(default=0)
    jam_21_teh = models.IntegerField(default=0)
    jam_21_milo = models.IntegerField(default=0)
    jam_21_orange = models.IntegerField(default=0)
    jam_21_lemontea = models.IntegerField(default=0)

    jam_22_ayam = models.IntegerField(default=0)
    jam_22_nasi = models.IntegerField(default=0)
    jam_22_teh = models.IntegerField(default=0)
    jam_22_milo = models.IntegerField(default=0)
    jam_22_orange = models.IntegerField(default=0)
    jam_22_lemontea = models.IntegerField(default=0)

    jam_23_ayam = models.IntegerField(default=0)
    jam_23_nasi = models.IntegerField(default=0)
    jam_23_teh = models.IntegerField(default=0)
    jam_23_milo = models.IntegerField(default=0)
    jam_23_orange = models.IntegerField(default=0)
    jam_23_lemontea = models.IntegerField(default=0)

    jam_24_ayam = models.IntegerField(default=0)
    jam_24_nasi = models.IntegerField(default=0)
    jam_24_teh = models.IntegerField(default=0)
    jam_24_milo = models.IntegerField(default=0)
    jam_24_orange = models.IntegerField(default=0)
    jam_24_lemontea = models.IntegerField(default=0)

    jam_1_ayam = models.IntegerField(default=0)
    jam_1_nasi = models.IntegerField(default=0)
    jam_1_teh = models.IntegerField(default=0)
    jam_1_milo = models.IntegerField(default=0)
    jam_1_orange = models.IntegerField(default=0)
    jam_1_lemontea = models.IntegerField(default=0)

    jam_2_ayam = models.IntegerField(default=0)
    jam_2_nasi = models.IntegerField(default=0)
    jam_2_teh = models.IntegerField(default=0)
    jam_2_milo = models.IntegerField(default=0)
    jam_2_orange = models.IntegerField(default=0)
    jam_2_lemontea = models.IntegerField(default=0)

    jam_3_ayam = models.IntegerField(default=0)
    jam_3_nasi = models.IntegerField(default=0)
    jam_3_teh = models.IntegerField(default=0)
    jam_3_milo = models.IntegerField(default=0)
    jam_3_orange = models.IntegerField(default=0)
    jam_3_lemontea = models.IntegerField(default=0)

    stok_ayam = models.FloatField(default=0)
    stok_chicken_skin = models.FloatField(default=0)