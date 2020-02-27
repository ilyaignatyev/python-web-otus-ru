"""
Админка
"""

from django.contrib import admin

from .models import Course, User, Lesson, Teacher, Student, CourseEntry


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Администрирование пользователей
    """
    list_display = ('id', 'name', 'surname', 'joined')
    list_display_links = ('name',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """
    Администрирование учителей
    """
    list_display = ('id', 'name', 'surname', 'joined', 'resume')
    list_display_links = ('name',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Администрирование студентов
    """
    list_display = ('id', 'name', 'surname', 'joined', 'resume')
    list_display_links = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Администрирование курсов
    """
    list_display = ('id', 'name', 'description', 'start')
    list_display_links = ('name',)


@admin.register(CourseEntry)
class CourseEntryAdmin(admin.ModelAdmin):
    """
    Администрирование записей на курс
    """
    list_display = ('id', 'student', 'course', 'date', 'cost', 'paid')
    list_display_links = ('student', 'course')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Администрирование уроков
    """
    list_display = ('id', 'course', 'name', 'description', 'start', 'teacher')
    list_display_links = ('name', 'description')
