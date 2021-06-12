from datetime import datetime, timedelta
from .models import Struk
import pytz

def main(tanggal_awal, tanggal_akhir):
    waktu_awal = datetime(tanggal_awal.year, tanggal_awal.month, tanggal_awal.day, 8, 0, 0, tzinfo=pytz.UTC) - timedelta(hours=7)
    waktu_akhir = datetime(tanggal_akhir.year, tanggal_akhir.month, tanggal_akhir.day, 23, 59, 59, tzinfo=pytz.UTC) - timedelta(hours=7)

    kumpulan_struk = Struk.objects.filter(created_at__range=[waktu_awal, waktu_akhir])
    
    return len(kumpulan_struk)
    