from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django import forms
from django.utils import timezone
from django.urls import reverse_lazy
from captcha.fields import CaptchaField
from .models import Task
from django.shortcuts import redirect


class CreateModelForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateView(CreateView):
    model = Task
    form_class = CreateModelForm
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
    form_class = CreateModelForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('task_list')


def complete_task(request, pk):
    task = Task.objects.get(pk=pk)
    task.done = True if not task.done else False
    task.save()
    return redirect('task_list')
