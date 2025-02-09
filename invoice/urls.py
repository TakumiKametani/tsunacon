from django.urls import path
from .views import InvoiceCreateView, InvoiceDetailView

urlpatterns = [
    path('', InvoiceCreateView.as_view(), name='invoice_create'),
    path('<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
]
