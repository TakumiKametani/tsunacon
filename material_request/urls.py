from django.urls import path
from .views import MaterialRequestView, material_request_success

app_name = 'material_request'

urlpatterns = [
    path('request/', MaterialRequestView.as_view(), name='request'),
    path('request/success/', material_request_success, name='request_success'),
]
