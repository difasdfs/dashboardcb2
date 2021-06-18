from datetime import date, datetime, timedelta
from investormetro.models import Struk, Sales
import pytz

def main():
    awal_buka = date(2020, 9, 12)
    sekarang = date.today()

    while True:
        if awal_buka <= sekarang:
            # do something
            awal_hari = datetime(awal_buka.year, awal_buka.month, awal_buka.day, hour=8, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC) - timedelta(hours=7)
            akhir_hari = datetime(awal_buka.year, awal_buka.month, awal_buka.day, hour=23, minute=59, second=59, microsecond=0, tzinfo=pytz.UTC) - timedelta(hours=7)

            struk_hari = Struk.objects.filter(created_at__range=[awal_hari, akhir_hari])

            i = 1
            jumlah_struk = len(struk_hari)
            penjualan_sehari = 0
            for struk in struk_hari:
                penjualan_sehari += struk.total_money

            s = Sales(
                tanggal = awal_buka,
                total_sales = penjualan_sehari,
                total_struk = jumlah_struk,
                omset = 0,
                verified = False
            )
            s.save()
            # akhir do something
            awal_buka += timedelta(days=1)
        else:
            break
    
# class Sales(models.Model):
#     tanggal = models.DateField('tanggal')
#     total_sales = models.IntegerField(default=0)
#     total_struk = models.IntegerField(default=0)
#     omset = models.IntegerField(default=0)
#     verified = models.BooleanField(default=False)
    
#     def __str__(self):
#         return str(self.tanggal)
    
    