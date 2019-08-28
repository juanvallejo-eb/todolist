from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth import LoginView

from django import forms
from django.urls import reverse_lazy
from captcha.fields import CaptchaField
from .models import Task
from django.shortcuts import redirect


class CreateModelForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = CreateModelForm
    success_url = reverse_lazy('task_list')


class TaskListView(LoginRequiredMixin, ListView):

    model = Task
    paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = CreateModelForm
    # template_name_suffix = '_update_form'
    success_url = reverse_lazy('task_list')


def complete_task(request, pk):
    task = Task.objects.get(pk=pk)
    task.done = not task.done
    task.save()
    return redirect('task_list')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')
