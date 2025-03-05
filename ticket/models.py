from django.db import models
from account.models import CustomUser
from dashboard.models import Project

class Ticket(models.Model):
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='requested_user')
    assignee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_user')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    num_tickets = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.requester} -> {self.assignee} | {self.project} | Tickets: {self.num_tickets}"

class TicketTransaction(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
