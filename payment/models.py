from django.db import models
from account.models import Customer, Member, Sales, CustomUser
from dashboard.models import Project
from datetime import date

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', '未確定'),
        ('confirmed', '確定'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('incomplete', '未完了'),
        ('complete', '完了'),
    ]

    user_type = models.CharField(max_length=50)
    user_id = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES)

    def __str__(self):
        return f"{self.user_type} - {self.user_id} - {self.project.name} - {self.amount} - {self.date}"


class SalesPayment(models.Model):
    sales = models.ForeignKey(Sales, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    status = models.CharField(max_length=50, choices=[
        ('pending', '未確定'),
        ('confirmed', '確定'),
    ])
    payment_status = models.CharField(max_length=50, choices=[
        ('incomplete', '未完了'),
        ('complete', '完了'),
    ])

    def __str__(self):
        return f"{self.sales} - {self.project} - {self.amount} - {self.date}"


class CustomerPaymentStatus(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    status = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class MemberSalesPaymentStatus(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    status = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)