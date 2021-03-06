# Generated by Django 3.1.4 on 2021-04-03 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_complaint'),
    ]

    operations = [
        migrations.CreateModel(
            name='MysteryGuest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cabang', models.CharField(choices=[('Antapani', 'Antapani'), ('Cisitu', 'Cisitu'), ('Jatinangor', 'Jatinangor'), ('Metro', 'Metro'), ('Sukapura', 'Sukapura'), ('Sukabirus', 'Sukabirus'), ('Sukajadi', 'Sukajadi'), ('Unjani', 'Unjani')], max_length=100)),
                ('nama', models.CharField(max_length=100)),
                ('tanggal', models.DateField()),
                ('nilai_appearance', models.FloatField()),
                ('komentar_appearance', models.TextField(max_length=1000)),
                ('nilai_aroma', models.FloatField()),
                ('komentar_aroma', models.TextField(max_length=1000)),
                ('nilai_rasa', models.FloatField()),
                ('komentar_rasa', models.TextField(max_length=1000)),
                ('nilai_overall', models.FloatField()),
                ('komentar_overall', models.TextField(max_length=1000)),
                ('dokumentasi_luar', models.CharField(max_length=100)),
                ('dokumentasi_dalam', models.CharField(max_length=100)),
                ('nilai_manajemen', models.FloatField()),
            ],
        ),
    ]
