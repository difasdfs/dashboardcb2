from .models import DataStruk

from . import logika_query_tren_penjualan

from dashboard.models import PeriodeKerja
import pytz
from datetime import datetime, timedelta

def total_sales(kumpulan_struk):
    total_sales = 0
    for ks in kumpulan_struk:
        total_sales += ks.total_money_filter()
    return total_sales


def main(periode, kemarin = False):

    periodenya = PeriodeKerja.objects.get(pk=periode)
    
    awal_periode = datetime(periodenya.awal_periode.year, periodenya.awal_periode.month, periodenya.awal_periode.day, 8, 0, 0, tzinfo=pytz.UTC) - timedelta(hours=7)
    akhir_periode = datetime(periodenya.akhir_periode.year, periodenya.akhir_periode.month, periodenya.akhir_periode.day, 23, 59, 59, tzinfo=pytz.UTC) - timedelta(hours=7)
    
    if kemarin:
        selisih = akhir_periode - awal_periode
    else:
        selisih = pytz.utc.localize(datetime.utcnow()) - awal_periode

    kumpulan_struk = DataStruk.objects.filter(created_at__range=[awal_periode, akhir_periode])

    total = total_sales(kumpulan_struk)
     
    try:
        rata_rata = total / selisih.days
    except:
        rata_rata = 0

    return logika_query_tren_penjualan.format_rupiah(rata_rata, total_penjualan = True)


def rata_rata_sales_periode(periode, kemarin = False):

    periodenya = PeriodeKerja.objects.get(pk=periode)
    
    awal_periode = datetime(periodenya.awal_periode.year, periodenya.awal_periode.month, periodenya.awal_periode.day, 8, 0, 0, tzinfo=pytz.UTC) - timedelta(hours=7)
    akhir_periode = datetime(periodenya.akhir_periode.year, periodenya.akhir_periode.month, periodenya.akhir_periode.day, 23, 59, 59, tzinfo=pytz.UTC) - timedelta(hours=7)

    kumpulan_struk = DataStruk.objects.filter(created_at__range=[awal_periode, akhir_periode])

    total = total_sales(kumpulan_struk)

    if kemarin:
        selisih = akhir_periode - awal_periode
    else:
        selisih = pytz.utc.localize(datetime.utcnow()) - awal_periode
    
    try:
        rata_rata = total / selisih.days
    except:
        rata_rata = 0

    return rata_rata

def selisih_tren(periode):
    sekarang = rata_rata_sales_periode(periode)
    kemarinn = rata_rata_sales_periode(periode-1, kemarin=True)
    return logika_query_tren_penjualan.format_rupiah(sekarang-kemarinn, total_penjualan=True)