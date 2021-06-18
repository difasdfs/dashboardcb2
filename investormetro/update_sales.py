from .models import Sales, Struk
from datetime import date, datetime, timedelta
import pytz

def update_sales(tanggal):
    awal_buka = tanggal
    sekarang = date.today()

    while True:
        if awal_buka == sekarang:
            # do something
            awal_hari = datetime(awal_buka.year, awal_buka.month, awal_buka.day, hour=8, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC) - timedelta(hours=7)
            akhir_hari = datetime(awal_buka.year, awal_buka.month, awal_buka.day, hour=23, minute=59, second=59, microsecond=0, tzinfo=pytz.UTC) - timedelta(hours=7)

            struk_hari = Struk.objects.filter(created_at__range=[awal_hari, akhir_hari])

            i = 1
            jumlah_struk = len(struk_hari)
            penjualan_sehari = 0
            for struk in struk_hari:
                penjualan_sehari += struk.total_money

            try:
                s = Sales.objects.get(tanggal=awal_buka)
                s.total_sales = penjualan_sehari
                s.total_struk = jumlah_struk
                s.save()
            except:
                s = Sales(
                    tanggal = awal_buka,
                    total_sales = penjualan_sehari,
                    total_struk = jumlah_struk,
                    omset = 0,
                    verified = False
                )
                s.save()
            # akhir do something
            break
        elif awal_buka < sekarang:
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

def main():
    hari_ini = date.today()

    semua_sales = Sales.objects.all()
    sales_akhir = semua_sales[len(semua_sales) - 1]
    primary_key = sales_akhir.id
    sales_akhir = Sales.objects.get(pk=primary_key)

    if sales_akhir.tanggal != hari_ini:
        update_sales(sales_akhir.tanggal + timedelta(days=1))
    else:
        update_sales(hari_ini)