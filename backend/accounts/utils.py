import random
from django.core.mail import send_mail


def generate_and_send_code(email):
    code = str(random.randint(100000, 999999))
    send_mail(
        "Ваш код подтверждения",
        f"Код для входа: {code}",
        "noreply@yourdomain.com",
        [email],
        fail_silently=False,
    )
    return code  # Возвращаем нехешированный код для проверки
