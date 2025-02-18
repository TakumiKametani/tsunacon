from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class InformationView(TemplateView):
    template_name = "info/information.html"


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

