# Generated by Django 3.1.4 on 2021-07-02 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supply_chain', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CabangLoyverse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_loyverse', models.CharField(max_length=80)),
                ('nama_cabang', models.CharField(max_length=80)),
            ],
        ),
    ]
