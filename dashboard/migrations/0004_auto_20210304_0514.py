# Generated by Django 3.1.6 on 2021-03-03 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_tugasproyek_link_bukti'),
    ]

    operations = [
        migrations.AddField(
            model_name='isitugasrutin',
            name='link_bukti',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='isitugasrutin',
            name='selesai_pada',
            field=models.DateTimeField(null=True, verbose_name='Selesai pada'),
        ),
    ]
