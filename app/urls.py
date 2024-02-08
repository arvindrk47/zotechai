from django.urls import path
from .views import ObtainTokenView, TodoListView, TodoDetailView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('token/', ObtainTokenView.as_view(), name='obtain-token'),
    path('todos/', TodoListView.as_view(), name='todo-list'),
    path('todos/<int:pk>/', TodoDetailView.as_view(), name='todo-detail'),
    path('login/', obtain_auth_token, name='login'),
]