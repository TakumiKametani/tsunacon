from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, ChatMessage, Grade
from .forms import ProjectForm, ChatMessageForm
from django.http import JsonResponse

# class ProjectListView(View, LoginRequiredMixin):
class ProjectListView(View):
    template_name = 'dashboard/project_list.html'

    def get(self, request):
        projects = Project.objects.all()
        return render(request, self.template_name, {'projects': projects})

# class ProjectDetailView(DetailView, LoginRequiredMixin):
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'dashboard/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat_messages'] = ChatMessage.objects.filter(project=self.object, is_draft=False)
        context['chat_form'] = ChatMessageForm()
        return context


class ProjectUpdateView(UpdateView, LoginRequiredMixin):
    model = Project
    form_class = ProjectForm
    template_name = 'dashboard/project_form.html'
    success_url = reverse_lazy('project_list')


class ProjectCreateView(CreateView, LoginRequiredMixin):
    model = Project
    form_class = ProjectForm
    template_name = 'dashboard/project_form.html'
    success_url = reverse_lazy('project_list')


class ChatMessageCreateView(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.user = request.user
            chat_message.project = get_object_or_404(Project, pk=request.POST.get('project_id'))
            chat_message.is_draft = 'save_draft' in request.POST
            chat_message.save()
            return JsonResponse({'status': 'success', 'message': 'Chat message created successfully'})
        return JsonResponse({'status': 'error', 'errors': form.errors})

class ChatMessageUpdateView(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        chat_message = get_object_or_404(ChatMessage, pk=kwargs.get('pk'))
        form = ChatMessageForm(request.POST, instance=chat_message)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.is_draft = 'save_draft' in request.POST
            chat_message.save()
            return JsonResponse({'status': 'success', 'message': 'Chat message updated successfully'})
        return JsonResponse({'status': 'error', 'errors': form.errors})

class ChatMessageDeleteView(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        chat_message = get_object_or_404(ChatMessage, pk=kwargs.get('pk'))
        project_pk = chat_message.project.pk
        chat_message.delete()
        return JsonResponse({'status': 'success', 'message': 'Chat message deleted successfully', 'project_pk': project_pk})


def get_grade_price(request):
    grade_id = request.GET.get('grade_id')
    if grade_id:
        grade = get_object_or_404(Grade, id=grade_id)
        return JsonResponse({'price': str(grade.price)})
    return JsonResponse({'price': ''})