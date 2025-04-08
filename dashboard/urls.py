from django.urls import path
from .views import (
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ChatMessageCreateView,
    ChatMessageUpdateView,
    ChatMessageDeleteView,
    get_tags
)

app_name = 'dashboard'

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('project/create/', ProjectCreateView.as_view(), name='project_create'),
    path('chat_message/create/', ChatMessageCreateView.as_view(), name='chat_message_create'),
    path('chat_message/update/<int:pk>/', ChatMessageUpdateView.as_view(), name='chat_message_update'),
    path('chat_message/delete/<int:pk>/', ChatMessageDeleteView.as_view(), name='chat_message_delete'),
    path('get_tags/', get_tags, name='get_tags'),
]
