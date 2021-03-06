# Generated by Django 3.1.4 on 2021-01-04 08:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DataKaryawan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nik', models.CharField(max_length=4, null=True)),
                ('no_id_fingerprint', models.IntegerField()),
                ('nama', models.CharField(max_length=100)),
                ('area', models.CharField(choices=[('Office', 'Office'), ('Jatinangor', 'Jatinangor'), ('Cisitu', 'Cisitu'), ('Unjani', 'Unjani'), ('Metro', 'Metro'), ('Sukajadi', 'Sukajadi'), ('Telkom Sukabirus', 'Telkom Sukabirus'), ('Telkom Sukapura', 'Telkom Sukapura')], max_length=30)),
                ('level_manajemen', models.CharField(max_length=40)),
                ('nama_posisi', models.CharField(max_length=30)),
                ('kode_posisi', models.CharField(max_length=5)),
                ('status_jabatan', models.CharField(max_length=40, null=True)),
                ('jabatan_baru', models.CharField(max_length=40, null=True)),
                ('status_pegawai', models.CharField(max_length=50, null=True)),
                ('tanggal_masuk', models.DateField(null=True, verbose_name='Tanggal Masuk')),
                ('lama_bekerja', models.CharField(max_length=100, null=True)),
                ('no_ktp', models.CharField(max_length=30, null=True)),
                ('tempat_lahir', models.CharField(max_length=40, null=True)),
                ('umur', models.IntegerField(null=True)),
                ('tanggal_lahir', models.DateField(null=True, verbose_name='Tanggal Lahir')),
                ('jenis_kelamin', models.CharField(choices=[('L', 'L'), ('P', 'P')], max_length=1)),
                ('agama', models.CharField(max_length=20, null=True)),
                ('pendidikan', models.CharField(choices=[('SD', 'SD'), ('SMP', 'SMP'), ('SMA/SMK', 'SMA/SMK'), ('D3', 'D3'), ('S1', 'S1'), ('S2', 'S2'), ('S3', 'S3')], max_length=10)),
                ('jurusan', models.CharField(max_length=40, null=True)),
                ('alamat', models.CharField(max_length=100, null=True)),
                ('no_hp', models.CharField(max_length=20)),
                ('marital_status', models.CharField(choices=[('BELUM MENIKAH', 'BELUM MENIKAH'), ('MENIKAH', 'MENIKAH'), ('CERAI', 'CERAI')], max_length=20)),
                ('anak', models.IntegerField()),
                ('no_rekening', models.CharField(max_length=100, null=True)),
                ('bpjs_ketenagakerjaan', models.CharField(max_length=100, null=True)),
                ('nama_darurat', models.CharField(max_length=100, null=True)),
                ('alamat_darurat', models.CharField(max_length=100, null=True)),
                ('hubungan_darurat', models.CharField(max_length=100, null=True)),
                ('no_hp_darurat', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(choices=[('AKTIF', 'AKTIF'), ('KELUAR', 'KELUAR')], max_length=100, null=True)),
                ('tanggal_keluar', models.DateField(null=True, verbose_name='Tanggal Keluar')),
                ('alasan_keluar', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TugasRutin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=150)),
                ('isi', models.CharField(max_length=1000)),
                ('bagian', models.CharField(max_length=150, null=True)),
                ('pemilik_tugas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TugasProyek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=150)),
                ('isi', models.CharField(max_length=1000)),
                ('deadline', models.DateTimeField(verbose_name='Deadline')),
                ('status', models.CharField(choices=[('Tuntas', 'Tuntas'), ('Hold', 'Hold'), ('On Progress', 'On Progress'), ('Selesai', 'Selesai'), ('Deadline', 'Deadline')], max_length=15)),
                ('bukti', models.CharField(max_length=100, null=True)),
                ('penilaian', models.IntegerField(null=True)),
                ('bagian', models.CharField(max_length=100, null=True)),
                ('komentar', models.CharField(max_length=1000)),
                ('pemilik_tugas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IsiTugasRutin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deadline', models.DateTimeField(verbose_name='Deadline')),
                ('status', models.CharField(choices=[('Tuntas', 'Tuntas'), ('Hold', 'Hold'), ('On Progress', 'On Progress'), ('Selesai', 'Selesai'), ('Deadline', 'Deadline')], max_length=15)),
                ('bukti', models.CharField(max_length=100, null=True)),
                ('penilaian', models.IntegerField(null=True)),
                ('komentar', models.CharField(max_length=1000)),
                ('judul', models.CharField(max_length=150, null=True)),
                ('isi', models.CharField(max_length=1000, null=True)),
                ('tugas_rutin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.tugasrutin')),
            ],
        ),
    ]
