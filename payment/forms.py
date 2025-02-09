from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['user_type', 'user_id', 'project', 'amount', 'date', 'status', 'payment_status']


from .models import CustomerPaymentStatus, MemberSalesPaymentStatus

class CustomerPaymentStatusForm(forms.ModelForm):
    class Meta:
        model = CustomerPaymentStatus
        fields = ['customer', 'date', 'status', 'amount']

class MemberSalesPaymentStatusForm(forms.ModelForm):
    class Meta:
        model = MemberSalesPaymentStatus
        fields = ['user', 'date', 'status', 'amount']