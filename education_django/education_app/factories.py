"""
Фабрики объектов
"""
import datetime

import factory
from .models import Teacher, Student, Administrator, Course, CourseEntry, CourseAdmin, Lesson
from django.contrib.auth.models import User


class UserFactory(factory.DjangoModelFactory):
    """
    Фабрика профилей
    """
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', '123')


class TeacherFactory(factory.DjangoModelFactory):
    """
    Фабрика учителей
    """
    class Meta:
        model = Teacher

    user = factory.SubFactory(UserFactory)
    about = factory.Faker('text', max_nb_chars=1000)


class StudentFactory(factory.DjangoModelFactory):
    """
    Фабрика студентов
    """
    class Meta:
        model = Student

    user = factory.SubFactory(UserFactory)
    about = factory.Faker('text', max_nb_chars=1000)


class AdministratorFactory(factory.DjangoModelFactory):
    """
    Фабрика студентов
    """
    class Meta:
        model = Administrator

    user = factory.SubFactory(UserFactory)
    about = factory.Faker('text', max_nb_chars=1000)


class CourseFactory(factory.DjangoModelFactory):
    """
    Фабрика курсов
    """
    class Meta:
        model = Course

    name = factory.Faker('sentence')
    description = factory.Faker('paragraph')
    start = factory.Faker('date_between_dates', date_start=datetime.date(2015, 1, 1), date_end=datetime.date(2021, 12, 31))
    cost = factory.Faker('random_int', min=2000, max=100000)


class CourseEntryFactory(factory.DjangoModelFactory):
    """
    Фабрика записей на курсы
    """
    class Meta:
        model = CourseEntry

    date = factory.Faker('date')
    cost = factory.Faker('random_int', min=2000, max=100000)
    paid = factory.Faker('random_element', elements=[True, False])


class CourseAdminFactory(factory.DjangoModelFactory):
    """
    Фабрика связи администратора с курсом
    """
    class Meta:
        model = CourseAdmin

    start = factory.Faker('date')


class LessonFactory(factory.DjangoModelFactory):
    """
    Фабрика связи администратора с курсом
    """
    class Meta:
        model = Lesson

    name = factory.Faker('sentence')
    start = factory.Faker('date_time_this_year', after_now=True)
    description = factory.Faker('text', max_nb_chars=1000)
