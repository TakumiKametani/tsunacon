from django.shortcuts import render, redirect
from django.views import View
from .forms import MaterialRequestForm

class MaterialRequestView(View):
    template_name = 'material_request/material_request_form.html'

    def get(self, request):
        form = MaterialRequestForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = MaterialRequestForm(request.POST)
        if form.is_valid():
            material_request = form.save()
            return redirect('material_request_success')
        return render(request, self.template_name, {'form': form})

def material_request_success(request):
    return render(request, 'material_request/material_request_success.html')
