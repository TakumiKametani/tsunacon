from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, ChatMessage, Tag
from .forms import ProjectForm, ChatMessageForm
from django.http import JsonResponse
from utils.helper import update_login_status,with_login_status
from django.utils.decorators import method_decorator


@method_decorator(with_login_status, name='dispatch')
class ProjectListView(View, LoginRequiredMixin):
    template_name = 'dashboard/project_list.html'

    def get(self, request):
        projects = Project.objects.all()
        return render(request, self.template_name, {'projects': projects})


@method_decorator(with_login_status, name='dispatch')
class ProjectDetailView(DetailView, LoginRequiredMixin):
    model = Project
    template_name = 'dashboard/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat_messages'] = ChatMessage.objects.filter(project=self.object, is_draft=False)
        context['chat_form'] = ChatMessageForm()
        return context


@method_decorator(with_login_status, name='dispatch')
class ProjectUpdateView(UpdateView, LoginRequiredMixin):
    model = Project
    form_class = ProjectForm
    template_name = 'dashboard/project_form.html'
    success_url = reverse_lazy('project_list')


@method_decorator(with_login_status, name='dispatch')
class ProjectCreateView(CreateView, LoginRequiredMixin):
    model = Project
    form_class = ProjectForm
    template_name = 'dashboard/project_form.html'
    success_url = reverse_lazy('project_list')


@method_decorator(with_login_status, name='dispatch')
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


@method_decorator(with_login_status, name='dispatch')
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


@method_decorator(with_login_status, name='dispatch')
class ChatMessageDeleteView(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        chat_message = get_object_or_404(ChatMessage, pk=kwargs.get('pk'))
        project_pk = chat_message.project.pk
        chat_message.delete()
        return JsonResponse({'status': 'success', 'message': 'Chat message deleted successfully', 'project_pk': project_pk})


def get_tags(request):
    try:
        category_ids = [int(cid) for cid in request.GET.getlist('categories[]')[0].split(',') if cid.isdigit()]
    except ValueError:
        category_ids = []

    tags = Tag.objects.filter(category__id__in=category_ids).distinct()
    data = [{'id': tag.id, 'name': tag.name, 'price': tag.price} for tag in tags]
    return JsonResponse(data, safe=False)