"""
Менеджеры для моделей
"""

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

from .const import USER_TYPE
from .users import get_user_type


class TeacherManager(models.Manager):
    """
    Менеджер модели преподавателя
    """


class StudentManager(models.Manager):
    """
    Менеджер модели студента
    """
    @staticmethod
    def for_user_queryset(user: User):
        """
        Возвращает студентов, доступных для просмотра текущему пользователю
        (суперпользователь, сам студент, студент, администратор или преподаватель курса, на который записан студент)
        :param user: Текущий пользователь
        :return: Студенты
        """
        from .models import Student
        query = Student.objects

        if user.is_superuser:
            return query

        user_type = get_user_type(user.id)
        if user_type == USER_TYPE.UNAUTHORIZED:
            return query.none()

        if user_type == USER_TYPE.STUDENT:
            return query.filter(Q(user__id=user.id) | Q(courseentry__student__user__id=user.id)).distinct()

        if user_type == USER_TYPE.TEACHER:
            return query.filter(courseentry__course__lesson__teacher__user__id=user.id).distinct()

        if user_type == USER_TYPE.ADMINISTRATOR:
            return query.filter(courseentry__course__courseadmin__administrator__user__id=user.id).distinct()

        return query.none()


class AdministratorManager(models.Manager):
    """
    Менеджер модели администратора
    """
    @staticmethod
    def for_user_queryset(user: User):
        """
        Возвращает администраторов, доступных для просмотра текущему пользователю
        (суперпользователь, сам администратор, администратор, студент или преподаватель курса, на котором
        администратор является администратором)
        :param user: Текущий пользователь
        :return: Админитраторы
        """
        from .models import Administrator
        query = Administrator.objects

        if user.is_superuser:
            return query

        user_type = get_user_type(user.id)
        if user_type == USER_TYPE.UNAUTHORIZED:
            return query.none()

        if user_type == USER_TYPE.STUDENT:
            return query.filter(courseadmin__course__student__user__id=user.id).distinct()

        if user_type == USER_TYPE.TEACHER:
            return query.filter(courseadmin__course__lesson__teacher__user__id=user.id).distinct()

        if user_type == USER_TYPE.ADMINISTRATOR:
            return query.filter(Q(user__id=user.id) |
                                Q(courseadmin__course__courseadmin__admin__user__id=user.id)).distinct()

        return query.none()


class CourseEntryManager(models.Manager):
    """
    Менеджер модели записи на курс
    """
    @staticmethod
    def for_user_queryset(user: User):
        """
        Возвращает записи на курс, доступные для просмотра текущему пользователю
        (суперпользователь, сам студент, администратор этого курса)
        :param user: Текущий пользователь
        :return: Записи студентов на курс
        """
        from .models import CourseEntry
        query = CourseEntry.objects

        if user.is_superuser:
            return query

        user_type = get_user_type(user.id)
        if user_type == USER_TYPE.UNAUTHORIZED:
            return query.none()

        if user_type == USER_TYPE.STUDENT:
            return query.filter(student__user__id=user.id)

        if user_type == USER_TYPE.ADMINISTRATOR:
            return query.filter(course__courseadmin__admin__user__id=user.id).distinct()

        return query.none()


class CourseAdminManager(models.Manager):
    """
    Менеджер модели связи администратора с курсом
    """
    @staticmethod
    def for_user_queryset(user: User):
        """
        Возвращает связи администратора с курсом, доступные для просмотра текущему пользователю
        (суперпользователь, сам администратор, администратор этого курса)
        :param user: Текущий пользователь
        :return: Записи студентов на курс
        """
        from .models import CourseAdmin
        query = CourseAdmin.objects

        if user.is_superuser:
            return query

        user_type = get_user_type(user.id)
        if user_type == USER_TYPE.UNAUTHORIZED:
            return query.none()

        if user_type == USER_TYPE.ADMINISTRATOR:
            return query.filter(course__courseadmin__admin__user__id=user.id).distinct()

        return query.none()


class LessonManager(models.Manager):
    """
    Менеджер модели урока
    """
    @staticmethod
    def for_user_queryset(user: User):
        """
        Возвращает уроки, доступные для просмотра текущему пользователю
        (студент, преподаватель, администратор курса, к которому относится урок)
        :param user: Текущий пользователь
        :return: Уроки
        """
        from .models import Lesson
        query = Lesson.objects

        if user.is_superuser:
            return query

        user_type = get_user_type(user.id)
        if user_type == USER_TYPE.UNAUTHORIZED:
            return query.none()

        if user_type == USER_TYPE.STUDENT:
            return query.filter(course__courseentry__student__user__id=user.id).distinct()

        if user_type == USER_TYPE.TEACHER:
            return query.filter(course__lesson__teacher_user_id=user.id).distinct()

        if user_type == USER_TYPE.ADMINISTRATOR:
            return query.filter(course__courseadmin__admin__user__id=user.id).distinct()

        return query.none()
