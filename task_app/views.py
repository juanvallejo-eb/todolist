import requests

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin
from pure_pagination.paginator import Paginator, Page

from django import forms
from django.urls import reverse_lazy
from captcha.fields import CaptchaField
from .models import Task
from django.shortcuts import redirect

from . import EVENTBRITEAPI


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


class ApiQuerySet:
    def __init__(self, api_result):
        self.api_result = api_result
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.api_result['events']):
            raise StopIteration
        next_value = self.api_result['events'][self.index]
        self.index += 1
        return next_value

    def count(self):
        return self.api_result['pagination']['object_count']


class ApiPaginator(Paginator):
    def page(self, number):
        "Returns a Page object for the given 1-based page number."
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return Page(self.object_list, number, self)


class EventsView(LoginRequiredMixin, PaginationMixin, ListView):
    template_name = 'task_app/events_list.html'
    paginate_by = 5
    paginator_class = ApiPaginator

    def get_user_events(self, user):
        token = user.social_auth.all()[0].access_token
        url = EVENTBRITEAPI
        page = self.request.GET['page'] if 'page' in self.request.GET else 1
        page_size = self.paginate_by
        headers = {
            'Authorization': 'Bearer '+token
        }
        params = {
            'page': page,
            'page_size': page_size
        }
        response = requests.get(url, headers=headers, params=params).json()
        return response

    def get_queryset(self):
        api_result = self.get_user_events(self.request.user)
        return ApiQuerySet(api_result)
