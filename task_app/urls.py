from django.conf.urls import url
from .views import (
    TaskCreateView,
    TaskListView,
    TaskUpdateView,
    complete_task,
    TaskDeleteView,
    EventsView,
)


urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/tasks/$', TaskListView.as_view(), name='task_list'),
    url(r'^(?P<pk>[0-9]+)/task/new/$', TaskCreateView.as_view(), name='task_new'),
    url(r'^(?P<pk_event>[0-9]+)/task/complete/(?P<pk>[0-9]+)/$', complete_task, name='task_complete'),
    url(r'^(?P<pk_event>[0-9]+)/task/update/(?P<pk>[0-9]+)/$', TaskUpdateView.as_view(), name='task_update'),
    url(r'^(?P<pk_event>[0-9]+)/task/delete/(?P<pk>[0-9]+)/$', TaskDeleteView.as_view(), name='task_delete'),
    url(r'^$', EventsView.as_view(), name='events_list'),
]
