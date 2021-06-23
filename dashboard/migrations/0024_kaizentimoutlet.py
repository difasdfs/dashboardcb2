# Generated by Django 3.1.4 on 2021-06-19 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0023_auto_20210607_1541'),
    ]

    operations = [
        migrations.CreateModel(
            name='KaizenTimOutlet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solusi_sekarang', models.TextField()),
                ('kronologis_kejadian', models.TextField()),
                ('analisis_akar_masalah', models.TextField()),
                ('action_plan_kaizen', models.TextField()),
                ('complaint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.complaint')),
            ],
        ),
    ]
