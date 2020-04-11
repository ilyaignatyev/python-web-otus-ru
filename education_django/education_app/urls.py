"""
Роутинг
"""
from django.urls import path, include
from rest_framework import routers

from .api_views import APITeacherViewSet, APIStudentViewSet, APIAdministratorViewSet, APICourseViewSet, \
    APICourseEntryViewSet, APICourseAdminViewSet, APILessonViewSet
from .views import CourseView, CourseListView, CourseCreateView, CourseUpdateView, CourseDeleteView, \
    MyCourseListView, TeacherListView, TeacherView, StudentView, CourseEntryCreateView, \
    CourseEntryUpdateView, CourseEntryDeleteView, LessonCreateView, LessonUpdateView, LessonDeleteView, \
    create_my_course_entry, CourseAdminCreateView, CourseAdminUpdateView, CourseAdminDeleteView, AdministratorView, \
    MyCourseEntryDeleteView, LessonView, AboutView, ContactsView, EmailSentView

app_name = 'education_app'

api_router = routers.DefaultRouter()
api_router.register(r'teacher', APITeacherViewSet, 'Teacher')
api_router.register(r'student', APIStudentViewSet, 'Student')
api_router.register(r'administrator', APIAdministratorViewSet, 'Administrator')
api_router.register(r'course', APICourseViewSet, 'Course')
api_router.register(r'courseentry', APICourseEntryViewSet, 'CourseEntry')
api_router.register(r'courseadmin', APICourseAdminViewSet, 'CourseAdmin')
api_router.register(r'lesson', APILessonViewSet, 'Lesson')

urlpatterns = [
    path('', CourseListView.as_view(), name='index'),
    path('my_courses/', MyCourseListView.as_view(), name='my_courses'),

    path('course/<int:id>/', CourseView.as_view(), name='course'),
    path('course/create/', CourseCreateView.as_view(), name='create_course'),
    path('course/update/<int:id>/', CourseUpdateView.as_view(), name='update_course'),
    path('course/delete/<int:id>/', CourseDeleteView.as_view(), name='delete_course'),

    path('teachers/', TeacherListView.as_view(), name='teachers'),
    path('teacher/<int:id>/', TeacherView.as_view(), name='teacher'),

    path('student/<int:id>/', StudentView.as_view(), name='student'),

    path('about/', AboutView.as_view(), name='about'),

    path('course_entry/create/course/<int:id>', CourseEntryCreateView.as_view(), name='create_course_entry'),
    path('course_entry/create_my/course/<int:id>', create_my_course_entry, name='create_my_course_entry'),
    path('course_entry/delete_my/course/<int:id>', MyCourseEntryDeleteView.as_view(), name='delete_my_course_entry'),
    path('course_entry/update/<int:id>/', CourseEntryUpdateView.as_view(), name='update_course_entry'),
    path('course_entry/delete/<int:id>/', CourseEntryDeleteView.as_view(), name='delete_course_entry'),

    path('lesson/<int:id>/', LessonView.as_view(), name='lesson'),
    path('lesson/create/course/<int:id>/', LessonCreateView.as_view(), name='create_lesson'),
    path('lesson/update/<int:id>/', LessonUpdateView.as_view(), name='update_lesson'),
    path('lesson/delete/<int:id>/', LessonDeleteView.as_view(), name='delete_lesson'),

    path('administrator/<int:id>', AdministratorView.as_view(), name='administrator'),

    path('course_admin/create/course/<int:id>', CourseAdminCreateView.as_view(), name='create_course_admin'),
    path('course_admin/update/<int:id>/', CourseAdminUpdateView.as_view(), name='update_course_admin'),
    path('course_admin/delete/<int:id>/', CourseAdminDeleteView.as_view(), name='delete_course_admin'),

    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('email_sent/', EmailSentView.as_view(), name='email_sent'),

    path('api/', include(api_router.urls))
]
