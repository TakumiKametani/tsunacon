from django.urls import path
from .views import TicketRequestView, TicketListView, TicketCancelView, ticket_success

urlpatterns = [
    path('request/', TicketRequestView.as_view(), name='ticket_request'),
    path('list/', TicketListView.as_view(), name='ticket_list'),
    path('cancel/<int:pk>/', TicketCancelView.as_view(), name='ticket_cancel'),
    path('success/', ticket_success, name='ticket_success'),
]
