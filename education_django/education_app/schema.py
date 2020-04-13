"""
Схемы GraphQL
"""

import graphene
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType

from django.contrib.auth.models import User

from .models import Student, Teacher, Administrator, Course, CourseEntry, CourseAdmin, Lesson, UserAbstract


class UserType(DjangoObjectType):
    """
    Профиль
    """
    class Meta:
        model = User


class UserAbstractType(DjangoObjectType):
    """
    Пользователь
    """
    class Meta:
        model = UserAbstract


class StudentType(DjangoObjectType):
    """
    Студент
    """
    class Meta:
        model = Student


class TeacherType(DjangoObjectType):
    """
    Преподаватель
    """
    class Meta:
        model = Teacher


class AdministratorType(DjangoObjectType):
    """
    Администратор
    """
    class Meta:
        model = Administrator


class CourseType(DjangoObjectType):
    """
    Администратор
    """
    class Meta:
        model = Course


class CourseEntryType(DjangoObjectType):
    """
    Запись на курс
    """
    class Meta:
        model = CourseEntry


class CourseAdminType(DjangoObjectType):
    """
    Связь администратора с курсом
    """
    class Meta:
        model = CourseAdmin


class LessonType(DjangoObjectType):
    """
    Урок
    """
    class Meta:
        model = Lesson


class LessonMutation(graphene.Mutation):
    """
    Изменение урока
    """
    class Arguments:
        lesson_id = graphene.Int(required=True)
        new_name = graphene.String(required=True)

    result = graphene.Boolean()
    lesson = graphene.Field(LessonType)

    def mutate(self, info, lesson_id: int, new_name: str):
        """
        Изменение названия урока
        """
        lesson = get_object_or_404(Lesson, id=lesson_id)
        lesson.name = new_name
        lesson.save()
        return {
            'result': True,
            'lesson': lesson
        }


class Mutation:
    change_lesson_name = LessonMutation.Field()


def _get_all(model, *args, **kwargs):
    """ Возвращает список объектов с учетом навигации """
    if 'limit' in kwargs:
        return model.objects.all()[:kwargs['limit']]
    return model.objects.all()


def _get_one(model, *args, **kwargs):
    """ Возвращает один объект по идентификатору """
    if 'id' in kwargs:
        return model.objects.get(id=kwargs['id'])


class Query:
    all_teachers = graphene.List(TeacherType, limit=graphene.Int())
    teacher = graphene.Field(TeacherType, id=graphene.Int())

    all_students = graphene.List(StudentType, limit=graphene.Int())
    student = graphene.Field(StudentType, id=graphene.Int())

    all_administrators = graphene.List(AdministratorType, limit=graphene.Int())
    administrator = graphene.Field(AdministratorType, id=graphene.Int())

    all_courses = graphene.List(CourseType, limit=graphene.Int())
    course = graphene.Field(CourseType, id=graphene.Int())

    all_course_entries = graphene.List(CourseEntryType, limit=graphene.Int())
    course_entry = graphene.Field(CourseEntryType, id=graphene.Int())

    all_course_admins = graphene.List(CourseAdminType, limit=graphene.Int())
    course_admin = graphene.Field(CourseAdminType, id=graphene.Int())

    all_lessons = graphene.List(LessonType, limit=graphene.Int())
    lesson = graphene.Field(LessonType, id=graphene.Int())

    def resolve_all_teachers(self, *args, **kwargs):
        """ Преподаватели """
        return _get_all(Teacher, *args, **kwargs)

    def resolve_teacher(self, *args, **kwargs):
        """ Преподаватель """
        return _get_one(Teacher, *args, **kwargs)

    def resolve_all_students(self, *args, **kwargs):
        """ Студенты """
        return _get_all(Student, *args, **kwargs)

    def resolve_student(self, *args, **kwargs):
        """ Студент """
        return _get_one(Student, *args, **kwargs)

    def resolve_all_administrators(self, *args, **kwargs):
        """ Администраторы """
        return _get_all(Administrator, *args, **kwargs)

    def resolve_administrator(self, *args, **kwargs):
        """ Администратор """
        return _get_one(Administrator, *args, **kwargs)

    def resolve_all_courses(self, *args, **kwargs):
        """ Курсы """
        return _get_all(Course, *args, **kwargs)

    def resolve_course(self, *args, **kwargs):
        """ Курс """
        return _get_one(Course, *args, **kwargs)

    def resolve_all_course_entries(self, *args, **kwargs):
        """ Записи на курсы """
        return _get_all(CourseEntry, *args, **kwargs)

    def resolve_course_entry(self, *args, **kwargs):
        """ Запись на курс """
        return _get_one(CourseEntry, *args, **kwargs)

    def resolve_all_course_admins(self, *args, **kwargs):
        """ Связи администраторов с курсами """
        return _get_all(CourseAdmin, *args, **kwargs)

    def resolve_course_admin(self, *args, **kwargs):
        """ Связь администратора с курсом """
        return _get_one(CourseAdmin, *args, **kwargs)

    def resolve_all_lessons(self, *args, **kwargs):
        """ Уроки """
        return _get_all(Lesson, *args, **kwargs)

    def resolve_lesson(self, *args, **kwargs):
        """ Урок """
        return _get_one(Lesson, *args, **kwargs)
