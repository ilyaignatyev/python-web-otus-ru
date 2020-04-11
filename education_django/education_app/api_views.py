"""
Представления для API
"""

from rest_framework import viewsets

from .models import Teacher, Student, Administrator, Course, CourseEntry, CourseAdmin, Lesson
from .permissions import TeacherPermissions, StudentPermissions, AdministratorPermissions, CoursePermissions, \
    CourseEntryPermissions, CourseAdminPermissions, LessonPermissions
from .serializers import TeacherSerializer, TeacherCreateSerializer, TeacherUpdateSerializer, StudentSerializer, \
    StudentCreateSerializer, StudentUpdateSerializer, AdministratorSerializer, AdministratorCreateSerializer, \
    AdministratorUpdateSerializer, CourseSerializer, CourseEntrySerializer, CourseAdminSerializer, LessonSerializer


class APITeacherViewSet(viewsets.ModelViewSet):
    """
    Преподаватель
    """
    queryset = Teacher.objects.all()
    permission_classes = (TeacherPermissions,)

    def get_serializer_class(self):
        if self.action == 'create':
            return TeacherCreateSerializer
        elif self.action == 'partial_update':
            return TeacherUpdateSerializer
        return TeacherSerializer


class APIStudentViewSet(viewsets.ModelViewSet):
    """
    Студент
    """
    permission_classes = (StudentPermissions,)

    def get_serializer_class(self):
        if self.action == 'create':
            return StudentCreateSerializer
        elif self.action == 'partial_update':
            return StudentUpdateSerializer
        return StudentSerializer

    def get_queryset(self):
        return Student.objects.for_user_queryset(self.request.user)


class APIAdministratorViewSet(viewsets.ModelViewSet):
    """
    Админимтратор
    """
    permission_classes = (AdministratorPermissions,)

    def get_serializer_class(self):
        if self.action == 'create':
            return AdministratorCreateSerializer
        elif self.action == 'partial_update':
            return AdministratorUpdateSerializer
        return AdministratorSerializer

    def get_queryset(self):
        return Administrator.objects.for_user_queryset(self.request.user)


class APICourseViewSet(viewsets.ModelViewSet):
    """
    Курс
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (CoursePermissions,)


class APICourseEntryViewSet(viewsets.ModelViewSet):
    """
    Запись студента на курс
    """
    serializer_class = CourseEntrySerializer
    permission_classes = (CourseEntryPermissions,)

    def get_queryset(self):
        return CourseEntry.objects.for_user_queryset(self.request.user)


class APICourseAdminViewSet(viewsets.ModelViewSet):
    """
    Связь админитратора с курсом
    """
    serializer_class = CourseAdminSerializer
    permission_classes = (CourseAdminPermissions,)

    def get_queryset(self):
        return CourseAdmin.objects.for_user_queryset(self.request.user)


class APILessonViewSet(viewsets.ModelViewSet):
    """
    Урок
    """
    serializer_class = LessonSerializer
    permission_classes = (LessonPermissions,)

    def get_queryset(self):
        return Lesson.objects.for_user_queryset(self.request.user)
