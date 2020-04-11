"""
Фабрики объектов
"""

import factory
from .models import Teacher, Student, Administrator, Course, CourseEntry, CourseAdmin, Lesson
from django.contrib.auth.models import User


class UserFactory(factory.DjangoModelFactory):
    """
    Фабрика профилей
    """
    class Meta:
        model = User


class TeacherFactory(factory.DjangoModelFactory):
    """
    Фабрика учителей
    """
    class Meta:
        model = Teacher

    user = factory.SubFactory(UserFactory)


class StudentFactory(factory.DjangoModelFactory):
    """
    Фабрика студентов
    """
    class Meta:
        model = Student

    user = factory.SubFactory(UserFactory)


class AdministratorFactory(factory.DjangoModelFactory):
    """
    Фабрика студентов
    """
    class Meta:
        model = Administrator

    user = factory.SubFactory(UserFactory)


class CourseFactory(factory.DjangoModelFactory):
    """
    Фабрика курсов
    """
    class Meta:
        model = Course


class CourseEntryFactory(factory.DjangoModelFactory):
    """
    Фабрика записей на курсы
    """
    class Meta:
        model = CourseEntry


class CourseAdminFactory(factory.DjangoModelFactory):
    """
    Фабрика связи администратора с курсом
    """
    class Meta:
        model = CourseAdmin


class LessonFactory(factory.DjangoModelFactory):
    """
    Фабрика связи администратора с курсом
    """
    class Meta:
        model = Lesson
