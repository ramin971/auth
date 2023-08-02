from django.contrib.auth.models import User
from .serializers import UserSerializer,UserUpdateSerializer\
    ,ChangePasswordSerializer,CookieTokenRefreshSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes =[IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'update':
            return UserUpdateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'update':
            return [IsAuthenticated()]
        elif self.action == 'create':
            return [AllowAny()]
        else:
            return [IsAdminUser()]
    
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

class CookieTokenObtainPairView(TokenObtainPairView):
  def finalize_response(self, request, response, *args, **kwargs):
    if response.data.get('refresh'):
        cookie_max_age = 3600 * 24 * 14 # 14 days
        response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )
        del response.data['refresh']
    return super().finalize_response(request, response, *args, **kwargs)

class CookieTokenRefreshView(TokenRefreshView):

    # If SimpleJWT ROTATE_REFRESH_TOKENS = True :
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14 # 14 days
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)
    serializer_class = CookieTokenRefreshSerializer