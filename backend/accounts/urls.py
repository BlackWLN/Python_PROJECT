# from django.urls import path
# from .views import CustomTokenObtainPairView, RegisterView, CurrentUserView

# urlpatterns = [
#     path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
#     path("register/", RegisterView.as_view(), name="register"),
#     path("me/", CurrentUserView.as_view(), name="current_user"),
#     path("signup/", signup_step1, name="signup_step1"),
#     path("signup/verify/", signup_step2, name="signup_step2"),
# ]

from django.urls import path
from .views import (
    CustomTokenObtainPairView,
    RegisterView,
    CurrentUserView,
    ProfileView
    signup_step1,
    signup_step2,
    custom_login,
)

urlpatterns = [
    path("api/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/me/", CurrentUserView.as_view(), name="current_user"),
    path("profile/", profile_view, name="profile"),
    path('profile/', ProfileView.as_view(), name='profile'),
    path("login/", custom_login, name="login"),
]
