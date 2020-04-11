"""
Сериализаторы
"""
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .const import USER_TYPE
from .models import Course, Teacher, Administrator, Student, CourseEntry, CourseAdmin, Lesson
from .users import create_user, update_user


class UserSerializer(serializers.ModelSerializer):
    """
    Пользователель
    """
    class Meta:
        model = User
        fields = 'id', 'username', 'first_name', 'last_name'


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Пользователель, для создания
    """
    class Meta:
        model = User
        fields = 'username', 'first_name', 'last_name', 'email', 'password'


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Пользователель, для записи
    """
    class Meta:
        model = User
        fields = 'id', 'username', 'first_name', 'last_name', 'email', 'password'

        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }


class UserCreateMixin:
    """
    Миксин для создания преподавателя/студента/администратора
    """

    def create(self, validated_data: dict) -> Teacher:
        """
        Создание
        :param validated_data: Данные
        :return: Преподаватель
        """
        profile_data = validated_data.pop('user')
        return create_user(profile_data, validated_data, model=self.Meta.model)


class UserUpdateMixin:
    """
    Миксин для редактирования преподавателя/студента/администратора
    """

    def update(self, instance: Teacher, validated_data: dict) -> Teacher:
        """
        Редактирование
        :param instance: Преподаватель
        :param validated_data: Данные
        :return:
        """
        profile_data = validated_data.pop('user')
        return update_user(instance, profile_data, validated_data)


class TeacherSerializer(serializers.ModelSerializer):
    """
    Преподаватель
    """
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = 'id', 'user', 'user_id', 'about'


class TeacherCreateSerializer(UserCreateMixin, serializers.ModelSerializer):
    """
    Преподаватель, создание
    """
    user = UserCreateSerializer()

    class Meta:
        model = Teacher
        fields = 'user', 'about'


class TeacherUpdateSerializer(UserUpdateMixin, serializers.ModelSerializer):
    """
    Преподаватель, редактирование
    """
    user = UserUpdateSerializer()

    class Meta:
        model = Teacher
        fields = 'id', 'user', 'about'


class StudentSerializer(serializers.ModelSerializer):
    """
    Студент
    """
    user = UserSerializer()

    class Meta:
        model = Student
        fields = 'id', 'user', 'user_id', 'about'


class StudentCreateSerializer(UserCreateMixin, serializers.ModelSerializer):
    """
    Студент, создание
    """
    user = UserCreateSerializer()

    class Meta:
        model = Student
        fields = 'user', 'about'


class StudentUpdateSerializer(UserUpdateMixin, serializers.ModelSerializer):
    """
    Студент, редактирование
    """
    user = UserUpdateSerializer()

    class Meta:
        model = Student
        fields = 'id', 'user', 'about'


class AdministratorSerializer(serializers.ModelSerializer):
    """
    Администратор
    """
    user = UserSerializer()

    class Meta:
        model = Administrator
        fields = 'id', 'user', 'user_id', 'about'


class AdministratorCreateSerializer(UserCreateMixin, serializers.ModelSerializer):
    """
    Администратор, создание
    """
    user = UserCreateSerializer()

    class Meta:
        model = Administrator
        fields = 'user', 'about'


class AdministratorUpdateSerializer(UserUpdateMixin, serializers.ModelSerializer):
    """
    Администратор, редактирование
    """
    user = UserUpdateSerializer()

    class Meta:
        model = Administrator
        fields = 'id', 'user', 'about'


class CourseSerializer(serializers.ModelSerializer):
    """
    Курс
    """
    class Meta:
        model = Course
        fields = 'id', 'name', 'description', 'start', 'cost', 'admins', 'students', 'deleted'


class CourseEntrySerializer(serializers.ModelSerializer):
    """
    Запись студента на курс
    """
    class Meta:
        model = CourseEntry
        fields = 'id', 'student', 'course', 'date', 'cost', 'paid'


class CourseAdminSerializer(serializers.ModelSerializer):
    """
    Администратор курса
    """
    class Meta:
        model = CourseAdmin
        fields = 'id', 'course', 'admin', 'start'


class LessonSerializer(serializers.ModelSerializer):
    """
    Урок
    """
    class Meta:
        model = Lesson
        fields = 'id', 'course', 'name', 'description', 'start', 'teacher'
