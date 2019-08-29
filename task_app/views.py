import requests
# import json
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
# from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin

from django import forms
from django.urls import reverse_lazy
from captcha.fields import CaptchaField
from .models import Task
from django.shortcuts import redirect


class CreateTaskForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Task
        exclude = ('user', 'event_id')


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = CreateTaskForm

    def get_success_url(self):
        return reverse_lazy(
            'task_list',
            kwargs={'pk': self.kwargs['pk']}
        )

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.event_id = self.kwargs['pk']
        self.object = form.save()
        return super().form_valid(form)


class TaskListView(LoginRequiredMixin, PaginationMixin, ListView):

    paginate_by = 6
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_id'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, event_id=self.kwargs['pk'])


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = CreateTaskForm

    def get_success_url(self):
        return reverse_lazy(
            'task_list',
            kwargs={'pk': self.kwargs['pk_event']}
        )


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_id'] = self.kwargs['pk_event']
        return context

    def get_success_url(self):
        return reverse_lazy(
            'task_list',
            kwargs={'pk': self.kwargs['pk_event']}
        )


def complete_task(request, pk_event, pk):
    task = Task.objects.get(pk=pk)
    task.done = not task.done
    task.save()
    success_url = reverse_lazy(
        'task_list',
        kwargs={'pk': pk_event}
    )
    return redirect(success_url)


def get_user_events(user, page, page_size):
    token = user.access_token
    url = 'https://www.eventbriteapi.com/v3/users/me/events/'
    page = 1
    headers = {
        'Authorization': 'Bearer '+token
    }
    params = {
        'page': page,
        'page_size': page_size
    }
    response = requests.get(url, headers=headers, params=params).json()['events']
    return response


class EventsView(PaginationMixin, ListView):
    template_name = 'task_app/events_list.html'
    paginate_by = 5
    context_object_name = 'event_list'

    def get_queryset(self):
        page_size = 5
        page = 1
        event_list = get_user_events(self.request.user.social_auth.all()[0], page, page_size)
        return event_list
