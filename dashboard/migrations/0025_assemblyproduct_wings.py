# Generated by Django 3.1.4 on 2021-06-26 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0024_kaizentimoutlet'),
    ]

    operations = [
        migrations.AddField(
            model_name='assemblyproduct',
            name='wings',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
