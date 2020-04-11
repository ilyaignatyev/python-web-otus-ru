"""
Тесты API
"""

import datetime

from django.contrib.auth.models import User
from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APISimpleTestCase, APITransactionTestCase, \
    force_authenticate

from .api_views import APITeacherViewSet, APIStudentViewSet, APIAdministratorViewSet, APICourseViewSet, \
    APICourseEntryViewSet, APICourseAdminViewSet, APILessonViewSet
from .factories import TeacherFactory, StudentFactory, AdministratorFactory, CourseFactory, CourseEntryFactory, \
    CourseAdminFactory, LessonFactory
from .models import Teacher, Student, Administrator, Course, CourseEntry, CourseAdmin, Lesson
from .tasks import send_email


class TeacherTestCase(APITestCase):
    """
    Тесты преподавателей
    """
    @classmethod
    def setUpTestData(cls):
        """
        Данные для тесткейса
        """
        cls.endpoint = '/api/teacher/'
        cls.superuser = User.objects.create_superuser(username='superuser', password='password',
                                                      email='superuser@gmail.com')

    def test_teacher_list(self):
        """
        Список преподавателей
        """
        teacher1 = TeacherFactory(user__username='teacher1', user__first_name='Name1', user__last_name='Surname1',
                                  about='About teacher1')
        teacher2 = TeacherFactory(user__username='teacher2', user__first_name='Name2', user__last_name='Surname2',
                                  about='About teacher2')
        request = APIRequestFactory().get(self.endpoint)
        force_authenticate(request, user=self.superuser)
        teacher_view = APITeacherViewSet.as_view({'get': 'list'})
        response = teacher_view(request)
        self.assertEqual(len(response.data), 2)

        teacher1_data = response.data[0]
        teacher1_user_data = teacher1_data['user']
        self.assertEqual(teacher1_data.get('id'), teacher1.id)
        self.assertEqual(teacher1_user_data.get('id'), teacher1.user.id)
        self.assertEqual(teacher1_user_data.get('username'), 'teacher1')
        self.assertEqual(teacher1_user_data.get('first_name'), 'Name1')
        self.assertEqual(teacher1_user_data.get('last_name'), 'Surname1')
        self.assertEqual(teacher1_data.get('about'), 'About teacher1')

        teacher2_data = response.data[1]
        teacher2_user_data = teacher2_data['user']
        self.assertEqual(teacher2_data.get('id'), teacher2.id)
        self.assertEqual(teacher2_user_data.get('id'), teacher2.user.id)
        self.assertEqual(teacher2_user_data.get('username'), 'teacher2')
        self.assertEqual(teacher2_user_data.get('first_name'), 'Name2')
        self.assertEqual(teacher2_user_data.get('last_name'), 'Surname2')
        self.assertEqual(teacher2_data.get('about'), 'About teacher2')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_teacher(self):
        """
        Получение преподавателя
        """
        teacher = TeacherFactory(user__username='teacher', user__first_name='Name', user__last_name='Surname',
                                 about='About teacher')
        request = APIRequestFactory().get(f'{self.endpoint}{teacher.id}/')
        force_authenticate(request, user=self.superuser)
        teacher_view = APITeacherViewSet.as_view({'get': 'retrieve'})
        response = teacher_view(request, pk=teacher.id)

        teacher_data = response.data
        teacher_user_data = teacher_data['user']
        self.assertEqual(teacher_data.get('id'), teacher.id)
        self.assertEqual(teacher_user_data.get('id'), teacher.user.id)
        self.assertEqual(teacher_user_data.get('username'), 'teacher')
        self.assertEqual(teacher_user_data.get('first_name'), 'Name')
        self.assertEqual(teacher_user_data.get('last_name'), 'Surname')
        self.assertEqual(teacher_data.get('about'), 'About teacher')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_teacher(self):
        """
        Создание преподавателя
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.endpoint, {
            "user": {
                "username": "teacher",
                "first_name": "Name",
                "last_name": "Surname",
                "password": "password",
                "email": "email@mail.ru"
            },
            "about": "About teacher"
        }, format='json')

        teacher_data = response.data
        teacher_user_data = teacher_data['user']
        self.assertEqual(teacher_user_data.get('username'), 'teacher')
        self.assertEqual(teacher_user_data.get('first_name'), 'Name')
        self.assertEqual(teacher_user_data.get('last_name'), 'Surname')
        self.assertEqual(teacher_user_data.get('email'), 'email@mail.ru')
        self.assertEqual(teacher_data.get('about'), 'About teacher')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_teacher(self):
        """
        Удаление преподавателя
        """
        teacher = TeacherFactory(user__username='teacher', user__first_name='Name', user__last_name='Surname',
                                 about='About teacher')
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(f'{self.endpoint}{teacher.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Teacher.DoesNotExist):
            Teacher.objects.get(id=teacher.id)


class StudentTestCase(APITestCase):
    """
    Тесты студентов
    """
    @classmethod
    def setUpTestData(cls):
        """
        Данные для тесткейса
        """
        cls.endpoint = '/api/student/'
        cls.superuser = User.objects.create_superuser(username='superuser', password='password',
                                                      email='superuser@gmail.com')

    def test_student_list(self):
        """
        Список студентов
        """
        student1 = StudentFactory(user__username='student1', user__first_name='Name1', user__last_name='Surname1',
                                  about='About student1')
        student2 = StudentFactory(user__username='student2', user__first_name='Name2', user__last_name='Surname2',
                                  about='About student2')
        request = APIRequestFactory().get(self.endpoint)
        force_authenticate(request, user=self.superuser)
        student_view = APIStudentViewSet.as_view({'get': 'list'})
        response = student_view(request)
        self.assertEqual(len(response.data), 2)

        student1_data = response.data[0]
        student1_user_data = student1_data['user']
        self.assertEqual(student1_data.get('id'), student1.id)
        self.assertEqual(student1_user_data.get('id'), student1.user.id)
        self.assertEqual(student1_user_data.get('username'), 'student1')
        self.assertEqual(student1_user_data.get('first_name'), 'Name1')
        self.assertEqual(student1_user_data.get('last_name'), 'Surname1')
        self.assertEqual(student1_data.get('about'), 'About student1')

        student2_data = response.data[1]
        student2_user_data = student2_data['user']
        self.assertEqual(student2_data.get('id'), student2.id)
        self.assertEqual(student2_user_data.get('id'), student2.user.id)
        self.assertEqual(student2_user_data.get('username'), 'student2')
        self.assertEqual(student2_user_data.get('first_name'), 'Name2')
        self.assertEqual(student2_user_data.get('last_name'), 'Surname2')
        self.assertEqual(student2_data.get('about'), 'About student2')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_student(self):
        """
        Получение студента
        """
        student = StudentFactory(user__username='student', user__first_name='Name', user__last_name='Surname',
                                 about='About student')
        request = APIRequestFactory().get(f'{self.endpoint}{student.id}/')
        force_authenticate(request, user=self.superuser)
        student_view = APIStudentViewSet.as_view({'get': 'retrieve'})
        response = student_view(request, pk=student.id)

        student_data = response.data
        student_user_data = student_data['user']
        self.assertEqual(student_data.get('id'), student.id)
        self.assertEqual(student_user_data.get('id'), student.user.id)
        self.assertEqual(student_user_data.get('username'), 'student')
        self.assertEqual(student_user_data.get('first_name'), 'Name')
        self.assertEqual(student_user_data.get('last_name'), 'Surname')
        self.assertEqual(student_data.get('about'), 'About student')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_student(self):
        """
        Создание студента
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.endpoint, {
            "user": {
                "username": "student",
                "first_name": "Name",
                "last_name": "Surname",
                "password": "password",
                "email": "email@mail.ru"
            },
            "about": "About student"
        }, format='json')

        student_data = response.data
        student_user_data = student_data['user']
        self.assertEqual(student_user_data.get('username'), 'student')
        self.assertEqual(student_user_data.get('first_name'), 'Name')
        self.assertEqual(student_user_data.get('last_name'), 'Surname')
        self.assertEqual(student_user_data.get('email'), 'email@mail.ru')
        self.assertEqual(student_data.get('about'), 'About student')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_student(self):
        """
        Удаление студента
        """
        student = StudentFactory(user__username='student', user__first_name='Name', user__last_name='Surname',
                                 about='About student')
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(f'{self.endpoint}{student.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(id=student.id)


class AdministratorTestCase(APITestCase):
    """
    Тесты администраторов
    """
    @classmethod
    def setUpTestData(cls):
        """
        Данные для тесткейса
        """
        cls.endpoint = '/api/administrator/'
        cls.superuser = User.objects.create_superuser(username='superuser', password='password',
                                                      email='superuser@gmail.com')

    def test_administrator_list(self):
        """
        Список администраторов
        """
        administrator1 = AdministratorFactory(user__username='administrator1', user__first_name='Name1',
                                              user__last_name='Surname1', about='About administrator1')
        administrator2 = AdministratorFactory(user__username='administrator2', user__first_name='Name2',
                                              user__last_name='Surname2', about='About administrator2')
        request = APIRequestFactory().get(self.endpoint)
        force_authenticate(request, user=self.superuser)
        administrator_view = APIAdministratorViewSet.as_view({'get': 'list'})
        response = administrator_view(request)
        self.assertEqual(len(response.data), 2)

        administrator1_data = response.data[0]
        administrator1_user_data = administrator1_data['user']
        self.assertEqual(administrator1_data.get('id'), administrator1.id)
        self.assertEqual(administrator1_user_data.get('id'), administrator1.user.id)
        self.assertEqual(administrator1_user_data.get('username'), 'administrator1')
        self.assertEqual(administrator1_user_data.get('first_name'), 'Name1')
        self.assertEqual(administrator1_user_data.get('last_name'), 'Surname1')
        self.assertEqual(administrator1_data.get('about'), 'About administrator1')

        administrator2_data = response.data[1]
        administrator2_user_data = administrator2_data['user']
        self.assertEqual(administrator2_data.get('id'), administrator2.id)
        self.assertEqual(administrator2_user_data.get('id'), administrator2.user.id)
        self.assertEqual(administrator2_user_data.get('username'), 'administrator2')
        self.assertEqual(administrator2_user_data.get('first_name'), 'Name2')
        self.assertEqual(administrator2_user_data.get('last_name'), 'Surname2')
        self.assertEqual(administrator2_data.get('about'), 'About administrator2')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_administrator(self):
        """
        Получение администратора
        """
        administrator = AdministratorFactory(user__username='administrator', user__first_name='Name',
                                             user__last_name='Surname', about='About administrator')
        request = APIRequestFactory().get(f'{self.endpoint}{administrator.id}/')
        force_authenticate(request, user=self.superuser)
        administrator_view = APIAdministratorViewSet.as_view({'get': 'retrieve'})
        response = administrator_view(request, pk=administrator.id)

        administrator_data = response.data
        administrator_user_data = administrator_data['user']
        self.assertEqual(administrator_data.get('id'), administrator.id)
        self.assertEqual(administrator_user_data.get('id'), administrator.user.id)
        self.assertEqual(administrator_user_data.get('username'), 'administrator')
        self.assertEqual(administrator_user_data.get('first_name'), 'Name')
        self.assertEqual(administrator_user_data.get('last_name'), 'Surname')
        self.assertEqual(administrator_data.get('about'), 'About administrator')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_administrator(self):
        """
        Создание администратора
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.endpoint, {
            "user": {
                "username": "administrator",
                "first_name": "Name",
                "last_name": "Surname",
                "password": "password",
                "email": "email@mail.ru"
            },
            "about": "About administrator"
        }, format='json')

        administrator_data = response.data
        administrator_user_data = administrator_data['user']
        self.assertEqual(administrator_user_data.get('username'), 'administrator')
        self.assertEqual(administrator_user_data.get('first_name'), 'Name')
        self.assertEqual(administrator_user_data.get('last_name'), 'Surname')
        self.assertEqual(administrator_user_data.get('email'), 'email@mail.ru')
        self.assertEqual(administrator_data.get('about'), 'About administrator')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_administrator(self):
        """
        Удаление администратора
        """
        administrator = AdministratorFactory(user__username='administrator', user__first_name='Name',
                                             user__last_name='Surname', about='About administrator')
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(f'{self.endpoint}{administrator.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Administrator.DoesNotExist):
            Administrator.objects.get(id=administrator.id)


class CourseTestCase(APITestCase):
    """
    Тесты курсов
    """
    @classmethod
    def setUpTestData(cls):
        """
        Данные для тесткейса
        """
        cls.endpoint = '/api/course/'
        cls.superuser = User.objects.create_superuser(username='superuser', password='password',
                                                      email='superuser@gmail.com')

    def test_course_list(self):
        """
        Список курсов
        """
        course1 = CourseFactory(name='Course1', description='Description1', start='2020-01-05', cost=5000,
                                deleted=False)
        course2 = CourseFactory(name='Course2', description='Description2', start='2020-01-05', cost=6000,
                                deleted=True)
        request = APIRequestFactory().get(self.endpoint)
        force_authenticate(request, user=self.superuser)
        course_view = APICourseViewSet.as_view({'get': 'list'})
        response = course_view(request)
        self.assertEqual(len(response.data), 2)

        course1_data = response.data[0]
        self.assertEqual(course1_data.get('id'), course1.id)
        self.assertEqual(course1_data.get('name'), 'Course1')
        self.assertEqual(course1_data.get('description'), 'Description1')
        self.assertEqual(course1_data.get('start'), '2020-01-05')
        self.assertEqual(course1_data.get('cost'), 5000)
        self.assertEqual(course1_data.get('deleted'), False)

        course2_data = response.data[1]
        self.assertEqual(course2_data.get('id'), course2.id)
        self.assertEqual(course2_data.get('name'), 'Course2')
        self.assertEqual(course2_data.get('description'), 'Description2')
        self.assertEqual(course2_data.get('start'), '2020-01-05')
        self.assertEqual(course2_data.get('cost'), 6000)
        self.assertEqual(course2_data.get('deleted'), True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_course(self):
        """
        Получение курса
        """
        course = CourseFactory(name='Course', description='Description', start='2020-01-05', cost=5000, deleted=False)
        request = APIRequestFactory().get(f'{self.endpoint}{course.id}/')
        force_authenticate(request, user=self.superuser)
        course_view = APICourseViewSet.as_view({'get': 'retrieve'})
        response = course_view(request, pk=course.id)

        course_data = response.data
        self.assertEqual(course_data.get('id'), course.id)
        self.assertEqual(course_data.get('name'), 'Course')
        self.assertEqual(course_data.get('description'), 'Description')
        self.assertEqual(course_data.get('start'), '2020-01-05')
        self.assertEqual(course_data.get('cost'), 5000)
        self.assertEqual(course_data.get('deleted'), False)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course(self):
        """
        Создание курса
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.endpoint, {
            "name": "Course",
            "description": "Description",
            "start": '2020-01-05',
            "cost": 5000,
            "deleted": False
        }, format='json')

        course_data = response.data
        self.assertEqual(course_data.get('name'), 'Course')
        self.assertEqual(course_data.get('description'), 'Description')
        self.assertEqual(course_data.get('start'), '2020-01-05')
        self.assertEqual(course_data.get('cost'), 5000)
        self.assertEqual(course_data.get('deleted'), False)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_course(self):
        """
        Удаление курса
        """
        course = CourseFactory(name='Course', description='Description', start='2020-01-05', cost=5000, deleted=False)
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(f'{self.endpoint}{course.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(id=course.id)


class CourseEntryTestCase(APITestCase):
    """
    Тесты записей на курс
    """
    @classmethod
    def setUpTestData(cls):
        """
        Данные для тесткейса
        """
        cls.endpoint = '/api/courseentry/'
        cls.course = CourseFactory(name='Course', description='Description', start='2020-01-05', cost=5000,
                                   deleted=False)
        cls.student = StudentFactory(user__username='student', user__first_name='Name', user__last_name='Surname',
                                     about='About student')
        cls.superuser = User.objects.create_superuser(username='superuser', password='password',
                                                      email='superuser@gmail.com')

    def test_course_entry_list(self):
        """
        Список записей на курс
        """
        course_entry = CourseEntryFactory(student=self.student, course=self.course, cost=5000, paid=True)
        request = APIRequestFactory().get(self.endpoint)
        force_authenticate(request, user=self.superuser)
        course_entry_view = APICourseEntryViewSet.as_view({'get': 'list'})
        response = course_entry_view(request)
        self.assertEqual(len(response.data), 1)

        course_entry_data = response.data[0]
        self.assertEqual(course_entry_data.get('id'), course_entry.id)
        self.assertEqual(course_entry_data.get('student'), self.student.id)
        self.assertEqual(course_entry_data.get('course'), self.course.id)
        self.assertEqual(course_entry_data.get('cost'), 5000)
        self.assertEqual(course_entry_data.get('paid'), True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_course_entry(self):
        """
        Получение записи на курс
        """
        course_entry = CourseEntryFactory(student=self.student, course=self.course, cost=5000, paid=True)
        request = APIRequestFactory().get(f'{self.endpoint}{course_entry.id}/')
        force_authenticate(request, user=self.superuser)
        course_entry_view = APICourseEntryViewSet.as_view({'get': 'retrieve'})
        response = course_entry_view(request, pk=course_entry.id)

        course_entry_data = response.data
        self.assertEqual(course_entry_data.get('id'), course_entry.id)
        self.assertEqual(course_entry_data.get('student'), self.student.id)
        self.assertEqual(course_entry_data.get('course'), self.course.id)
        self.assertEqual(course_entry_data.get('cost'), 5000)
        self.assertEqual(course_entry_data.get('paid'), True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course_entry(self):
        """
        Создание записи на курс
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.endpoint, {
            "student": self.student.id,
            "course": self.course.id,
            "cost": 5000,
            "paid": True
        }, format='json')

        course_entry_data = response.data
        self.assertEqual(course_entry_data.get('student'), self.student.id)
        self.assertEqual(course_entry_data.get('course'), self.course.id)
        self.assertEqual(course_entry_data.get('cost'), 5000)
        self.assertEqual(course_entry_data.get('paid'), True)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_course(self):
        """
        Удаление записи на курс
        """
        course_entry = CourseEntryFactory(student=self.student, course=self.course, cost=5000, paid=True)
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(f'{self.endpoint}{course_entry.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(CourseEntry.DoesNotExist):
            CourseEntry.objects.get(id=course_entry.id)


class CourseAdminTestCase(APITestCase):
    """
    Тесты свзи администратора с курсом
    """
    @classmethod
    def setUpTestData(cls):
        """
        Данные для тесткейса
        """
        cls.endpoint = '/api/courseadmin/'
        cls.course = CourseFactory(name='Course', description='Description', start='2020-01-05', cost=5000,
                                   deleted=False)
        cls.administrator = AdministratorFactory(user__username='administrator', user__first_name='Name',
                                                 user__last_name='Surname', about='About administrator')
        cls.superuser = User.objects.create_superuser(username='superuser', password='password',
                                                      email='superuser@gmail.com')

    def test_course_admin_list(self):
        """
        Список связей администраторов с курсами
        """
        course_admin = CourseAdminFactory(admin=self.administrator, course=self.course, start='2020-01-05')
        request = APIRequestFactory().get(self.endpoint)
        force_authenticate(request, user=self.superuser)
        course_admin_view = APICourseAdminViewSet.as_view({'get': 'list'})
        response = course_admin_view(request)
        self.assertEqual(len(response.data), 1)

        course_entry_data = response.data[0]
        self.assertEqual(course_entry_data.get('id'), course_admin.id)
        self.assertEqual(course_entry_data.get('admin'), self.administrator.id)
        self.assertEqual(course_entry_data.get('course'), self.course.id)
        self.assertEqual(course_entry_data.get('start'), '2020-01-05')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_course_admin(self):
        """
        Получение связи администратора с курсом
        """
        course_admin = CourseAdminFactory(admin=self.administrator, course=self.course, start='2020-01-05')
        request = APIRequestFactory().get(f'{self.endpoint}{course_admin.id}/')
        force_authenticate(request, user=self.superuser)
        course_admin_view = APICourseAdminViewSet.as_view({'get': 'retrieve'})
        response = course_admin_view(request, pk=course_admin.id)

        course_entry_data = response.data
        self.assertEqual(course_entry_data.get('id'), course_admin.id)
        self.assertEqual(course_entry_data.get('admin'), self.administrator.id)
        self.assertEqual(course_entry_data.get('course'), self.course.id)
        self.assertEqual(course_entry_data.get('start'), '2020-01-05')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course_admin(self):
        """
        Создание связи администратора с курсом
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.endpoint, {
            "admin": self.administrator.id,
            "course": self.course.id,
            "start": '2020-01-05',
        }, format='json')

        course_entry_data = response.data
        self.assertEqual(course_entry_data.get('admin'), self.administrator.id)
        self.assertEqual(course_entry_data.get('course'), self.course.id)
        self.assertEqual(course_entry_data.get('start'), '2020-01-05')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_course_admin(self):
        """
        Удаление связи администратора с курсом
        """
        course_admin = CourseAdminFactory(admin=self.administrator, course=self.course, start='2020-01-05')
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(f'{self.endpoint}{course_admin.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(CourseAdmin.DoesNotExist):
            CourseAdmin.objects.get(id=course_admin.id)


class LessonTestCase(APITransactionTestCase):
    """
    Тесты свзи администратора с курсом
    """
    @classmethod
    def setUpClass(cls):
        """
        Данные для тесткейса
        """
        super(LessonTestCase, cls).setUpClass()
        cls.endpoint = '/api/lesson/'

    def setUp(self):
        """
        Данные для каждого теста
        """
        self.course = CourseFactory(name='Course', description='Description', start='2020-01-05', cost=5000,
                                    deleted=False)
        self.teacher = TeacherFactory(user__username='teacher', user__first_name='Name', user__last_name='Surname',
                                      about='About teacher')
        self.superuser = User.objects.create_superuser(username='superuser', password='password',
                                                       email='superuser@gmail.com')

    def test_lesson_list(self):
        """
        Список уроков
        """
        lesson = LessonFactory(name='Name', teacher=self.teacher, course=self.course,
                               start=datetime.datetime(2020, 11, 1, 19, 0, 0))
        request = APIRequestFactory().get(self.endpoint)
        force_authenticate(request, user=self.superuser)
        lesson_view = APILessonViewSet.as_view({'get': 'list'})
        response = lesson_view(request)
        self.assertEqual(len(response.data), 1)

        lesson_data = response.data[0]
        self.assertEqual(lesson_data.get('id'), lesson.id)
        self.assertEqual(lesson_data.get('name'), 'Name')
        self.assertEqual(lesson_data.get('teacher'), self.teacher.id)
        self.assertEqual(lesson_data.get('course'), self.course.id)
        self.assertEqual(lesson_data.get('start'), '2020-11-01T19:00:00Z')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lesson_admin(self):
        """
        Получение урока
        """
        lesson = LessonFactory(name='Name', teacher=self.teacher, course=self.course,
                               start=datetime.datetime(2020, 11, 1, 19, 0, 0))
        request = APIRequestFactory().get(f'{self.endpoint}{lesson.id}/')
        force_authenticate(request, user=self.superuser)
        lesson_view = APILessonViewSet.as_view({'get': 'retrieve'})
        response = lesson_view(request, pk=lesson.id)

        lesson_data = response.data
        self.assertEqual(lesson_data.get('id'), lesson.id)
        self.assertEqual(lesson_data.get('name'), 'Name')
        self.assertEqual(lesson_data.get('teacher'), self.teacher.id)
        self.assertEqual(lesson_data.get('course'), self.course.id)
        self.assertEqual(lesson_data.get('start'), '2020-11-01T19:00:00Z')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_lesson(self):
        """
        Создание урока
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(self.endpoint, {
            "name": 'Name',
            "teacher": self.teacher.id,
            "course": self.course.id,
            "start": '2020-11-01T19:00:00Z',
        }, format='json')

        lesson_data = response.data
        self.assertEqual(lesson_data.get('name'), 'Name')
        self.assertEqual(lesson_data.get('teacher'), self.teacher.id)
        self.assertEqual(lesson_data.get('course'), self.course.id)
        self.assertEqual(lesson_data.get('start'), '2020-11-01T19:00:00Z')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_lesson(self):
        """
        Удаление урока
        """
        lesson = LessonFactory(name='Name', teacher=self.teacher, course=self.course,
                               start=datetime.datetime(2020, 11, 1, 19, 0, 0))
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(f'{self.endpoint}{lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Lesson.DoesNotExist):
            Lesson.objects.get(id=lesson.id)


class EmailTestCase(APISimpleTestCase):
    """
    Тест отправки email
    """
    def test_send_email(self):
        """
        Тест отправки email
        """
        send_email('theme', 'message', 'from@gmail.com', ['to@gmail.com'])

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'theme')
        self.assertEqual(mail.outbox[0].body, 'message')
        self.assertEqual(mail.outbox[0].from_email, 'from@gmail.com')
        self.assertEqual(mail.outbox[0].to, ['to@gmail.com'])
