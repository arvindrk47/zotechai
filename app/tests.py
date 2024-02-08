from django.test import TestCase

# Create your tests here.

from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.utils import timezone
from .models import Todo

class APITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.token.created = timezone.now()
        self.token.expires = self.token.created + timedelta(days=3)
        self.token.save()

        self.client = APIClient()

    def test_obtain_token(self):
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_create_todo_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        todo_data = {'title': 'Test Task', 'description': 'Description of Test Task'}
        response = self.client.post('/api/todos/', todo_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Todo.objects.count(), 1)
        self.assertEqual(Todo.objects.first().title, 'Test Task')

    def test_create_todo_unauthenticated(self):
        todo_data = {'title': 'Test Task', 'description': 'Description of Test Task'}
        response = self.client.post('/api/todos/', todo_data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(Todo.objects.count(), 0)

    def test_get_todo_list_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        Todo.objects.create(title='Task 1', description='Description of Task 1', user=self.user)

        response = self.client.get('/api/todos/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Task 1')

    def test_get_todo_list_unauthenticated(self):
        Todo.objects.create(title='Task 1', description='Description of Task 1', user=self.user)

        response = self.client.get('/api/todos/')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(response.data), 0)

    def test_get_todo_detail_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        todo = Todo.objects.create(title='Task 1', description='Description of Task 1', user=self.user)

        response = self.client.get(f'/api/todos/{todo.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Task 1')

    def test_get_todo_detail_unauthenticated(self):
        todo = Todo.objects.create(title='Task 1', description='Description of Task 1', user=self.user)

        response = self.client.get(f'/api/todos/{todo.id}/')

        self.assertEqual(response.status_code, 401)
