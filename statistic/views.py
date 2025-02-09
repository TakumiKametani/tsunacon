from django.views.generic import ListView
from dashboard.models import Project
from django.db.models import Min, Max

class ProjectStatisticsView(ListView):
    model = Project
    template_name = 'statistics/statistics.html'
    context_object_name = 'projects'

    def get_queryset(self):
        projects = Project.objects.all()
        client_id = self.request.GET.get('client_id')
        client_name = self.request.GET.get('client_name')
        min_amount = self.request.GET.get('min_amount')
        max_amount = self.request.GET.get('max_amount')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        sort_by = self.request.GET.get('sort_by', 'name')

        if client_id:
            projects = projects.filter(client_id=client_id)
        if client_name:
            projects = projects.filter(client_name__icontains=client_name)
        if min_amount:
            projects = projects.filter(amount__gte=min_amount)
        if max_amount:
            projects = projects.filter(amount__lte=max_amount)
        if start_date:
            projects = projects.filter(start_date__gte=start_date)
        if end_date:
            projects = projects.filter(end_date__lte=end_date)

        projects = projects.order_by(sort_by)
        return projects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = self.get_queryset()
        context['min_amount_overall'] = projects.aggregate(Min('amount'))['amount__min']
        context['max_amount_overall'] = projects.aggregate(Max('amount'))['amount__max']
        context['client_id'] = self.request.GET.get('client_id')
        context['client_name'] = self.request.GET.get('client_name')
        context['min_amount'] = self.request.GET.get('min_amount')
        context['max_amount'] = self.request.GET.get('max_amount')
        context['start_date'] = self.request.GET.get('start_date')
        context['end_date'] = self.request.GET.get('end_date')
        context['sort_by'] = self.request.GET.get('sort_by', 'name')
        return context
