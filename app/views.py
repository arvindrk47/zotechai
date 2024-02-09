from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes  # Import the permission_classes decorator
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
from django.db import IntegrityError
from django.contrib.auth.models import User
import logging

class ObtainTokenView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({
                'error': 'Please provide both username and password'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None:
            try:
                user = User.objects.create_user(username=username, password=password)
            except IntegrityError:
                return Response({
                    'error': 'Username already exists',
                }, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)

        # Set token expiration
        token.expires = datetime.now() + timedelta(days=3)
        token.save()

        return Response({
            'token': token.key
        })

class TodoListView(APIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]  # Set permission_classes as a class attribute

    def get(self, request):
        todos = Todo.objects.filter(user=request.user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        logger = logging.getLogger(__name__)

        # Log request data
        logger.info(f"Request data: {request.data}")

        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            # Automatically associate the authenticated user with the ToDo item
            serializer.validated_data['user'] = request.user
            serializer.save()
            # Log validated data
            logger.info(f"Validated data: {serializer.validated_data}")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Log serializer errors
            logger.error(f"Serializer errors: {serializer.errors}")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk, user=request.user)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk, user=request.user)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk, user=request.user)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
