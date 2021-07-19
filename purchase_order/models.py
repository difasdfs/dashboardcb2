from django.db import models
from rm_app.models import ProfilPengguna
# Create your models here.

class PurchaseOrder(models.Model):
    profil_pengguna = models.ForeignKey(ProfilPengguna, on_delete=models.CASCADE)
    nomor_po = models.CharField(max_length=20)
    nama_pic = models.CharField(max_length=50, null=True)
    nomor_pic = models.CharField(max_length=50, null=True)
    alamat = models.CharField(max_length=100, null=True)
    tanggal_po = models.DateField(null=True)
    
    def __str__(self):
        return self.nomor_po

    def format_tanggal(self):
        return self.tanggal_po.strftime("%d %b %Y"),

class BarangPurchaseOrder(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    nama_item = models.CharField(max_length=30)
    jumlah_order = models.IntegerField()
    satuan = models.CharField(max_length=30)

    def __str__(self):
        return self.purchase_order.nomor_po + " - " + self.nama_item

class StatusPurchaseOrder(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    status = models.CharField(max_length=70) # Belum Diterima, Diterima Lengkap, Diterima Tidak Lengkap
    
    def __str__(self):
        return self.purchase_order.nomor_po + " - " + self.status
	
class BarangDiterima(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    diterima_sebenarnya = models.ForeignKey(BarangPurchaseOrder, on_delete=models.CASCADE, null=True)
    nama_barang = models.CharField(max_length=150)
    jumlah_diterima = models.IntegerField()

    def __str__(self):
        return self.purchase_order.nomor_po + " - " + self.nama_barang + " - " + str(self.jumlah_diterima)
