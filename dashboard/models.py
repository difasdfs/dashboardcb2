from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import pytz
import locale
import string
import random

# Create your models here.

class TugasProyek(models.Model):
    STATUS = (
        ('Tuntas', 'Tuntas'),
        ('Hold', 'Hold'),
        ('On Progress', 'On Progress'),
        ('Selesai', 'Selesai'),
        ('Deadline', 'Deadline'),
        ('Terlambat', 'Terlambat')
    )

    pemilik_tugas = models.ForeignKey(User, on_delete=models.CASCADE)
    judul = models.CharField(max_length=150)
    isi = models.CharField(max_length=1000)
    deadline = models.DateTimeField('Deadline')
    status = models.CharField(max_length=15, choices=STATUS)
    bukti = models.CharField(max_length=100, null=True)
    penilaian = models.IntegerField(null=True)
    bagian = models.CharField(max_length = 100, null=True)
    komentar = models.CharField(max_length=1000)
    selesai_pada = models.DateTimeField('Selesai pada', null=True)
    link_bukti = models.CharField(max_length=1000, null=True)
    archive = models.BooleanField(null=True, default=False)
    ketuntasan = models.BooleanField(null=True, default=False)

    def __str__(self):
        return self.judul

class TugasRutin(models.Model):
    pemilik_tugas = models.ForeignKey(User, on_delete=models.CASCADE)
    judul = models.CharField(max_length=150)
    isi = models.CharField(max_length=1000)
    bagian = models.CharField(max_length=150, null=True)
    archive = models.BooleanField(null=True)

    def __str__(self):
        return self.judul

class IsiTugasRutin(models.Model):
    STATUS = (
        ('Tuntas', 'Tuntas'),
        ('Hold', 'Hold'),
        ('On Progress', 'On Progress'),
        ('Selesai', 'Selesai'),
        ('Deadline', 'Deadline'),
    )

    tugas_rutin = models.ForeignKey(TugasRutin, on_delete=models.CASCADE)
    deadline = models.DateTimeField('Deadline')
    status = models.CharField(max_length=15, choices=STATUS)
    bukti = models.CharField(max_length=100, null=True)
    penilaian = models.IntegerField(null=True)
    komentar = models.CharField(max_length=1000)
    link_bukti = models.CharField(max_length=1000, null=True, default='#')
    selesai_pada = models.DateTimeField('Selesai pada', null=True)
    ketuntasan = models.BooleanField(null=True, default=False)
    judul = models.CharField(max_length=150, null=True)
    isi = models.CharField(max_length=1000, null=True)

class PeriodeSp(models.Model):
    nama_periode = models.CharField(max_length=100)
    tahun = models.IntegerField()
    awal_periode = models.DateTimeField('Awal periode')
    akhir_periode = models.DateTimeField('Akhir Periode')
    dieksekusi = models.BooleanField(default=False)

    def __str__(self):
        return self.nama_periode

# ini model gagal
class KenaSp(models.Model):
    periode_sp = models.ForeignKey(PeriodeSp, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    berakhir_pada = models.DateTimeField('Berakhir pada')
    keaktifan = models.BooleanField(default=True)

    def __str__(self):
        user = User.objects.get(pk=self.id_user)
        return user.first_name

# ini yang dipake
class SuratPeringatan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mulai_sp = models.DateField()
    berakhir_sp = models.DateField()
    keaktifan = models.BooleanField()

    def berakhir_dalam(self):
        selisih = self.berakhir_sp - datetime.date.today()
        return selisih.days


class DataKaryawan(models.Model):
    AREA = (
        ('Office', 'Office'),
        ('Antapani', 'Antapani'),
        ('Jatinangor', 'Jatinangor'),
        ('Cisitu', 'Cisitu'),
        ('Unjani', 'Unjani'),
        ('Metro', 'Metro'),
        ('Sukajadi', 'Sukajadi'),
        ('Telkom Sukabirus', 'Telkom Sukabirus'),
        ('Telkom Sukapura', 'Telkom Sukapura'),
	    ('Kopo','Kopo'),
    )

    JENIS_KELAMIN = (
        ('L', 'L'),
        ('P', 'P'),
    )

    PENDIDIKAN = (
        ('SD', 'SD'),
        ('SMP', 'SMP'),
        ('SMA/SMK', 'SMA/SMK'),
        ('D3', 'D3'),
        ('S1', 'S1'),
        ('S2', 'S2'),
        ('S3', 'S3'),
    )

    MARITAL = (
        ('BELUM MENIKAH', 'BELUM MENIKAH'),
        ('MENIKAH', 'MENIKAH'),
        ('CERAI', 'CERAI')
    )

    STATUS = (
        ('AKTIF','AKTIF'),
        ('KELUAR', 'KELUAR'),
    )

    nik = models.CharField(max_length=4, null=True)
    no_id_fingerprint = models.IntegerField()
    nama = models.CharField(max_length=100)
    area = models.CharField(max_length=30, choices=AREA)
    level_manajemen = models.CharField(max_length=40)
    nama_posisi = models.CharField(max_length=30)
    kode_posisi = models.CharField(max_length=5)
    status_jabatan = models.CharField(max_length=40, null=True)
    jabatan_baru = models.CharField(max_length=40, null=True)
    status_pegawai = models.CharField(max_length=50, null=True)
    tanggal_masuk = models.DateField('Tanggal Masuk', null=True)
    lama_bekerja = models.CharField(max_length=100, null=True)
    no_ktp = models.CharField(max_length=30, null=True)
    tempat_lahir = models.CharField(max_length=40, null=True)
    umur = models.IntegerField(null=True)
    tanggal_lahir = models.DateField('Tanggal Lahir', null=True)
    jenis_kelamin = models.CharField(max_length=1, choices=JENIS_KELAMIN)
    agama = models.CharField(max_length=20, null=True)
    pendidikan = models.CharField(max_length=10, choices=PENDIDIKAN)
    jurusan = models.CharField(max_length=40, null=True)
    alamat = models.CharField(max_length=100, null=True)
    no_hp = models.CharField(max_length=20)
    marital_status = models.CharField(max_length=20, choices=MARITAL)
    anak = models.IntegerField()
    no_rekening = models.CharField(max_length=100, null=True)
    bpjs_ketenagakerjaan = models.CharField(max_length=100, null=True)
    nama_darurat = models.CharField(max_length=100, null=True)
    alamat_darurat = models.CharField(max_length=100, null=True)
    hubungan_darurat = models.CharField(max_length=100, null=True)
    no_hp_darurat = models.CharField(max_length=100, null=True)

    status = models.CharField(max_length=100, null=True, choices=STATUS)

    tanggal_keluar = models.DateField('Tanggal Keluar', null=True)
    alasan_keluar = models.CharField(max_length=200, null=True)
    # metod lama bekerja
    # umur
    def __str__(self):
        return self.nama

    def pasang_nik(self):
        nike = str(self.id)
        tampilan = '000' + nike
        self.nik = tampilan[-4:]

    def inisialisasi(self):
        self.nama = self.nama.upper()
        self.alamat = self.alamat.upper()
        self.tempat_lahir = self.tempat_lahir.upper()
        self.kode_posisi = self.kode_posisi.upper()
        self.agama = self.agama.upper()

    def update_data(self):
        # umur
        if self.status != 'KELUAR':
            lahir = self.tanggal_lahir
            hariini = datetime.date.today()
            selisih = hariini - lahir
            self.umur = selisih.days // 365

            # lama bekerja
            masuk = self.tanggal_masuk
            selisih = hariini - masuk
            
            # ngitung hari
            selisih = selisih.days

            # ngitung tahun
            tahun = selisih // 365
            selisih = selisih - (tahun*365)

            # ngitung bulan
            bulan = selisih // 30
            selisih = selisih - (bulan*30)

            self.lama_bekerja = str(tahun) + " tahun, " + str(bulan) + " bulan, " + str(selisih) + " hari"


class DataStruk(models.Model):
    nomor_struk = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    outlet = models.CharField(max_length=70)
    nama_pembayaran = models.CharField(max_length=70)
    tipe_struk = models.CharField(max_length=70)
    money_amount = models.IntegerField()

    def __str__(self):
        return self.nomor_struk + ' - ' + self.tipe_struk
    
class NomorStrukTerakhir(models.Model):
    nomor_struk = models.CharField(max_length=50)

    def __str__(self):
        return self.nomor_struk

class AverageCheck(models.Model):
    hari = models.DateField()
    awal_hari = models.DateTimeField()
    akhir_hari = models.DateTimeField()
    total_check = models.IntegerField(default=0, null=True)
    total_sales = models.IntegerField(default=0, null=True)
    total_check_online = models.IntegerField(default=0, null=True)
    total_sales_online = models.IntegerField(default=0, null=True)
    average_check = models.FloatField(default=0, null=True)
    average_check_online = models.FloatField(default=0, null=True)
    
    total_check_antapani = models.IntegerField(default=0, null=True)
    total_check_online_antapani = models.IntegerField(default=0, null=True)
    average_check_antapani = models.FloatField(default=0, null=True)
    average_check_online_antapani = models.FloatField(default=0, null=True)
    total_sales_antapani = models.IntegerField(default=0, null=True)
    total_sales_online_antapani = models.IntegerField(default=0, null=True)

    total_check_metro = models.IntegerField(default=0, null=True)
    total_check_online_metro = models.IntegerField(default=0, null=True)
    average_check_metro = models.FloatField(default=0, null=True)
    average_check_online_metro = models.FloatField(default=0, null=True)
    total_sales_metro = models.IntegerField(default=0, null=True)
    total_sales_online_metro = models.IntegerField(default=0, null=True)

    total_check_jatinangor = models.IntegerField(default=0, null=True)
    total_check_online_jatinangor = models.IntegerField(default=0, null=True)
    average_check_jatinangor = models.FloatField(default=0, null=True)
    average_check_online_jatinangor = models.FloatField(default=0, null=True)
    total_sales_jatinangor = models.IntegerField(default=0, null=True)
    total_sales_online_jatinangor = models.IntegerField(default=0, null=True)

    total_check_sukapura = models.IntegerField(default=0, null=True)
    total_check_online_sukapura = models.IntegerField(default=0, null=True)
    average_check_sukapura = models.FloatField(default=0, null=True)
    average_check_online_sukapura = models.FloatField(default=0, null=True)
    total_sales_sukapura = models.IntegerField(default=0, null=True)
    total_sales_online_sukapura = models.IntegerField(default=0, null=True)

    total_check_sukabirus = models.IntegerField(default=0, null=True)
    total_check_online_sukabirus = models.IntegerField(default=0, null=True)
    average_check_sukabirus = models.FloatField(default=0, null=True)
    average_check_online_sukabirus = models.FloatField(default=0, null=True)
    total_sales_sukabirus = models.IntegerField(default=0, null=True)
    total_sales_online_sukabirus = models.IntegerField(default=0, null=True)

    total_check_unjani = models.IntegerField(default=0, null=True)
    total_check_online_unjani = models.IntegerField(default=0, null=True)
    average_check_unjani = models.FloatField(default=0, null=True)
    average_check_online_unjani = models.FloatField(default=0, null=True)
    total_sales_unjani = models.IntegerField(default=0, null=True)
    total_sales_online_unjani = models.IntegerField(default=0, null=True)

    total_check_cisitu = models.IntegerField(default=0, null=True)
    total_check_online_cisitu = models.IntegerField(default=0, null=True)
    average_check_cisitu = models.FloatField(default=0, null=True)
    average_check_online_cisitu = models.FloatField(default=0, null=True)
    total_sales_cisitu = models.IntegerField(default=0, null=True)
    total_sales_online_cisitu = models.IntegerField(default=0, null=True)

    total_check_sukajadi = models.IntegerField(default=0, null=True)
    total_check_online_sukajadi = models.IntegerField(default=0, null=True)
    average_check_sukajadi = models.FloatField(default=0, null=True)
    average_check_online_sukajadi = models.FloatField(default=0, null=True)
    total_sales_sukajadi = models.IntegerField(default=0, null=True)
    total_sales_online_sukajadi = models.IntegerField(default=0, null=True)

    def tentukan_awal_akhir_hari(self):
        self.awal_hari = datetime.datetime(self.hari.year, self.hari.month, self.hari.day, 0, 0, 1, 0, tzinfo=pytz.UTC) - datetime.timedelta(hours=7)
        self.akhir_hari = datetime.datetime(self.hari.year, self.hari.month, self.hari.day, 23, 59, 59, 0, tzinfo=pytz.UTC) - datetime.timedelta(hours=7) 

    def formatnya(self, angka):

        if isinstance(angka, float):
            angka = str(angka)
            angka = angka.split('.')
            angka = angka[0]
            angka = int(angka)

        if angka >= 1000000:
            jutaan = angka // 1000000
            pengurang = jutaan * 1000000
            angka = angka - pengurang

            ribuan = angka // 1000
            pengurang = ribuan * 1000
            ribuan = "00000" + str(ribuan)
            ribuan = ribuan[-3:]

            angka = angka - pengurang
            sisa = '00000' + str(angka)
            sisa = sisa[-3:]

            return "Rp. " + str(jutaan) + '.' + ribuan + '.' + sisa
        elif angka >= 1000:
            ribuan = angka // 1000
            pengurang = ribuan * 1000
            angka = angka - pengurang

            sisa = '00000' + str(angka)
            sisa = sisa[-3:]
            
            return "Rp. " + str(ribuan) + '.' + sisa

class PeriodeKerja(models.Model):
    periode = models.CharField(max_length=50)
    awal_periode = models.DateField() # 26 bulan sebelumnya
    akhir_periode = models.DateField() # 25 bulan periode

    def __str__(self):
        return self.periode

class OmsetBulan(models.Model):
    periode = models.ForeignKey(PeriodeKerja, on_delete=models.CASCADE)
    omset_bulan_ini = models.IntegerField()
    omset_bulan_sebelumnya = models.IntegerField()
    target_omset = models.IntegerField()

    def __str__(self):
        return "Omset " + self.periode.periode

    def dapatkan_omset_bulan_sebelumnya(self):
        idnya = self.id - 1
        d = OmsetBulan.objects.get(pk=idnya)
        self.omset_bulan_sebelumnya = d.omset_bulan_ini
        self.save()

    # UNTUK UPDATE
    def hitung_omset_bulan(self):
        awal = self.periode.awal_periode
        akhir = self.periode.akhir_periode
        awal_hitung = datetime.datetime(awal.year, awal.month, awal.day, 0, 0, 1, tzinfo=pytz.UTC) - datetime.timedelta(hours=7)
        akhir_hitung = datetime.datetime(akhir.year, akhir.month, akhir.day, 23, 59, 59, tzinfo=pytz.UTC) - datetime.timedelta(hours=7)
        ds = DataStruk.objects.filter(created_at__range=[awal_hitung, akhir_hitung])
        omset = 0
        for s in ds:
            omset += s.money_amount
        self.omset_bulan_ini = omset
        self.save()

    def sales_to_target(self):
        awal = self.periode.awal_periode
        akhir = self.periode.akhir_periode
        berapa_hari = akhir-awal
        berapa_hari = berapa_hari.days

        if berapa_hari <= 0:
            return 0

        omset_yang_kurang = self.target_omset - self.omset_bulan_ini

        if omset_yang_kurang <= 0:
            return 0

        sales_to_targetnya = omset_yang_kurang / berapa_hari

        return sales_to_targetnya

    def selisih_omset_target(self):
        selisih = self.omset_bulan_ini - self.target_omset
        if selisih == 0:
            return "0"
        elif selisih > 0:
            return "+" + self.formatnya(selisih)
        else:
            selisih = abs(selisih)
            return "-" + self.formatnya(selisih)

    def selisih_omset_bulan(self):
        selisih = self.omset_bulan_ini - self.omset_bulan_sebelumnya
        if selisih == 0:
            return "0"
        elif selisih > 0:
            return "+" + self.formatnya(selisih)
        else:
            selisih = -selisih
            return "-" + self.formatnya(selisih)

    def formatnya(self, angka):

        if isinstance(angka, float):
            angka = str(angka)
            angka = angka.split('.')
            angka = angka[0]
            angka = int(angka)

        if angka >= 1000000000:
            milyaran = angka // 1000000000
            pengurang = milyaran * 1000000000
            angka = angka - pengurang

            jutaan = angka // 1000000
            pengurang = jutaan * 1000000
            jutaan = "00000" + str(jutaan)
            jutaan = jutaan[-3:]
            angka = angka - pengurang

            ribuan = angka // 1000
            pengurang = ribuan * 1000
            ribuan = "00000" + str(ribuan)
            ribuan = ribuan[-3:]

            angka = angka - pengurang
            sisa = '00000' + str(angka)
            sisa = sisa[-3:]

            return "Rp. " + str(milyaran) + '.' + str(jutaan) + '.' + ribuan + '.' + sisa

        elif angka >= 1000000:
            jutaan = angka // 1000000
            pengurang = jutaan * 1000000
            angka = angka - pengurang

            ribuan = angka // 1000
            pengurang = ribuan * 1000
            ribuan = "00000" + str(ribuan)
            ribuan = ribuan[-3:]

            angka = angka - pengurang
            sisa = '00000' + str(angka)
            sisa = sisa[-3:]

            return "Rp. " + str(jutaan) + '.' + ribuan + '.' + sisa
        elif angka >= 1000:
            ribuan = angka // 1000
            pengurang = ribuan * 1000
            angka = angka - pengurang

            sisa = '00000' + str(angka)
            sisa = sisa[-3:]
            
            return "Rp. " + str(ribuan) + '.' + sisa
        else:
            return str(angka)


class Complaint(models.Model):
    CABANG = [
        ("Antapani", "Antapani"),
        ("Cisitu", "Cisitu"),
        ("Jatinangor", "Jatinangor"),
        ("Metro", "Metro"),
        ("Sukapura", "Sukapura"),
        ("Sukabirus", "Sukabirus"),
        ("Sukajadi", "Sukajadi"),
        ("Unjani", "Unjani"),
    ]

    JENIS = [
        ("Kualitas Produk", "Kualitas Produk"),
        ("Kebersihan", "Kebersihan"),
        ("Pelayanan", "Pelayanan"),
        ("Tidak Lengkap", "Tidak Lengkap"),
        ("Lainnya", "Lainnya")
    ]

    tanggal = models.DateField()
    jam_operasional = models.TimeField()
    nama = models.CharField(max_length=100)
    media_penyampaian_complain = models.CharField(max_length=100)
    nomor_kontak = models.CharField(max_length=30)
    complaint = models.TextField(max_length=1000)
    handling = models.CharField(max_length=100)
    jenis = models.CharField(max_length=100, choices=JENIS, null=True)
    cabang = models.CharField(max_length=100, choices=CABANG)
    status = models.CharField(max_length=100, null=True)

class MysteryGuest(models.Model):
    CABANG = [
        ("Antapani", "Antapani"),
        ("Cisitu", "Cisitu"),
        ("Jatinangor", "Jatinangor"),
        ("Metro", "Metro"),
        ("Sukapura", "Sukapura"),
        ("Sukabirus", "Sukabirus"),
        ("Sukajadi", "Sukajadi"),
        ("Unjani", "Unjani"),
    ]

    cabang = models.CharField(max_length=100, choices=CABANG)
    nama = models.CharField(max_length=100)
    tanggal = models.DateField()
    nilai_appearance = models.FloatField()
    komentar_appearance = models.TextField(max_length=1000)
    nilai_aroma = models.FloatField()
    komentar_aroma = models.TextField(max_length=1000)
    nilai_rasa = models.FloatField()
    komentar_rasa = models.TextField(max_length=1000)
    nilai_overall = models.FloatField()
    komentar_overall = models.TextField(max_length=1000)
    dokumentasi_luar = models.CharField(max_length=100)
    dokumentasi_dalam = models.CharField(max_length=100)
    nilai_manajemen = models.FloatField()

class KepuasanPelanggan(models.Model):
    tanggal = models.DateField()
    
    google_antapani = models.FloatField()
    google_cisitu = models.FloatField()
    google_jatinangor = models.FloatField()
    google_metro = models.FloatField()
    google_sukabirus = models.FloatField()
    google_sukapura = models.FloatField()
    google_sukajadi = models.FloatField()
    google_unjani = models.FloatField()

    gofood_antapani = models.FloatField()
    gofood_cisitu = models.FloatField()
    gofood_jatinangor = models.FloatField()
    gofood_metro = models.FloatField()
    gofood_sukabirus = models.FloatField()
    gofood_sukapura = models.FloatField()
    gofood_sukajadi = models.FloatField()
    gofood_unjani = models.FloatField()

    grabfood_antapani = models.FloatField()
    grabfood_cisitu = models.FloatField()
    grabfood_jatinangor = models.FloatField()
    grabfood_metro = models.FloatField()
    grabfood_sukabirus = models.FloatField()
    grabfood_sukapura = models.FloatField()
    grabfood_sukajadi = models.FloatField()
    grabfood_unjani = models.FloatField()

    survei_antapani = models.FloatField()
    survei_cisitu = models.FloatField()
    survei_jatinangor = models.FloatField()
    survei_metro = models.FloatField()
    survei_sukabirus = models.FloatField()
    survei_sukapura = models.FloatField()
    survei_sukajadi = models.FloatField()
    survei_unjani = models.FloatField()

    def __str__(self):
        return str(self.tanggal)

    def dapat_average(self, cabang):
        hasil = 0
        if cabang == "Antapani":
            hasil = self.google_antapani + self.gofood_antapani + self.grabfood_antapani + self.survei_antapani
        elif cabang == "Cisitu" :
            hasil = self.google_cisitu + self.gofood_cisitu + self.grabfood_cisitu + self.survei_cisitu
        elif cabang == "Jatinangor" :
            hasil = self.google_jatinangor + self.gofood_jatinangor + self.grabfood_jatinangor + self.survei_jatinangor
        elif cabang == "Metro" :
            hasil = self.google_metro + self.gofood_metro + self.grabfood_metro + self.survei_metro
        elif cabang == "Sukabirus" :
            hasil = self.google_sukabirus + self.gofood_sukabirus + self.grabfood_sukabirus + self.survei_sukabirus
        elif cabang == "Sukapura" :
            hasil = self.google_sukapura + self.gofood_sukapura + self.grabfood_sukapura + self.survei_sukapura
        elif cabang == "Sukajadi" :
            hasil = self.google_sukajadi + self.gofood_sukajadi + self.grabfood_sukajadi + self.survei_sukajadi
        elif cabang == "Unjani" :
            hasil = self.google_unjani + self.gofood_unjani + self.grabfood_unjani + self.survei_unjani

        hasil /=4
        return hasil

    def dapat_average_semua(self):
        hasil = self.google_antapani + self.google_cisitu + self.google_jatinangor + self.google_metro + self.google_sukabirus + self.google_sukapura + self.google_sukajadi + self.google_unjani
        hasil += self.gofood_antapani + self.gofood_cisitu + self.gofood_jatinangor + self.gofood_metro + self.gofood_sukabirus + self.gofood_sukapura + self.gofood_sukajadi + self.gofood_unjani
        hasil += self.grabfood_antapani + self.grabfood_cisitu + self.grabfood_jatinangor + self.grabfood_metro + self.grabfood_sukabirus + self.grabfood_sukapura + self.grabfood_sukajadi + self.grabfood_unjani
        hasil += self.survei_antapani + self.survei_cisitu + self.survei_jatinangor + self.survei_metro + self.survei_sukabirus + self.survei_sukapura + self.survei_sukajadi + self.survei_unjani
        hasil /= 32

        hasil = "{:.2f}".format(hasil)

        return float(hasil)

class TanggalWeekendWeekdays(models.Model):
    tanggal = models.DateField()
    weekend = models.BooleanField(default=False)

    def __str__(self):
        return str(self.tanggal)

class AssemblyProduct(models.Model):
    sku = models.CharField(max_length=30)
    nama = models.CharField(max_length=100, null=True)
    kategori = models.CharField(max_length=50, null=True)
    ayam = models.IntegerField()

class PemakaianAyam(models.Model):
    tanggal = models.DateField()
    pemakaian_ayam = models.IntegerField(default=0)
    pemakaian_ayam_antapani = models.IntegerField(default=0)
    pemakaian_ayam_jatinangor = models.IntegerField(default=0)
    pemakaian_ayam_metro = models.IntegerField(default=0)
    pemakaian_ayam_sukapura = models.IntegerField(default=0)
    pemakaian_ayam_sukabirus = models.IntegerField(default=0)
    pemakaian_ayam_unjani = models.IntegerField(default=0)
    pemakaian_ayam_cisitu = models.IntegerField(default=0)
    pemakaian_ayam_sukajadi = models.IntegerField(default=0)
    dieksekusi = models.BooleanField(default=False)

    def __str__(self):
        return str(self.tanggal) + " - " + str(self.pemakaian_ayam)

class TokenTest(models.Model):
    aktif = models.BooleanField(default=True)
    token = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.token

    def generate_unique_token(self):
        while True:
            tokennya = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            t = TokenTest.objects.filter(token=tokennya)
            if t:
                continue
            else:
                self.token = tokennya
                break
    
class PesertaTest(models.Model):
    token = models.ForeignKey(TokenTest, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()
    pendidikan_terakhir = models.CharField(max_length=20)
    tanggal_test = models.DateField()
    umur = models.IntegerField(null=True)

    def __str__(self):
        return self.nama

    def hitung_umur(self):
        sekarang = datetime.date.today()
        tanggal_lahir = self.tanggal_lahir
        selisih = sekarang - tanggal_lahir
        hari = selisih.days
        self.umur = hari // 365

class JawabanIst(models.Model):
    peserta_test = models.ForeignKey(PesertaTest, on_delete=models.CASCADE)
    se_1 = models.CharField(max_length=1, null=True)
    se_2 = models.CharField(max_length=1, null=True)
    se_3 = models.CharField(max_length=1, null=True)
    se_4 = models.CharField(max_length=1, null=True)
    se_5 = models.CharField(max_length=1, null=True)
    se_6 = models.CharField(max_length=1, null=True)
    se_7 = models.CharField(max_length=1, null=True)
    se_8 = models.CharField(max_length=1, null=True)
    se_9 = models.CharField(max_length=1, null=True)
    se_10 = models.CharField(max_length=1, null=True)
    se_11 = models.CharField(max_length=1, null=True)
    se_12 = models.CharField(max_length=1, null=True)
    se_13 = models.CharField(max_length=1, null=True)
    se_14 = models.CharField(max_length=1, null=True)
    se_15 = models.CharField(max_length=1, null=True)
    se_16 = models.CharField(max_length=1, null=True)
    se_17 = models.CharField(max_length=1, null=True)
    se_18 = models.CharField(max_length=1, null=True)
    se_19 = models.CharField(max_length=1, null=True)
    se_20 = models.CharField(max_length=1, null=True)

    wa_1 = models.CharField(max_length=1, null=True)
    wa_2 = models.CharField(max_length=1, null=True)
    wa_3 = models.CharField(max_length=1, null=True)
    wa_4 = models.CharField(max_length=1, null=True)
    wa_5 = models.CharField(max_length=1, null=True)
    wa_6 = models.CharField(max_length=1, null=True)
    wa_7 = models.CharField(max_length=1, null=True)
    wa_8 = models.CharField(max_length=1, null=True)
    wa_9 = models.CharField(max_length=1, null=True)
    wa_10 = models.CharField(max_length=1, null=True)
    wa_11 = models.CharField(max_length=1, null=True)
    wa_12 = models.CharField(max_length=1, null=True)
    wa_13 = models.CharField(max_length=1, null=True)
    wa_14 = models.CharField(max_length=1, null=True)
    wa_15 = models.CharField(max_length=1, null=True)
    wa_16 = models.CharField(max_length=1, null=True)
    wa_17 = models.CharField(max_length=1, null=True)
    wa_18 = models.CharField(max_length=1, null=True)
    wa_19 = models.CharField(max_length=1, null=True)
    wa_20 = models.CharField(max_length=1, null=True)

    an_1 = models.CharField(max_length=1, null=True)
    an_2 = models.CharField(max_length=1, null=True)
    an_3 = models.CharField(max_length=1, null=True)
    an_4 = models.CharField(max_length=1, null=True)
    an_5 = models.CharField(max_length=1, null=True)
    an_6 = models.CharField(max_length=1, null=True)
    an_7 = models.CharField(max_length=1, null=True)
    an_8 = models.CharField(max_length=1, null=True)
    an_9 = models.CharField(max_length=1, null=True)
    an_10 = models.CharField(max_length=1, null=True)
    an_11 = models.CharField(max_length=1, null=True)
    an_12 = models.CharField(max_length=1, null=True)
    an_13 = models.CharField(max_length=1, null=True)
    an_14 = models.CharField(max_length=1, null=True)
    an_15 = models.CharField(max_length=1, null=True)
    an_16 = models.CharField(max_length=1, null=True)
    an_17 = models.CharField(max_length=1, null=True)
    an_18 = models.CharField(max_length=1, null=True)
    an_19 = models.CharField(max_length=1, null=True)
    an_20 = models.CharField(max_length=1, null=True)

    ge_1 = models.CharField(max_length=20, null=True)
    ge_2 = models.CharField(max_length=20, null=True)
    ge_3 = models.CharField(max_length=20, null=True)
    ge_4 = models.CharField(max_length=20, null=True)
    ge_5 = models.CharField(max_length=20, null=True)
    ge_6 = models.CharField(max_length=20, null=True)
    ge_7 = models.CharField(max_length=20, null=True)
    ge_8 = models.CharField(max_length=20, null=True)
    ge_9 = models.CharField(max_length=20, null=True)
    ge_10 = models.CharField(max_length=20, null=True)
    ge_11 = models.CharField(max_length=20, null=True)
    ge_12 = models.CharField(max_length=20, null=True)
    ge_13 = models.CharField(max_length=20, null=True)
    ge_14 = models.CharField(max_length=20, null=True)
    ge_15 = models.CharField(max_length=20, null=True)
    ge_16 = models.CharField(max_length=20, null=True)
    
    ra_1 = models.CharField(max_length=20, null=True)
    ra_2 = models.CharField(max_length=20, null=True)
    ra_3 = models.CharField(max_length=20, null=True)
    ra_4 = models.CharField(max_length=20, null=True)
    ra_5 = models.CharField(max_length=20, null=True)
    ra_6 = models.CharField(max_length=20, null=True)
    ra_7 = models.CharField(max_length=20, null=True)
    ra_8 = models.CharField(max_length=20, null=True)
    ra_9 = models.CharField(max_length=20, null=True)
    ra_10 = models.CharField(max_length=20, null=True)
    ra_11 = models.CharField(max_length=20, null=True)
    ra_12 = models.CharField(max_length=20, null=True)
    ra_13 = models.CharField(max_length=20, null=True)
    ra_14 = models.CharField(max_length=20, null=True)
    ra_15 = models.CharField(max_length=20, null=True)
    ra_16 = models.CharField(max_length=20, null=True)
    ra_17 = models.CharField(max_length=20, null=True)
    ra_18 = models.CharField(max_length=20, null=True)
    ra_19 = models.CharField(max_length=20, null=True)
    ra_20 = models.CharField(max_length=20, null=True)

    zr_1 = models.CharField(max_length=20, null=True)
    zr_2 = models.CharField(max_length=20, null=True)
    zr_3 = models.CharField(max_length=20, null=True)
    zr_4 = models.CharField(max_length=20, null=True)
    zr_5 = models.CharField(max_length=20, null=True)
    zr_6 = models.CharField(max_length=20, null=True)
    zr_7 = models.CharField(max_length=20, null=True)
    zr_8 = models.CharField(max_length=20, null=True)
    zr_9 = models.CharField(max_length=20, null=True)
    zr_10 = models.CharField(max_length=20, null=True)
    zr_11 = models.CharField(max_length=20, null=True)
    zr_12 = models.CharField(max_length=20, null=True)
    zr_13 = models.CharField(max_length=20, null=True)
    zr_14 = models.CharField(max_length=20, null=True)
    zr_15 = models.CharField(max_length=20, null=True)
    zr_16 = models.CharField(max_length=20, null=True)
    zr_17 = models.CharField(max_length=20, null=True)
    zr_18 = models.CharField(max_length=20, null=True)
    zr_19 = models.CharField(max_length=20, null=True)
    zr_20 = models.CharField(max_length=20, null=True)

    fa_1 = models.CharField(max_length=1, null=True)
    fa_2 = models.CharField(max_length=1, null=True)
    fa_3 = models.CharField(max_length=1, null=True)
    fa_4 = models.CharField(max_length=1, null=True)
    fa_5 = models.CharField(max_length=1, null=True)
    fa_6 = models.CharField(max_length=1, null=True)
    fa_7 = models.CharField(max_length=1, null=True)
    fa_8 = models.CharField(max_length=1, null=True)
    fa_9 = models.CharField(max_length=1, null=True)
    fa_10 = models.CharField(max_length=1, null=True)
    fa_11 = models.CharField(max_length=1, null=True)
    fa_12 = models.CharField(max_length=1, null=True)
    fa_13 = models.CharField(max_length=1, null=True)
    fa_14 = models.CharField(max_length=1, null=True)
    fa_15 = models.CharField(max_length=1, null=True)
    fa_16 = models.CharField(max_length=1, null=True)
    fa_17 = models.CharField(max_length=1, null=True)
    fa_18 = models.CharField(max_length=1, null=True)
    fa_19 = models.CharField(max_length=1, null=True)
    fa_20 = models.CharField(max_length=1, null=True)

    wu_1 = models.CharField(max_length=1, null=True)
    wu_2 = models.CharField(max_length=1, null=True)
    wu_3 = models.CharField(max_length=1, null=True)
    wu_4 = models.CharField(max_length=1, null=True)
    wu_5 = models.CharField(max_length=1, null=True)
    wu_6 = models.CharField(max_length=1, null=True)
    wu_7 = models.CharField(max_length=1, null=True)
    wu_8 = models.CharField(max_length=1, null=True)
    wu_9 = models.CharField(max_length=1, null=True)
    wu_10 = models.CharField(max_length=1, null=True)
    wu_11 = models.CharField(max_length=1, null=True)
    wu_12 = models.CharField(max_length=1, null=True)
    wu_13 = models.CharField(max_length=1, null=True)
    wu_14 = models.CharField(max_length=1, null=True)
    wu_15 = models.CharField(max_length=1, null=True)
    wu_16 = models.CharField(max_length=1, null=True)
    wu_17 = models.CharField(max_length=1, null=True)
    wu_18 = models.CharField(max_length=1, null=True)
    wu_19 = models.CharField(max_length=1, null=True)
    wu_20 = models.CharField(max_length=1, null=True)

    me_1 = models.CharField(max_length=1, null=True)
    me_2 = models.CharField(max_length=1, null=True)
    me_3 = models.CharField(max_length=1, null=True)
    me_4 = models.CharField(max_length=1, null=True)
    me_5 = models.CharField(max_length=1, null=True)
    me_6 = models.CharField(max_length=1, null=True)
    me_7 = models.CharField(max_length=1, null=True)
    me_8 = models.CharField(max_length=1, null=True)
    me_9 = models.CharField(max_length=1, null=True)
    me_10 = models.CharField(max_length=1, null=True)
    me_11 = models.CharField(max_length=1, null=True)
    me_12 = models.CharField(max_length=1, null=True)
    me_13 = models.CharField(max_length=1, null=True)
    me_14 = models.CharField(max_length=1, null=True)
    me_15 = models.CharField(max_length=1, null=True)
    me_16 = models.CharField(max_length=1, null=True)
    me_17 = models.CharField(max_length=1, null=True)
    me_18 = models.CharField(max_length=1, null=True)
    me_19 = models.CharField(max_length=1, null=True)
    me_20 = models.CharField(max_length=1, null=True)