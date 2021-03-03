# Generated by Django 3.1.5 on 2021-02-03 06:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, null=True)),
                ('password', models.CharField(max_length=20, null=True)),
                ('link_qrcode', models.CharField(max_length=50, null=True)),
                ('id_loyverse', models.CharField(max_length=100, null=True)),
                ('nama', models.CharField(max_length=50, null=True)),
                ('email', models.CharField(max_length=50, null=True)),
                ('phone_number', models.CharField(max_length=50, null=True)),
                ('address', models.CharField(max_length=50, null=True)),
                ('city', models.CharField(max_length=50, null=True)),
                ('region', models.CharField(max_length=50, null=True)),
                ('postal_code', models.CharField(max_length=10, null=True)),
                ('country_code', models.CharField(max_length=15, null=True)),
                ('customer_code', models.CharField(max_length=15, null=True)),
                ('note', models.CharField(max_length=50, null=True)),
                ('first_visit', models.CharField(max_length=20, null=True)),
                ('last_visit', models.CharField(max_length=20, null=True)),
                ('total_visit', models.CharField(max_length=20, null=True)),
                ('total_spent', models.CharField(max_length=20, null=True)),
                ('total_points', models.CharField(max_length=20, null=True)),
                ('created_at', models.CharField(max_length=20, null=True)),
                ('updated_at', models.CharField(max_length=20, null=True)),
                ('deleted_at', models.CharField(max_length=20, null=True)),
                ('keaktifan', models.BooleanField(null=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
