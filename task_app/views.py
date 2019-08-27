from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
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


class TaskCreateView(CreateView):
    model = Task
    form_class = CreateModelForm
    success_url = reverse_lazy('task_list')


class TaskListView(ListView):

    model = Task
    paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskUpdateView(UpdateView):
    model = Task
    form_class = CreateModelForm
    # template_name_suffix = '_update_form'
    success_url = reverse_lazy('task_list')


def complete_task(request, pk):
    task = Task.objects.get(pk=pk)
    task.done = not task.done
    task.save()
    return redirect('task_list')


class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')
