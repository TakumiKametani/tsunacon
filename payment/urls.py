from django.urls import path
from .views import PaymentListView, PaymentDetailView, SalesPaymentListView, SalesPaymentDetailView, CustomerPaymentStatusCreateView, MemberSalesPaymentStatusCreateView, customer_payment_status_success, member_sales_payment_status_success

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('payments/<int:year>/<int:month>/', PaymentDetailView.as_view(), name='payment_detail'),
    path('sales_payments/', SalesPaymentListView.as_view(), name='sales_payment_list'),
    path('sales_payments/<int:project_id>/', SalesPaymentDetailView.as_view(), name='sales_payment_detail'),
    #
    path('customer_payment_status/create/', CustomerPaymentStatusCreateView.as_view(),
         name='customer_payment_status_create'),
    path('member_sales_payment_status/create/', MemberSalesPaymentStatusCreateView.as_view(),
         name='member_sales_payment_status_create'),
    path('customer_payment_status/success/', customer_payment_status_success, name='customer_payment_status_success'),
    path('member_sales_payment_status/success/', member_sales_payment_status_success,
         name='member_sales_payment_status_success'),
]
