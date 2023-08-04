from .views import CookieTokenObtainPairView,CookieTokenRefreshView
from django.http import HttpResponse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

# settings.AUTH_USER_MODEL
@receiver(post_save,sender=User)
def get_token_while_registration(sender,instance,created,**kwargs):
    if created:
        # Create an HttpResponse object
        # response = HttpResponse()

        # Set the cookie using the HttpResponse.set_cookie() method
        # instance.response = response
        # instance.set_cookie('my_cookie', 'cookie_value')
        
        # Return the response
        # return instance.response
    
        # refresh_token = RefreshToken.for_user(instance)
        # my_view=TokenRefreshView(refresh=refresh_token)
        # my_view=CookieTokenRefreshView(refresh=refresh_token)
        # my_view.finalize_response()
        # print(my_view)
        # response = HttpResponse()
        # response.set_cookie('my_cookie','cookie_value')
        print('#####signal#####')
    # if kwargs['created']:
       
    #     refresh_token = RefreshToken.for_user(kwargs['instance'])
    #     if refresh_token:
    #         response = HttpResponse('signal')
            # cookie_max_age = 3600 * 24 * 14 # 14 days
            # response.set_cookie('refresh_token', str(refresh_token), max_age=cookie_max_age, httponly=True )
            # print('############',refresh_token)
            # print('######str######',str(refresh_token))
            # print('######type str######',type(str(refresh_token)))
            # print('######type######',type(refresh_token))
            # response.set_cookie('my_cookie', 'cookie_value')
            # response['Set-Cookie'] = ('food=bread; drink=water; Path=/; max_age=10')
            
            # print()
            # return response

        # result=CookieTokenObtainPairView(username=user.username,password=user.password)
        # refresh=result.refresh
        # access=result.access
        # print(result)