# Generated by Django 3.1.4 on 2021-06-18 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IdCabangMetro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_cabang', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal', models.DateField(verbose_name='tanggal')),
                ('total_sales', models.IntegerField(default=0)),
                ('total_struk', models.IntegerField(default=0)),
                ('omset', models.IntegerField(default=0)),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Struk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomor_struk', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(verbose_name='created at')),
                ('total_money', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='StrukTerakhir',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomor_struk', models.CharField(max_length=20)),
            ],
        ),
    ]
