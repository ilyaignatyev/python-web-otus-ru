from django.contrib.auth.models import User
from django.db.models import Q

from const import USER_TYPE


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
