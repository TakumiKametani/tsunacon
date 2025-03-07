from django.urls import path
from .views import AnnouncementListView, AnnouncementDetailView, QuestionAnswerView, CustomerVoiceView, PriceView, CharacteristicView, ContactView

app_name = 'info'

urlpatterns = [
    path('announcements/', AnnouncementListView.as_view(), name='announcement_list'),
    path('announcements/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement_detail'),
    path('question_answer/', QuestionAnswerView.as_view(), name='question_answer'),
    path('customer_voice/', CustomerVoiceView.as_view(), name='customer_voice'),
    path('price/', PriceView.as_view(), name='price'),
    path('characteristic/', CharacteristicView.as_view(), name='characteristic'),
    path('contact/', ContactView.as_view(), name='contact'),
]
