from django.urls import path
from .views import InvoiceCreateView, InvoiceDetailView

app_name = 'invoice'

urlpatterns = [
    path('', InvoiceCreateView.as_view(), name='invoice_create'),
    path('<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
]
