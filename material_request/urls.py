from django.urls import path
from .views import MaterialRequestView, material_request_success

urlpatterns = [
    path('request/', MaterialRequestView.as_view(), name='material_request'),
    path('request/success/', material_request_success, name='material_request_success'),
]
