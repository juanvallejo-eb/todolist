from django.conf.urls import url
from .views import TaskCreateView, TaskListView, TaskUpdateView, complete_task, TaskDeleteView


urlpatterns = [
    url(r'^new/$', TaskCreateView.as_view(), name='task_new'),
    url(r'update/(?P<pk>[0-9]+)/$', TaskUpdateView.as_view(), name='task_update'),
    url(r'complete/(?P<pk>[0-9]+)/$', complete_task, name='task_complete'),
    url(r'delete/(?P<pk>[0-9]+)/$', TaskDeleteView.as_view(), name='task_delete'),
    url(r'^$', TaskListView.as_view(), name='task_list'),
]
