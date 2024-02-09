from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Todo

class TodoAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_todo_list(self):
        response = self.client.get('/api/todos/')
        self.assertEqual(response.status_code, 200)
        # Ensure no Todos are initially present
        self.assertEqual(len(response.data), 0)
    
    def test_create_todo(self):
        data = {'title': 'Test Todo', 'description': 'This is a test todo'}
        response = self.client.post('/api/todos/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Todo.objects.count(), 1)
        self.assertEqual(Todo.objects.get().title, 'Test Todo')
    
    def test_todo_detail(self):
        todo = Todo.objects.create(title='Test Todo', description='This is a test todo', user=self.user)
        response = self.client.get(f'/api/todos/{todo.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Test Todo')
    
    def test_update_todo(self):
        todo = Todo.objects.create(title='Test Todo', description='This is a test todo', user=self.user)
        data = {'title': 'Updated Todo', 'description': 'This is an updated todo'}
        response = self.client.put(f'/api/todos/{todo.id}/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Todo.objects.get().title, 'Updated Todo')
    
    def test_delete_todo(self):
        todo = Todo.objects.create(title='Test Todo', description='This is a test todo', user=self.user)
        response = self.client.delete(f'/api/todos/{todo.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Todo.objects.count(), 0)
