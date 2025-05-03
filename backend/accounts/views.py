from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model, login, authenticate
from django.shortcuts import render, redirect
from .forms import CustomLoginForm, CustomSignupForm
from allauth.account.views import SignupView, LoginView
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()


# Сериализаторы
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Позволяем вход как по email, так и по username
        user = User.objects.filter(
            Q(email=attrs.get("email_or_username"))
            | Q(username=attrs.get("email_or_username"))
        ).first()

        if user:
            attrs["email"] = user.email
            data = super().validate(attrs)
            return data
        raise serializers.ValidationError("Неверные учетные данные")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_teacher"]


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


# API Представления
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Автоматический вход после регистрации
        login(request, user)

        return Response(
            {"user": UserSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# HTML Представления
class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    template_name = "account/signup.html"

    def form_valid(self, form):
        # Проверка совпадения паролей
        if form.cleaned_data["password1"] != form.cleaned_data["password2"]:
            form.add_error("password2", "Пароли не совпадают")
            return self.form_invalid(form)

        response = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        return response


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "account/login.html"

    def form_valid(self, form):
        # Позволяем вход как по email, так и по username
        credentials = {"password": form.cleaned_data["password"]}

        email_or_username = form.cleaned_data["login"]
        if "@" in email_or_username:
            credentials["email"] = email_or_username
        else:
            credentials["username"] = email_or_username

        user = authenticate(**credentials)
        if user:
            login(self.request, user)
            return redirect(self.get_success_url())

        form.add_error(None, "Неверные учетные данные")
        return self.form_invalid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class CustomLogoutView(View):
    def get(self, request):
        from django.contrib.auth import logout

        logout(request)
        return redirect("home")
