from accounts.models import User  # Импорт вашей кастомной модели


def create_user(strategy, details, user=None, **kwargs):
    if user:
        return {"is_new": False}

    # Автоматическое создание пользователя при OAuth-входе
    user = User.objects.create(
        username=details["email"].split("@")[0],
        email=details["email"],
        is_teacher=False,  # Все OAuth-пользователи по умолчанию студенты
        first_name=details.get("first_name", ""),
        last_name=details.get("last_name", ""),
    )
    return {"is_new": True, "user": user}
