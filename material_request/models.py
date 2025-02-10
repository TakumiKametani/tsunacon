from django.db import models
from account.models import Customer

class MaterialRequest(models.Model):
    """資料請求で入力していただいた値は、真実かどうかが不明なので、こちらでも情報を保持しておく"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    first_name_kana = models.CharField(max_length=255)
    last_name_kana = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=10)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
