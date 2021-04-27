# Generated by Django 3.1.4 on 2021-04-27 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_jawabanist_pesertatest_tokentest'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssemblyProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=30)),
                ('ayam', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TanggalWeekendWeekdays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal', models.DateField()),
                ('weekend', models.BooleanField(default=False)),
            ],
        ),
    ]
