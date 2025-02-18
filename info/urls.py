from django.urls import path
from .views import InformationView, QuestionAnswerView, CustomerVoiceView, PriceView, CharacteristicView, ContactView

app_name = 'info'

urlpatterns = [
    path('information/', InformationView.as_view(), name='information'),
    path('question_answer/', QuestionAnswerView.as_view(), name='question_answer'),
    path('customer_voice/', CustomerVoiceView.as_view(), name='customer_voice'),
    path('price/', PriceView.as_view(), name='price'),
    path('characteristic/', CharacteristicView.as_view(), name='characteristic'),
    path('contact/', ContactView.as_view(), name='contact'),
]
