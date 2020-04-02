"""
Представления для API
"""

from rest_framework import viewsets

from .models import Teacher, Student, Administrator, Course, CourseEntry, CourseAdmin, Lesson
from .permissions import TeacherPermissions, StudentPermissions, AdministratorPermissions, CoursePermissions, \
    CourseEntryPermissions, CourseAdminPermissions, LessonPermissions
from .serializers import TeacherSerializer, StudentSerializer, AdministratorSerializer, CourseSerializer, \
    CourseEntrySerializer, CourseAdminSerializer, LessonSerializer


class APITeacherViewSet(viewsets.ModelViewSet):
    """
    Преподаватель
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (TeacherPermissions,)


class APIStudentViewSet(viewsets.ModelViewSet):
    """
    Студент
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (StudentPermissions,)

    def get_queryset(self):
        return Student.objects.for_user_queryset(self.request.user)


class APIAdministratorViewSet(viewsets.ModelViewSet):
    """
    Администратор
    """
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer
    permission_classes = (AdministratorPermissions,)

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
    queryset = CourseEntry.objects.all()
    serializer_class = CourseEntrySerializer
    permission_classes = (CourseEntryPermissions,)

    def get_queryset(self):
        return CourseEntry.objects.for_user_queryset(self.request.user)


class APICourseAdminViewSet(viewsets.ModelViewSet):
    """
    Связь админитратора с курсом
    """
    queryset = CourseAdmin.objects.all()
    serializer_class = CourseAdminSerializer
    permission_classes = (CourseAdminPermissions,)

    def get_queryset(self):
        return CourseAdmin.objects.for_user_queryset(self.request.user)


class APILessonViewSet(viewsets.ModelViewSet):
    """
    Урок
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (LessonPermissions,)
