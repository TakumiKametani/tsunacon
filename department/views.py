from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from .forms import DepartmentForm, ContactPersonForm
from account.models import Customer
from .models import Department, Person
from django.core.mail import send_mail

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from utils.helper import update_login_status, with_login_status



@method_decorator(with_login_status, name='dispatch')
class DepartmentListView(View, LoginRequiredMixin):
    template_name = 'department/department_list.html'

    def get(self, request):
        # TODO queryを記載する
        departments = ''
        return render(request, self.template_name, {'departments': departments})


@method_decorator(with_login_status, name='dispatch')
class DepartmentCreateView(View, LoginRequiredMixin):
    template_name = 'department/department_form.html'

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
class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'department/department_detail.html'


@method_decorator(with_login_status, name='dispatch')
class ContactPersonListView(View, LoginRequiredMixin):
    template_name = 'department/contact_person_list.html'

    def get(self, request):
        # TODO queryを記載する
        contact_persons = ''
        return render(request, self.template_name, {'contact_persons': contact_persons})


@method_decorator(with_login_status, name='dispatch')
class ContactPersonCreateView(View, LoginRequiredMixin):
    template_name = 'department/contact_person_form.html'

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


@method_decorator(with_login_status, name='dispatch')
class ContactPersonDetailView(DetailView):
    model = Person
    template_name = 'department/contact_person_detail.html'


def department_success(request):
    return render(request, 'department/success.html', {'message': 'Department created successfully'})

def contact_person_success(request):
    return render(request, 'department/success.html', {'message': 'Contact person created successfully'})

