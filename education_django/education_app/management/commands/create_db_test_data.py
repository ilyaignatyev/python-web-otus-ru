"""
Заполняет базу данных тестовыми данными
"""
import random

from django.contrib.auth.models import User
from django.core.management import BaseCommand
import factory

from education_app.factories import TeacherFactory, StudentFactory, AdministratorFactory, CourseFactory, CourseEntryFactory, \
    CourseAdminFactory, LessonFactory
from education_app.models import Lesson, Student, Administrator, Teacher, Course, CourseAdmin, CourseEntry


class Command(BaseCommand):
    help = 'Creates test data in database'

    @factory.Faker.override_default_locale('ru_RU')
    def handle(self, *args, **kwargs):
        for model in [CourseAdmin, CourseEntry, Lesson, Course, Student, Administrator, Teacher, User]:
            model.objects.all().delete()

        User.objects.create_superuser(username='superuser', password='123', email='superuser@gmail.com')

        students = StudentFactory.create_batch(1000)
        administrators = AdministratorFactory.create_batch(20)
        teachers = TeacherFactory.create_batch(100)
        courses = CourseFactory.create_batch(100)
        self.__create_batch_with_check(300, CourseAdminFactory, courses, administrators, 'course', 'admin')
        self.__create_batch_with_check(4000, CourseEntryFactory, courses, students, 'course', 'student')
        self.__create_batch_with_check(3000, LessonFactory, courses, teachers, 'course', 'teacher')

    @staticmethod
    def __create_batch_with_check(count, factory, list1, list2, name1, name2):
        """
        Массовое создание объектов (уроки/записи студентов на курсы/связи администраторов с курсами) с заполнением
        связанных объектов из переданных списков с проверкой на уникальность пары объект1+объект2
        :param count: Количество
        :param factory: Фабрика
        :param list1: Список объектов первого типа
        :param list2: Список объектов второго типа
        :param name1: Название поля в модели для объекта первого типа
        :param name2: Название поля в модели для объекта второго типа
        """
        check_dict = {}
        for idx in range(count):
            obj1 = random.choice(list1)
            obj2 = random.choice(list2)
            if obj1.id not in check_dict:
                check_dict[obj1.id] = []
            elif obj2.id in check_dict[obj1.id]:
                continue
            check_dict[obj1.id].append(obj2.id)
            params = {name1: obj1, name2: obj2}
            factory(**params)
