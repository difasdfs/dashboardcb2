
from rm_app.models import ProduksiAyam
from django.utils import timezone
from django.contrib.auth.models import User

def cek_hari(id_pelapornya, hari, cabangnya):
    a = ProduksiAyam.objects.filter(tanggal=hari, cabang=cabangnya)
    
    if not a:
    
        pa = ProduksiAyam(
            id_pelapor = id_pelapornya,
            cabang = cabangnya,
            tanggal = hari,
            waktu_lapor = timezone.now(),
        )
        pa.save()
    