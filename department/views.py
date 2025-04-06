from django.shortcuts import render, redirect
from django.views import View
from .forms import DepartmentForm, ContactPersonForm
from account.models import Customer
from .models import Department
from django.core.mail import send_mail

from dashboard.forms import ProjectForm
from dashboard.models import Project
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from utils.helper import update_login_status, with_login_status


@method_decorator(with_login_status, name='dispatch')
class DepartmentCreateView(View, LoginRequiredMixin):
    template_name = 'departments/department_form.html'

    def get(self, request):
        form = DepartmentForm()
        customers = Customer.objects.filter(customer_type__in=['company', 'organization', 'group'])
        return render(request, self.template_name, {'form': form, 'customers': customers})

    def post(self, request):
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_success')
        customers = Customer.objects.filter(customer_type__in=['company', 'organization', 'group'])
        return render(request, self.template_name, {'form': form, 'customers': customers})


@method_decorator(with_login_status, name='dispatch')
class ContactPersonCreateView(View, LoginRequiredMixin):
    template_name = 'departments/contact_person_form.html'

    def get(self, request):
        form = ContactPersonForm()
        departments = Department.objects.all()
        return render(request, self.template_name, {'form': form, 'departments': departments})

    def post(self, request):
        form = ContactPersonForm(request.POST)
        if form.is_valid():
            contact_person = form.save()
            send_mail(
                'New Contact Person Registered',
                'A new contact person has been registered.',
                'from@example.com',
                [contact_person.email],
                fail_silently=False,
            )
            return redirect('contact_person_success')
        departments = Department.objects.all()
        return render(request, self.template_name, {'form': form, 'departments': departments})

def department_success(request):
    return render(request, 'departments/success.html', {'message': 'Department created successfully'})

def contact_person_success(request):
    return render(request, 'departments/success.html', {'message': 'Contact person created successfully'})


@method_decorator(with_login_status, name='dispatch')
class ProjectCreateView(View, LoginRequiredMixin):
    template_name = 'departments/project_form.html'

    def get(self, request):
        form = ProjectForm(request=request)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProjectForm(request.POST, request=request)
        if form.is_valid():
            project = form.save()
            return redirect('project_success')
        return render(request, self.template_name, {'form': form})


def project_success(request):
    return render(request, 'departments/project_create_success.html', {'message': 'Project created successfully'})

