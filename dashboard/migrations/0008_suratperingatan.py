# Generated by Django 3.1.4 on 2021-03-26 19:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0007_auto_20210311_0546'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuratPeringatan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mulai_sp', models.DateField()),
                ('berakhir_sp', models.DateField()),
                ('keaktifan', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
