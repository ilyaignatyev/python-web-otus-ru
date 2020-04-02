"""
Права для API
"""

from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class TeacherPermissions(BasePermission):
    """
    Права на преподавателей
    - просмотр: все
    - создание, изменение, удаление: суперпользователь
    """
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or request.user and request.user.is_superuser)


class StudentPermissions(BasePermission):
    """
    Права на студентов
    - просмотр: суперпользователь, сам студент, студент, администратор или преподаватель курса,
                на который записан студент (проверяется в менеджере в for_user_queryset)
    - создание, изменение, удаление: суперпользователь
    """
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS and not request.user.is_superuser:
            return False
        return True


class AdministratorPermissions(BasePermission):
    """
    Права на администраторов
    - просмотр: суперпользователь, сам администратор, администратор, студент или преподаватель курса, на котором
                администратор является администратором  (проверяется в менеджере в for_user_queryset)
    - создание, изменение, удаление: суперпользователь
    """
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS and not request.user.is_superuser:
            return False
        return True


class CoursePermissions(BasePermission):
    """
    Права на курс
    - просмотр: все
    - создание: суперпользователь
    - изменение: суперпользователь или администратор этого курса
    - удаление: суперпользователь
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_superuser
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user.is_superuser
        elif request.method == 'PUT':
            return obj.can_update(obj.id, request.user)
        return True


class CourseEntryPermissions(BasePermission):
    """
    Права на запись стедунта на курс
    - просмотр: суперпользователь, сам студент, администратор этого курса (проверяется в менеджере в for_user_queryset)
    - создание: суперпользователь, сам студент, администратор этого курса
    - изменение: суперпользователь, администратор этого курса
    - удаление: суперпользователь, сам студент, админитратор этого курса
    """
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method == 'POST':
            from .models import Course, Student
            course_id = request.data.get('course')
            student_id = request.data.get('student')
            get_object_or_404(Course, id=course_id)
            student = get_object_or_404(Student, id=student_id)
            return student_id is not None and student.user == request.user or \
                   Course.is_admin(course_id, request.user.id)

        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        from .models import Course

        if request.method == 'DELETE':
            return obj.student.user == request.user or \
                   Course.is_admin(obj.course.id, request.user.id)
        elif request.method == 'PUT':
            return Course.is_admin(obj.course.id, request.user.id)
        return True


class CourseAdminPermissions(BasePermission):
    """
    Права на связь администратора курса с курсом
    - просмотр: суперпользователь, сам администратор, администратор этого курса (проверяется в менеджере в
                for_user_queryset)
    - создание: суперпользователь
    - изменение: суперпользователь
    - удаление: суперпользователь
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_superuser
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'DELETE'):
            return request.user.is_superuser
        return True


class LessonPermissions(BasePermission):
    """
    Права на уроки
    - просмотр: студент, преподаватель, администратор курса, к которому относится урок (проверяется в менеджере
                в for_user_queryset)
    - создание: суперпользователь, администратор курса, к которому относится урок
    - изменение: суперпользователь, администратор курса, к которому относится урок, преподаватель урока
    - удаление: суперпользователь, администратор курса, к которому относится урок
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            from .models import Lesson, Course
            course_id = request.data.get('course')
            get_object_or_404(Course, id=course_id)
            return Lesson.can_cud(course_id, request.user)
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'DELETE'):
            return obj.can_cud(obj.course.id, request.user)
        return True
