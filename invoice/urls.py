from django.urls import path
from .views import InvoiceListView, InvoiceCreateView, InvoiceDetailView, registration_success

app_name = 'invoice'

urlpatterns = [
    path('list/', InvoiceListView.as_view(), name='invoice_list'),
    path('create/', InvoiceCreateView.as_view(), name='invoice_create'),
    path('detail/<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('registration_success/', registration_success, name='registration_success'),
]
