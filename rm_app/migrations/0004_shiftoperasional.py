# Generated by Django 3.1.4 on 2021-06-25 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rm_app', '0003_absenkaryawan_absentanggal'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShiftOperasional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode', models.CharField(max_length=10)),
                ('deskripsi', models.CharField(max_length=70)),
                ('warna', models.CharField(max_length=12, null=True)),
                ('cabang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rm_app.cabang')),
            ],
        ),
    ]
