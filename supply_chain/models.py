from django.db import models

# Create your models here.

class KategoriLoyverse(models.Model):
    id_loyverse = models.CharField(max_length=80)
    nama_kategori = models.CharField(max_length=80)

    def __str__(self):
        return self.nama_kategori