from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Member(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=20, null=True)
    link_qrcode = models.CharField(max_length=50, null=True)
    id_loyverse = models.CharField(max_length=100, null=True)
    nama = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    region = models.CharField(max_length=50, null=True)
    postal_code = models.CharField(max_length=10, null=True)
    country_code = models.CharField(max_length=15, null=True)
    customer_code = models.CharField(max_length=15, null=True)
    note = models.CharField(max_length=50, null=True)
    first_visit = models.CharField(max_length=20, null=True)
    last_visit = models.CharField(max_length=20, null=True)
    total_visit = models.CharField(max_length=20, null=True)
    total_spent = models.CharField(max_length=20, null=True)
    total_points = models.CharField(max_length=20, null=True)
    created_at = models.CharField(max_length=20, null=True)
    updated_at = models.CharField(max_length=20, null=True)
    deleted_at = models.CharField(max_length=20, null=True)
    keaktifan = models.BooleanField(null=True)