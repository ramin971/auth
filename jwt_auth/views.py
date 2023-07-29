from django.contrib.auth.models import User
from .serializers import UserSerializer,UserUpdateSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
    

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'update':
            return UserUpdateSerializer
        return UserSerializer
    
    @action(detail=False , methods=['GET','PUT','PATCH'])
    def me(self,request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        elif request.method == 'PATCH' or 'PUT':
            serializer = UserUpdateSerializer(user,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)

    # def update(self, request, *args, **kwargs):
    #     kwargs['partial']=True
    #     return super().update(request, *args, **kwargs)