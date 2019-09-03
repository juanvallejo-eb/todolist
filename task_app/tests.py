import json
import unittest
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.forms import ValidationError
from .models import Priority, Task
from social_django.models import UserSocialAuth


def mocked_requests_get(*args, **_):
    class MockResponse:
        def __init__(self, json_data=None, status_code=200):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            with open('task_app/response_example.json', 'r') as f:
                return json.loads(f.read())

        def raise_for_status(self):
            pass
    return MockResponse()


class YourTestClass(TestCase):
    def setUp(self):
        self.high = Priority.objects.create(name='High')
        self.normal = Priority.objects.create(name='Normal')
        self.low = Priority.objects.create(name='Low')
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
    
        UserSocialAuth.objects.create(
            user=self.user,
            provider='eventbrite',
            uid='34563456',
            extra_data={
                'auth_time': 1567447106,
                'access_token': 'KLHJLJHLKJH',
                'token_type': 'bearer',
            }
        )

    def test_login(self):
        """Test login with valid user"""
        response = self.client.login(username='testuser', password='12345')
        self.assertEqual(response, True)

    def test_login_fail(self):
        """Test login with invalid user"""
        response = self.client.login(username='fred', password='secret')
        self.assertEqual(response, False)

    def test_task_creation(self):
        """Test model creation of tasks"""
        task = Task.objects.create(name='asd', done=False, priority=self.high, user=self.user, event_id=1234)
        task.full_clean()
        self.assertTrue(isinstance(task, Task))

    def test_invalid_task_creation(self):
        """Test that a validation error is raised if some fields are blank"""
        task = Task(name='asd')
        with self.assertRaises(ValidationError) as context:
            task.full_clean()
        self.assertEqual(set(context.exception.error_dict), set(['user', 'priority', 'event_id']))

    def test_login_url(self):
        """Test valid login url"""
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    @unittest.mock.patch('task_app.views.requests.get', side_effect=mocked_requests_get)
    def test_events_view(self, mocked_request):
        """Test the events view showing events"""
        self.client.force_login(self.user)
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['task_app/events_list.html'])
        self.assertContains(response, 'Recital EDA 3.0')

    @unittest.mock.patch('task_app.views.requests.get', side_effect=mocked_requests_get)
    def test_get_events_pages(self, mocked_request):
        """Test the call of the api with a page number"""
        self.client.force_login(self.user)
        response = self.client.get('/events/?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mocked_request.call_args[1]['params']['page'], '2')

    def test_events_view_without_login(self):
        """Test that the user gets redirected when is not logged in"""
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 302)

    def test_task_view(self):
        """Test valid task view url"""
        self.client.force_login(self.user)
        response = self.client.get('/events/{}/tasks/'.format(1234))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['task_app/task_list.html'])

    def test_invalid_task_view(self):
        """Test that tasks view can't be accessed with no event reference"""
        self.client.force_login(self.user)
        response = self.client.get('/events/tasks/')
        self.assertEqual(response.status_code, 404)

    def test_task_list(self):
        """Test task list showing task event's tasks"""
        self.client.force_login(self.user)
        event_id = 1234
        Task.objects.create(name='asd', done=False, priority=self.high, user=self.user, event_id=event_id)
        response = self.client.get('/events/{}/tasks/'.format(event_id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'asd')

    def test_task_list_only_user_tasks(self):
        """Test that the tasks list only shows tasks from the logged user"""
        other_user = User.objects.create_user(username='other_user', password='asdfghjkl')
        self.client.force_login(self.user)
        event_id = 1234
        Task.objects.create(name='Task name', done=False, priority=self.high, user=other_user, event_id=event_id)
        response = self.client.get('/events/{}/tasks/'.format(event_id))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Task name')

    def test_task_list_only_event_tasks(self):
        """Test that the tasks list only shows tasks from the selected event"""
        self.client.force_login(self.user)
        event_id = 1234
        Task.objects.create(name='Task name', done=False, priority=self.high, user=self.user, event_id=event_id)
        Task.objects.create(name='Other task', done=False, priority=self.high, user=self.user, event_id=4321)
        response = self.client.get('/events/{}/tasks/'.format(event_id))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Other task')

    def test_task_create_view(self):
        self.client.force_login(self.user)
        event_id = 1234
        response = self.client.post(
            '/events/{}/task/new/'.format(event_id),
            {'name': 'hello', 'priority': '{}'.format(self.normal.id), 'captcha_0': 'PASSED', 'captcha_1': 'PASSED'}
        )
        self.assertEqual(response.status_code, 302)
        task = Task.objects.get(name='hello')
        self.assertFalse(task.done)

    def test_task_update_view(self):
        self.client.force_login(self.user)
        event_id = 1234
        task = Task.objects.create(name='Task name', done=False, priority=self.high, user=self.user, event_id=event_id)
        response = self.client.post(
            '/events/{}/task/update/{}/'.format(event_id, task.id),
            {
                'name': 'test name',
                'done': 'True',
                'priority': '{}'.format(self.normal.id),
                'captcha_0': 'PASSED', 'captcha_1': 'PASSED'
            }
        )
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertEqual(task.name, 'test name')
        self.assertEqual(task.done, True)
