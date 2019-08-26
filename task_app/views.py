from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.utils import timezone
from django.urls import reverse_lazy
from .models import Task


class TaskCreateView(CreateView):
    model = Task
    fields = ['name', 'done', 'priority', 'user']
    success_url = reverse_lazy('task_list')


class TaskListView(ListView):

    model = Task
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class TaskUpdateView(UpdateView):
    model = Task
    fields = ['name', 'done', 'priority']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('task_list')
