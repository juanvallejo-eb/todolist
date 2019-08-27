from django.conf.urls import url
from .views import TaskCreateView, TaskListView, TaskUpdateView, complete_task


urlpatterns = [
    url(r'^new/$', TaskCreateView.as_view(), name='task_new'),
    url(r'update/(?P<pk>[0-9]+)/$', TaskUpdateView.as_view(), name='task_update'),
    url(r'complete/(?P<pk>[0-9]+)/$', complete_task, name='task_complete'),
    url(r'^$', TaskListView.as_view(), name='task_list'),
]
