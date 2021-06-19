from django.db import models

# Create your models here.
class Layer(models.Model):
    nama = models.CharField(max_length=50)
    def __str__(self):
        return self.nama

class Cabang(models.Model):
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    nama = models.CharField(max_length=50)
    def __str__(self):
        return self.nama

class Kategori(models.Model):
    nama = models.CharField(max_length=200)
    def __str__(self):
        return self.nama

class Item(models.Model):
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    nama = models.CharField(max_length=200)
    #kategori = models.ManyToManyField(Kategori, blank=True)
    def __str__(self):
        return self.nama

class Harga(models.Model):
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    nama = models.CharField(max_length=200, default="Harga")
    harga_dinein = models.IntegerField(default=0)
    harga_takeaway = models.IntegerField(default=0)
    harga_gofood = models.IntegerField(default=0)
    harga_grabfood = models.IntegerField(default=0)
    harga_shopeefood = models.IntegerField(default=0)
    def __str__(self):
        return self.nama

class Modifier(models.Model):
    item = models.ManyToManyField(Item, blank=True)
    nama = models.CharField(max_length=200)
    def __str__(self):
        return self.nama

class Varian(models.Model):
    kategori = models.ForeignKey(Modifier, on_delete=models.CASCADE)
    nama = models.CharField(max_length=200)
    harga = models.IntegerField(default=0)
    def __str__(self):
        return self.nama

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)