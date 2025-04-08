from django.urls import path
from .views import DepartmentListView, DepartmentCreateView, DepartmentDetailView, ContactPersonListView, ContactPersonCreateView, ContactPersonDetailView, department_success, contact_person_success

app_name = 'department'

urlpatterns = [
    path('', DepartmentListView.as_view(), name='department_list'),
    path('create/', DepartmentCreateView.as_view(), name='department_create'),
    path('detail/<int:pk>/', DepartmentDetailView.as_view(), name='department_detail'),
    path('contact_person/', ContactPersonListView.as_view(), name='contact_person_list'),
    path('contact_person/create/', ContactPersonCreateView.as_view(), name='contact_person_create'),
    path('contact_person/detail/<int:pk>/', ContactPersonDetailView.as_view(), name='contact_person_detail'),
    path('success/', department_success, name='department_success'),
    path('contact_person/success/', contact_person_success, name='contact_person_success'),
]
