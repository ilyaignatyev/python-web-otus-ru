"""
Сериализаторы
"""

from rest_framework import serializers

from .models import Course, Teacher, Administrator, Student, CourseEntry, CourseAdmin, Lesson


class TeacherSerializer(serializers.ModelSerializer):
    """
    Преподаватель
    """
    class Meta:
        model = Teacher
        fields = 'id', 'user', 'about'


class StudentSerializer(serializers.ModelSerializer):
    """
    Студент
    """
    class Meta:
        model = Student
        fields = 'id', 'user', 'about'


class AdministratorSerializer(serializers.ModelSerializer):
    """
    Администратор
    """
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
