"""
Пользователи
"""
from django.contrib.auth.models import User
from django.db.models import Q

from .const import USER_TYPE


def get_user_type(user_id) -> int:
    """
    Возвращает тип пользователя
    :param user_id: идентификатор ппользователя
    :return: Тип
    """
    record = User.objects.filter(Q(student__user__id=user_id) | Q(teacher__user__id=user_id) |
                                 Q(administrator__user__id=user_id)).values('student__id', 'teacher__id',
                                                                            'administrator__id').first()
    for field, result in zip(['student__id', 'teacher__id', 'administrator__id'],
                             [USER_TYPE.STUDENT, USER_TYPE.TEACHER, USER_TYPE.ADMINISTRATOR]):
        if record.get(field) is not None:
            return result
    return USER_TYPE.UNAUTHORIZED


def create_user(profile_data: dict, user_data: dict, model=None, user_type: int = None):
    """
    Создание пользователя определенного типа
    :param profile_data: Данные профиля
    :param user_data: Данные пользвоателя
    :param model: Класс пользователя
    :param user_type: Тип (если класс не передан)
    :return: Пользователь
    """
    profile = User.objects.create_user(
        username=profile_data.get('username'),
        first_name=profile_data.get('first_name'),
        last_name=profile_data.get('last_name'),
        email=profile_data.get('email'),
        password=profile_data.get('password')
    )

    if model is None and type is not None:
        from .models import Student, Teacher, Administrator
        model = {
            USER_TYPE.STUDENT: Student,
            USER_TYPE.TEACHER: Teacher,
            USER_TYPE.ADMINISTRATOR: Administrator,
        }[user_type]

    return model.objects.create(user=profile, about=user_data['about'])


def update_user(user, profile_data: dict, user_data: dict):
    """
    Обновление данных пользователя
    :param user: Пользвоатель (Преподаватель/Студент/Администратор)
    :param profile_data: Данные профиля
    :param user_data: Данные пользвоателя
    :return: Пользователь
    """
    for field in profile_data:
        setattr(user.user, field, profile_data[field])

    for field in user_data:
        setattr(user, field, user_data[field])
    user.save()
    return user
