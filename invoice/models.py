from django.db import models

class Invoice(models.Model):
    client_name = models.CharField(max_length=255)
    client_address = models.TextField()
    issue_date = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice {self.id} - {self.client_name}"
