# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.contrib.auth.hashers import make_password


# class User(AbstractUser):
#     username = None  # Полностью отключаем username
#     email = models.EmailField(unique=True)
#     confirmation_code = models.CharField(max_length=128, blank=True)  # Хешированный код

#     USERNAME_FIELD = "email"  # Используем email для аутентификации
#     REQUIRED_FIELDS = []  # Убираем обязательные поля

#     is_teacher = models.BooleanField(default=False)
#     exams_passed = models.ManyToManyField(
#         "exams.Exam",  # Явное указание приложения
#         through="UserExam",
#         related_name="passed_users",
#     )

#     def save(self, *args, **kwargs):
#         # Хешируем код (если он есть) перед сохранением
#         if self.confirmation_code and not self.confirmation_code.startswith("pbkdf2_"):
#             self.confirmation_code = make_password(self.confirmation_code)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.email


# class UserExam(models.Model):
#     user = models.ForeignKey("User", on_delete=models.CASCADE)  # Строковая ссылка
#     exam = models.ForeignKey("exams.Exam", on_delete=models.CASCADE)
#     score = models.IntegerField()
#     completed_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = [["user", "exam"]]
# вроде рабочий вариант ниже

# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.contrib.auth.hashers import make_password
# from django.core.mail import send_mail
# from django.conf import settings
# import random


# class User(AbstractUser):
#     username = None
#     email = models.EmailField(unique=True)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []

#     # Дополнительные поля если нужно
#     is_teacher = models.BooleanField(default=False)

#     def __str__(self):
#         return self.email


# class UserExam(models.Model):
#     user = models.ForeignKey("User", on_delete=models.CASCADE)
#     exam = models.ForeignKey("exams.Exam", on_delete=models.CASCADE)
#     score = models.IntegerField()
#     completed_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = [["user", "exam"]]

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, verbose_name="Логин")
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    is_teacher = models.BooleanField(default=False, verbose_name="Преподаватель")

    USERNAME_FIELD = "email"  # Основное поле для входа
    REQUIRED_FIELDS = ["username"]  # Обязательные поля при создании пользователя

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username or self.email

    @classmethod
    def get_by_natural_key(cls, email):
        # Позволяет искать пользователя как по email, так и по username
        return cls.objects.get(Q(email=email) | Q(username=email))


class UserExam(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    exam = models.ForeignKey(
        "exams.Exam", on_delete=models.CASCADE, verbose_name="Экзамен"
    )
    score = models.IntegerField(verbose_name="Оценка")
    completed_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата завершения"
    )

    class Meta:
        verbose_name = "Результат экзамена"
        verbose_name_plural = "Результаты экзаменов"
        unique_together = [["user", "exam"]]
