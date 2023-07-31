from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.routers import DefaultRouter,SimpleRouter

router = SimpleRouter()
router.register('users',views.UserViewSet)
urlpatterns = [
    path('',include(router.urls)),
    path('change_password',views.ChangePassword.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]