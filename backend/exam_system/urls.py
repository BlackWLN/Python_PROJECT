# from django.contrib import admin
# from django.urls import path, include
# from . import views
# from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
# from accounts.views import CustomTokenObtainPairView, RegisterView, CurrentUserView

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     # Аутентификация
#     path(
#         "api/auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
#     ),
#     path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
#     path("api/auth/register/", RegisterView.as_view(), name="register"),
#     path("api/auth/me/", CurrentUserView.as_view(), name="current_user"),
#     # path("", views.home_view, name="home"),  # Корневой URL
#     path("", include("exams.urls")),
#     path("exams/", include("exams.urls")),
#     path("api/", include("exams.urls")),
#     path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
#     path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
#     # Приложения
#     # path("api/accounts/", include("accounts.urls")),
#     # path("api/exams/", include("exams.urls")),
# ]

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import (
    CustomTokenObtainPairView,
    RegisterView,
    CurrentUserView,
    CustomSignupView,
    CustomLoginView,
    ProfileView,
)
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Аутентификация
    path(
        "api/auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/me/", CurrentUserView.as_view(), name="current_user"),
    # OAuth
    path("accounts/", include("allauth.urls")),
    # Приложение exams
    # path("", include("exams.urls")),  # Все URL из exams будут доступны от корня
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
    path("accounts/signup/", CustomSignupView.as_view(), name="account_signup"),
    path("accounts/login/", CustomLoginView.as_view(), name="account_login"),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("exams/", include("exams.urls")),
]
