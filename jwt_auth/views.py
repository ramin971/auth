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
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken




class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    # permission_classes =[IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'update':
            return UserUpdateSerializer
        return UserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer) # NONE
        # print('###req.data: ',request.data)
        # print('###serializer.data: ',serializer.data)
        # user = User.objects.create_user(password=request.data['password'][0],**serializer.data)
        user = get_object_or_404(User,pk=serializer.data.get('id'))
        refresh_token = RefreshToken.for_user(user)
        
        result = {**serializer.data , **{'access':str(refresh_token.access_token)}}
        response = Response(result , status=status.HTTP_201_CREATED)
        cookie_max_age = 3600 * 24 * 14 # 14 days
        response.set_cookie('refresh_token', refresh_token, max_age=cookie_max_age, httponly=True )
        # response['access'] = str(refresh_token.access_token) #add to head of response

        return response
        

    def get_permissions(self):
        return [AllowAny()]
        # if self.request.method == 'GET':
        #     print('g')
        #     if self.action == 'list':
        #         print('l')
        #         return [AllowAny()]
        #     elif self.action == 'retrieve':
        #         print('r')
        #         return [AllowAny()]

            # return
        # elif self.request.method == 'PUT':
            # print('p')
            # return [IsAuthenticated()]
        # elif self.request.method == 'POST':
            # print('c')
            # return [AllowAny()]
        # else:
        #     if self.action == 'list':
        #         return [IsAdminUser()]
        #     elif self.action == 'retrieve':
        #         return [IsAuthenticated()]
    
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