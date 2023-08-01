from django.contrib.auth.models import User
from .serializers import UserSerializer,UserUpdateSerializer,ChangePasswordSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.shortcuts import get_object_or_404

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes =[IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'update':
            return UserUpdateSerializer
        return UserSerializer
    
    @action(detail=False , methods=['get','put'],permission_classes=[IsAuthenticated])
    def me(self,request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = UserUpdateSerializer(user,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)


class ChangePassword(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user':self.request.user}
    
    # Change Status_Code of ChangePassword from 201 to 205
    def create(self, request, *args, **kwargs):
        result = super().create(request, *args, **kwargs)
        result.status_code = 205
        return result

    
