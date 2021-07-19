from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(PurchaseOrder)
admin.site.register(BarangPurchaseOrder)
admin.site.register(StatusPurchaseOrder)
admin.site.register(BarangDiterima)