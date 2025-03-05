from django.urls import path
from .views import DepartmentCreateView, ContactPersonCreateView, department_success, contact_person_success, ProjectCreateView, project_success

app_name = 'department'

urlpatterns = [
    path('department/create/', DepartmentCreateView.as_view(), name='department_create'),
    path('contact_person/create/', ContactPersonCreateView.as_view(), name='contact_person_create'),
    path('department/success/', department_success, name='department_success'),
    path('contact_person/success/', contact_person_success, name='contact_person_success'),
    path('project/create/', ProjectCreateView.as_view(), name='project_create'),
    path('project/success/', project_success, name='project_success'),
]
