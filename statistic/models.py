from django.db import models
from dashboard.models import Project

class Statistics(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    min_amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
