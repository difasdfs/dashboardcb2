# Generated by Django 3.1.4 on 2021-07-02 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KategoriLoyverse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_loyverse', models.CharField(max_length=80)),
                ('nama_kategori', models.CharField(max_length=80)),
            ],
        ),
    ]
