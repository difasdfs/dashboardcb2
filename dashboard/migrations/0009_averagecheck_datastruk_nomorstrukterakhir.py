# Generated by Django 3.1.4 on 2021-03-31 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_suratperingatan'),
    ]

    operations = [
        migrations.CreateModel(
            name='AverageCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hari', models.DateField()),
                ('awal_hari', models.DateTimeField()),
                ('akhir_hari', models.DateTimeField()),
                ('total_check', models.IntegerField(default=0, null=True)),
                ('total_sales', models.IntegerField(default=0, null=True)),
                ('total_check_online', models.IntegerField(default=0, null=True)),
                ('total_sales_online', models.IntegerField(default=0, null=True)),
                ('average_check', models.FloatField(default=0, null=True)),
                ('average_check_online', models.FloatField(default=0, null=True)),
                ('total_check_antapani', models.IntegerField(default=0, null=True)),
                ('total_check_online_antapani', models.IntegerField(default=0, null=True)),
                ('average_check_antapani', models.FloatField(default=0, null=True)),
                ('average_check_online_antapani', models.FloatField(default=0, null=True)),
                ('total_sales_antapani', models.IntegerField(default=0, null=True)),
                ('total_sales_online_antapani', models.IntegerField(default=0, null=True)),
                ('total_check_metro', models.IntegerField(default=0, null=True)),
                ('total_check_online_metro', models.IntegerField(default=0, null=True)),
                ('average_check_metro', models.FloatField(default=0, null=True)),
                ('average_check_online_metro', models.FloatField(default=0, null=True)),
                ('total_sales_metro', models.IntegerField(default=0, null=True)),
                ('total_sales_online_metro', models.IntegerField(default=0, null=True)),
                ('total_check_jatinangor', models.IntegerField(default=0, null=True)),
                ('total_check_online_jatinangor', models.IntegerField(default=0, null=True)),
                ('average_check_jatinangor', models.FloatField(default=0, null=True)),
                ('average_check_online_jatinangor', models.FloatField(default=0, null=True)),
                ('total_sales_jatinangor', models.IntegerField(default=0, null=True)),
                ('total_sales_online_jatinangor', models.IntegerField(default=0, null=True)),
                ('total_check_sukapura', models.IntegerField(default=0, null=True)),
                ('total_check_online_sukapura', models.IntegerField(default=0, null=True)),
                ('average_check_sukapura', models.FloatField(default=0, null=True)),
                ('average_check_online_sukapura', models.FloatField(default=0, null=True)),
                ('total_sales_sukapura', models.IntegerField(default=0, null=True)),
                ('total_sales_online_sukapura', models.IntegerField(default=0, null=True)),
                ('total_check_sukabirus', models.IntegerField(default=0, null=True)),
                ('total_check_online_sukabirus', models.IntegerField(default=0, null=True)),
                ('average_check_sukabirus', models.FloatField(default=0, null=True)),
                ('average_check_online_sukabirus', models.FloatField(default=0, null=True)),
                ('total_sales_sukabirus', models.IntegerField(default=0, null=True)),
                ('total_sales_online_sukabirus', models.IntegerField(default=0, null=True)),
                ('total_check_unjani', models.IntegerField(default=0, null=True)),
                ('total_check_online_unjani', models.IntegerField(default=0, null=True)),
                ('average_check_unjani', models.FloatField(default=0, null=True)),
                ('average_check_online_unjani', models.FloatField(default=0, null=True)),
                ('total_sales_unjani', models.IntegerField(default=0, null=True)),
                ('total_sales_online_unjani', models.IntegerField(default=0, null=True)),
                ('total_check_cisitu', models.IntegerField(default=0, null=True)),
                ('total_check_online_cisitu', models.IntegerField(default=0, null=True)),
                ('average_check_cisitu', models.FloatField(default=0, null=True)),
                ('average_check_online_cisitu', models.FloatField(default=0, null=True)),
                ('total_sales_cisitu', models.IntegerField(default=0, null=True)),
                ('total_sales_online_cisitu', models.IntegerField(default=0, null=True)),
                ('total_check_sukajadi', models.IntegerField(default=0, null=True)),
                ('total_check_online_sukajadi', models.IntegerField(default=0, null=True)),
                ('average_check_sukajadi', models.FloatField(default=0, null=True)),
                ('average_check_online_sukajadi', models.FloatField(default=0, null=True)),
                ('total_sales_sukajadi', models.IntegerField(default=0, null=True)),
                ('total_sales_online_sukajadi', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DataStruk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomor_struk', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField()),
                ('outlet', models.CharField(max_length=70)),
                ('nama_pembayaran', models.CharField(max_length=70)),
                ('tipe_struk', models.CharField(max_length=70)),
                ('money_amount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NomorStrukTerakhir',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomor_struk', models.CharField(max_length=50)),
            ],
        ),
    ]
