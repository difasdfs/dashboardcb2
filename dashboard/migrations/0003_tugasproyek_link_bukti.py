# Generated by Django 3.1.6 on 2021-03-03 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20210304_0205'),
    ]

    operations = [
        migrations.AddField(
            model_name='tugasproyek',
            name='link_bukti',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
