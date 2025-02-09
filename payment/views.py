from django.shortcuts import render, redirect
from django.views import View
from .forms import PaymentForm, CustomerPaymentStatusForm, MemberSalesPaymentStatusForm
from .models import Payment, SalesPayment
from django.db.models import Sum
from ticket.models import TicketTransaction

class PaymentListView(View):
    template_name = 'payments/payment_list.html'

    def get(self, request):
        user_id = request.user.id
        user_type = 'member' if hasattr(request.user, 'member') else 'sales'
        payments = Payment.objects.filter(user_id=user_id, user_type=user_type).order_by('-date')
        monthly_totals = payments.values('date__year', 'date__month').annotate(total_amount=Sum('amount')).order_by(
            'date__year', 'date__month')

        received_tickets = TicketTransaction.objects.filter(ticket__assignee=request.user).values(
            'transaction_date__year', 'transaction_date__month').annotate(total_amount=Sum('amount')).order_by(
            'transaction_date__year', 'transaction_date__month')

        given_tickets = TicketTransaction.objects.filter(ticket__requester=request.user).values(
            'transaction_date__year', 'transaction_date__month').annotate(total_amount=Sum('amount')).order_by(
            'transaction_date__year', 'transaction_date__month')

        combined_totals = []
        for month in monthly_totals:
            total_amount = month['total_amount']
            received = next((t for t in received_tickets if
                             t['transaction_date__year'] == month['date__year'] and t['transaction_date__month'] ==
                             month['date__month']), None)
            given = next((t for t in given_tickets if
                          t['transaction_date__year'] == month['date__year'] and t['transaction_date__month'] == month[
                              'date__month']), None)
            received_amount = received['total_amount'] if received else 0
            given_amount = given['total_amount'] if given else 0
            combined_totals.append({
                'year': month['date__year'],
                'month': month['date__month'],
                'payment_total': total_amount,
                'received_total': received_amount,
                'given_total': given_amount,
                'combined_total': total_amount + received_amount - given_amount
            })

        return render(request, self.template_name, {
            'payments': payments,
            'combined_totals': combined_totals,
            'monthly_totals': monthly_totals,
            'received_tickets': received_tickets,
            'given_tickets': given_tickets,
        })



class PaymentDetailView(View):
    template_name = 'payments/payment_detail.html'

    def get(self, request, year, month):
        user_id = request.user.id
        user_type = 'member' if hasattr(request.user, 'member') else 'sales'
        payments = Payment.objects.filter(user_id=user_id, user_type=user_type, date__year=year, date__month=month)
        received_tickets = TicketTransaction.objects.filter(ticket__assignee=request.user, transaction_date__year=year, transaction_date__month=month)
        given_tickets = TicketTransaction.objects.filter(ticket__requester=request.user, transaction_date__year=year, transaction_date__month=month)
        return render(request, self.template_name, {'payments': payments, 'received_tickets': received_tickets, 'given_tickets': given_tickets})


class SalesPaymentListView(View):
    template_name = 'payments/sales_payment_list.html'

    def get(self, request):
        sales_id = request.user.id
        payments = SalesPayment.objects.filter(sales_id=sales_id).order_by('-date')
        monthly_totals = payments.values('date__year', 'date__month').annotate(total_amount=Sum('amount')).order_by(
            'date__year', 'date__month')

        return render(request, self.template_name, {'payments': payments, 'monthly_totals': monthly_totals})


class SalesPaymentDetailView(View):
    template_name = 'payments/sales_payment_detail.html'

    def get(self, request, project_id):
        payments = SalesPayment.objects.filter(project_id=project_id)
        return render(request, self.template_name, {'payments': payments})


class CustomerPaymentStatusCreateView(View):
    template_name = 'accounts/customer_payment_status_form.html'

    def get(self, request):
        form = CustomerPaymentStatusForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomerPaymentStatusForm(request.POST)
        if form.is_valid():
            payment_status = form.save(commit=False)
            payment_status.save()
            return redirect('customer_payment_status_success')
        return render(request, self.template_name, {'form': form})

class MemberSalesPaymentStatusCreateView(View):
    template_name = 'accounts/member_sales_payment_status_form.html'

    def get(self, request):
        form = MemberSalesPaymentStatusForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = MemberSalesPaymentStatusForm(request.POST)
        if form.is_valid():
            payment_status = form.save(commit=False)
            payment_status.save()
            return redirect('member_sales_payment_status_success')
        return render(request, self.template_name, {'form': form})

def customer_payment_status_success(request):
    return render(request, 'accounts/customer_payment_status_success.html')

def member_sales_payment_status_success(request):
    return render(request, 'accounts/member_sales_payment_status_success.html')