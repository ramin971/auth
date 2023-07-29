from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer,UserUpdateSerializer
from rest_framework.viewsets import ModelViewSet

    

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    # serializer_class = UserSerializer
    def get_serializer_class(self):
        if self.action == 'update':
            return UserUpdateSerializer
        return UserSerializer