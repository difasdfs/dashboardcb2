# Generated by Django 3.1.6 on 2021-03-03 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tugasproyek',
            name='selesai_pada',
            field=models.DateTimeField(null=True, verbose_name='Selesai pada'),
        ),
        migrations.AlterField(
            model_name='datakaryawan',
            name='area',
            field=models.CharField(choices=[('Office', 'Office'), ('Antapani', 'Antapani'), ('Jatinangor', 'Jatinangor'), ('Cisitu', 'Cisitu'), ('Unjani', 'Unjani'), ('Metro', 'Metro'), ('Sukajadi', 'Sukajadi'), ('Telkom Sukabirus', 'Telkom Sukabirus'), ('Telkom Sukapura', 'Telkom Sukapura'), ('Kopo', 'Kopo')], max_length=30),
        ),
        migrations.AlterField(
            model_name='tugasproyek',
            name='status',
            field=models.CharField(choices=[('Tuntas', 'Tuntas'), ('Hold', 'Hold'), ('On Progress', 'On Progress'), ('Selesai', 'Selesai'), ('Deadline', 'Deadline'), ('Terlambat', 'Terlambat')], max_length=15),
        ),
    ]
