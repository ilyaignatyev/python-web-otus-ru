"""
Админка
"""

from django.contrib import admin

from education_app.models import CourseAdmin, Administrator
from .models import Course, Lesson, Teacher, Student, CourseEntry


@admin.register(Teacher)
class TeacherAdministration(admin.ModelAdmin):
    """
    Администрирование учителей
    """
    list_display = ('id', 'user', 'about')
    list_display_links = ('user',)


@admin.register(Student)
class StudentAdministration(admin.ModelAdmin):
    """
    Администрирование студентов
    """
    list_display = ('id', 'user', 'about')
    list_display_links = ('user',)


@admin.register(Administrator)
class AdministratorAdministration(admin.ModelAdmin):
    """
    Администрирование студентов
    """
    list_display = ('id', 'user', 'about')
    list_display_links = ('user',)


@admin.register(Course)
class CourseAdministration(admin.ModelAdmin):
    """
    Администрирование курсов
    """
    list_display = ('id', 'name', 'description', 'start')
    list_display_links = ('name',)


@admin.register(CourseEntry)
class CourseEntryAdministration(admin.ModelAdmin):
    """
    Администрирование записей на курс
    """
    list_display = ('id', 'student', 'course', 'date', 'cost', 'paid')
    list_display_links = ('student', 'course')


@admin.register(CourseAdmin)
class CourseAdminAdministration(admin.ModelAdmin):
    """
    Администрирование записей на курс
    """
    list_display = ('id', 'course', 'admin', 'start')
    list_display_links = ('id',)


@admin.register(Lesson)
class LessonAdministration(admin.ModelAdmin):
    """
    Администрирование уроков
    """
    list_display = ('id', 'course', 'name', 'description', 'start', 'teacher')
    list_display_links = ('name', 'description')
