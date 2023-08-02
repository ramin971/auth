from .views import CookieTokenObtainPairView
from django.http import HttpResponse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken

# settings.AUTH_USER_MODEL
@receiver(post_save,sender=User)
def get_token_while_registration(sender,**kwargs):
    if kwargs['created']:
        print('777777777777777777777')
        # user=kwargs['instance']
        print(kwargs)
        refresh_token = RefreshToken.for_user(kwargs['instance'])
        if refresh_token:
            response = HttpResponse()
            cookie_max_age = 3600 * 24 * 14 # 14 days
            response.set_cookie('refresh_token', str(refresh_token), max_age=cookie_max_age, httponly=True )
            print('############',refresh_token)
            print('######type######',type(refresh_token))

            return response

        # result=CookieTokenObtainPairView(username=user.username,password=user.password)
        # refresh=result.refresh
        # access=result.access
        # print(result)