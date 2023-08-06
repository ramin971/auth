from django.contrib.auth.models import User
from .serializers import UserSerializer,UserUpdateSerializer\
    ,ChangePasswordSerializer,CookieTokenRefreshSerializer
from .permissions import CreateOrIsAdmin
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView,ListCreateAPIView
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    permission_classes =[CreateOrIsAdmin]

    def get_serializer_class(self):
        if self.action == 'update':
            return UserUpdateSerializer
        return UserSerializer
    # add page_size to response
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['page_size'] = str(PageNumberPagination.page_size)
        return response
    # create_user / set refresh_cookie / add access_response
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # NOT WORK : save user without hashed password 
        # self.perform_create(serializer) # NONE
        # user = get_object_or_404(User,pk=serializer.data.get('id'))
        # print('###req.data: ',request.data)
        # print('###serializer.data: ',serializer.data)
        # print('$$$$$req.data$$$$$$$',request.data['password'],type(request.data['password'])) WORKED
        # print(serializer.validated_data)
        # print(serializer.validated_data['password'],type(serializer.validated_data['password']))
        user = User.objects.create_user(password=serializer.validated_data['password'],**serializer.data)
        refresh_token = RefreshToken.for_user(user)
        
        result = {**serializer.data , **{'access':str(refresh_token.access_token)}}
        response = Response(result , status=status.HTTP_201_CREATED)
        cookie_max_age = 3600 * 24 * 14 # 14 days
        response.set_cookie('refresh_token', refresh_token, max_age=cookie_max_age, httponly=True )
        return response

    @action(detail=False , methods=['get','put','delete'],permission_classes=[IsAuthenticated])
    def me(self,request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            
            print('########get mycookie:',request.COOKIES.get('my_cookie'))
            # print('##########get_cookie',request.COOKIES.get('refresh_token'))
            # print(type(request.COOKIES.get('refresh_token')))
            return Response(serializer.data,status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = UserUpdateSerializer(user,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
    # @action(detail=False, methods=['post'],serializer_class=ChangePasswordSerializer)
    # def change_password(self,request):
    #     if request.method == 'POST':
    #         # serializer = ChangePasswordSerializer(data=request.data)
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data,status=status.HTTP_205_RESET_CONTENT)


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