from django.urls import path
from .views import ProjectStatisticsView

urlpatterns = [
    path('statistics/', ProjectStatisticsView.as_view(), name='project_statistics'),
]
