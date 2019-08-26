from django.conf.urls import url
from .views import TaskCreateView, TaskListView, TaskUpdateView


urlpatterns = [
    url(r'^new/$', TaskCreateView.as_view(), name='task_new'),
    url(r'update/(?P<pk>[0-9]+)/$', TaskUpdateView.as_view(), name='task_update'),
    url(r'^$', TaskListView.as_view(), name='task_list'),
]
