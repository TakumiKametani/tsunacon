from django.db import models
from account.models import Customer, CustomUser


class InvoiceManager(models.Manager):
    pass


class Invoice(models.Model):
    client_name = models.CharField(max_length=255)
    client_address = models.TextField()
    issue_date = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    file_path = models.CharField(max_length=500, blank=True, null=True)
    customer = models.ForeignKey(Customer, related_name='invoice_customer', blank=True, null=True, on_delete=models.SET_NULL)
    created = models.ForeignKey(CustomUser, related_name='created', blank=True, null=True, on_delete=models.SET_NULL)
    published = models.BooleanField(verbose_name='顧客様への公開フラグ', default=False)

    objects = InvoiceManager()

    def __str__(self):
        return f"Invoice {self.id} - {self.client_name}"
