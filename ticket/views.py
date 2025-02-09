from django.shortcuts import render, redirect
from django.views import View
from .forms import TicketRequestForm
from .models import Ticket
from django.contrib.auth.models import User

class TicketRequestView(View):
    template_name = 'tickets/ticket_request_form.html'

    def get(self, request):
        form = TicketRequestForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TicketRequestForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.requester = request.user
            ticket.save()
            return redirect('ticket_success')
        return render(request, self.template_name, {'form': form})

class TicketListView(View):
    template_name = 'tickets/ticket_list.html'

    def get(self, request):
        tickets = Ticket.objects.filter(assignee=request.user)
        return render(request, self.template_name, {'tickets': tickets})

class TicketCancelView(View):
    template_name = 'tickets/ticket_cancel.html'

    def get(self, request, pk):
        ticket = Ticket.objects.get(pk=pk)
        return render(request, self.template_name, {'ticket': ticket})

    def post(self, request, pk):
        ticket = Ticket.objects.get(pk=pk)
        ticket.is_cancelled = True
        ticket.save()
        return redirect('ticket_list')

def ticket_success(request):
    return render(request, 'tickets/success.html', {'message': 'Ticket request successful'})
