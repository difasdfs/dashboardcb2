from django.db import models

# Create your models here.
class StrukTerakhir(models.Model):
    nomor_struk = models.CharField(max_length=20)

    def __str__(self):
        return self.nomor_struk

class IdCabangMetro(models.Model):
    id_cabang = models.CharField(max_length=100)

    def __str__(self):
        return self.id_cabang

class Struk(models.Model):
    nomor_struk = models.CharField(max_length=50)
    created_at = models.DateTimeField('created at')
    total_money = models.IntegerField(default=0)
    def __str__(self):
        return self.nomor_struk

class Sales(models.Model):
    tanggal = models.DateField('tanggal')
    total_sales = models.IntegerField(default=0)
    total_struk = models.IntegerField(default=0)
    omset = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.tanggal) + " - " + str(self.verified)