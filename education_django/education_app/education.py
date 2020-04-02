"""
Общие функции
"""

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Course, Student, Administrator, Teacher


def get_user_course_rights(user: User, course_id: int):
    """
    Возвращает права пользователя на элементы курса:
    - уроки
    - записи студентов
    - студентов
    - администраторов
    :param user: Текущий пользователь
    :param course_id: Идентификатор курса
    :return: Права
        course_u - изенение курсов
        course_d - удаление курсов
        lesson_cud - создание/изменение/удаление уроков
        students_v - просмотр списка студентов курса
        my_courseentry_c - запись текущего пользователя на курс
        my_courseentry_d - удаление записи текущего пользователя на курс
        courseentry_cud - создание/изменение/удаление записи произвольного студента на курс
        courseadmin_cud - создание/изменение/удаление администратора курса
        courseadmins_v - просмотр списка администраторов курса
    """
    result = {
        'course_u': False,
        'course_d': False,
        'lesson_cud': False,
        'students_v': False,
        'my_courseentry_c': False,
        'my_courseentry_d': False,
        'courseentry_cud': False,
        'courseadmin_cud': False,
        'courseadmins_v': False
    }
    cur_user_id = user.id
    superuser = user.is_superuser

    if superuser:
        for key in set(result.keys()) - {'my_courseentry_c', 'my_courseentry_d'}:
            result[key] = True
        return result

    course = get_object_or_404(Course, id=course_id)

    administrator = Administrator.get_by_user(cur_user_id)
    course_admin = administrator in course.admins.all() if administrator else False
    student = Student.get_by_user(cur_user_id)
    teacher = Teacher.get_by_user(cur_user_id)
    course_students = course.students.all()

    result['course_u'] = superuser or course_admin
    result['course_d'] = superuser
    result['lesson_cud'] = course_admin
    result['students_v'] = course_admin or teacher
    result['my_courseentry_c'] = student is not None and student not in course_students
    result['my_courseentry_d'] = student is not None and student in course_students
    result['courseentry_cud'] = course_admin
    result['courseadmin_cud'] = False
    result['courseadmins_v'] = course_admin

    return result
