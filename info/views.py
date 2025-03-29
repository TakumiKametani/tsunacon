from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from account.models import LoginStatus
from .models import Announcement, UserAnnouncement
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect

from utils.helper import update_login_status, with_login_status, get_login_status_cache
from django.utils.decorators import method_decorator


class AnnouncementListView(generic.ListView):
    model = Announcement
    template_name = 'info/announcement_list.html'
    context_object_name = 'announcements'

    def get_queryset(self):
        user = self.request.user
        audience = ['all']
        read_announcements = UserAnnouncement.objects.none()
        if not self.request.user.is_authenticated:
            # 未ログインユーザー
            announcements = Announcement.objects.filter(is_active=True,
                                                        target_audience__in=audience).order_by('-created')
        else:
            audience += ['membership']
            login_status = get_login_status_cache(user=user)
            read_announcements = UserAnnouncement.objects.filter(user=user).values_list('announcement', flat=True)
            if login_status.is_customer:
                # 顧客向けのフィルタリング
                audience += ['customer']
                announcements = Announcement.objects.filter(is_active=True, target_audience__in=audience).order_by(
                    '-created')
            elif login_status.is_member:
                # つな会員向けのフィルタリング
                audience += ['member']
                announcements = Announcement.objects.filter(is_active=True, target_audience__in=audience).order_by(
                    '-created')
            elif login_status.is_employee:
                # 社員向けのフィルタリング
                audience += ['employee']
                announcements = Announcement.objects.filter(is_active=True, target_audience__in=audience).order_by(
                    '-created')
            else:
                announcements = Announcement.objects.none()

        return announcements, read_announcements

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _, read_announcements = self.get_queryset()
        context['read_announcements'] = read_announcements
        return context


class AnnouncementDetailView(generic.DetailView):
    model = Announcement
    template_name = 'info/announcement_detail.html'
    context_object_name = 'announcement'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_announcement, created = UserAnnouncement.objects.get_or_create(user=request.user, announcement=self.object)
        if not user_announcement.is_read:
            user_announcement.is_read = True
            user_announcement.read_at = timezone.now()
            user_announcement.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class QuestionAnswerView(TemplateView):
    template_name = "info/question_answer.html"


class CustomerVoiceView(TemplateView):
    template_name = "info/customer_voice.html"


class PriceView(TemplateView):
    template_name = "info/price.html"


class CharacteristicView(TemplateView):
    template_name = "info/characteristic.html"


class ContactView(TemplateView):
    template_name = "info/contact.html"

