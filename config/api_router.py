from django.conf import settings
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from custom_jwt_auth.users.api.views import (
    UserViewSet,
    RegistrationAPIView,
    LoginAPIView,
    UserRetrieveUpdateAPIView,
)


router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)


urlpatterns = [
    path("register/", RegistrationAPIView.as_view(), name="sign_up"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("user/", UserRetrieveUpdateAPIView.as_view()),
]

app_name = "api"
urlpatterns += router.urls
