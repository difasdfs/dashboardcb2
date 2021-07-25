from django.db import models

# from home_dashboard.models import DataStruk
# obj= DataStruk.objects.all().order_by('-id')[0]
# 71750

# Create your models here.
class DataStruk(models.Model):
    receipt_number = models.CharField(max_length=100)
    receipt_type = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    receipt_date = models.DateTimeField()
    total_money = models.IntegerField()
    total_tax = models.IntegerField()
    store_id = models.CharField(max_length=170)
    dining_option = models.CharField(max_length=100)
    payments = models.CharField(max_length=100)

    def __str__(self):
        return self.receipt_number

    def total_money_filter(self):
        
        payments = self.payments
        total_money = self.total_money
        total_tax = self.total_tax

        if "GO FOOD" in payments:
            total_money_filter = total_money * 0.8
        elif "Kredit Bank Lain" in payments:
            total_money_filter = total_money * 0.982
        elif "Debit Bank Lain" in payments:
            total_money_filter = total_money * 0.985
        elif "Kredit BRI" in payments:
            total_money_filter = total_money * 0.99
        elif "Debit BRI" in payments:
            total_money_filter = total_money * 0.9985
        elif "QR BRI" in payments:
            total_money_filter = total_money * 0.997
        elif "SHOPEE FOOD" in payments:
            total_money_filter = total_money * 0.668
        elif "BCA" in payments:
            total_money_filter = total_money * 0.997
        elif "GRAB FOOD" in payments:
            total_money_filter = total_money * 0.8
        elif "SHOPEE PAY" in payments:
            total_money_filter = total_money * 0.997
        elif "OVO" in payments:
            total_money_filter = total_money * 0.997
        elif "GOPAY" in payments:
            total_money_filter = total_money * 0.997
        elif "Cash" in payments:
            total_money_filter = total_money - total_tax
        else:
            total_money_filter = total_money

        return total_money_filter