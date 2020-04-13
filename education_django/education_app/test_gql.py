"""
Тесты GraphQL
"""

import datetime
import json

from graphene_django.utils import GraphQLTestCase

from education_django import schema

from .factories import TeacherFactory, StudentFactory, AdministratorFactory, CourseFactory, CourseEntryFactory, \
    CourseAdminFactory, LessonFactory


class GQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    @classmethod
    def setUpTestData(cls):
        """
        Данные для тесткейса
        """
        cls.course = CourseFactory(name='Course', description='Description', start='2020-01-05', cost=5000,
                                   deleted=False)
        cls.student = StudentFactory(user__username='student', user__first_name='Name', user__last_name='Surname',
                                     about='About student')
        cls.teacher = TeacherFactory(user__username='teacher', user__first_name='Name', user__last_name='Surname',
                                     about='About teacher')
        cls.administrator = AdministratorFactory(user__username='administrator', user__first_name='Name',
                                                 user__last_name='Surname', about='About administrator')
        cls.course_entry = CourseEntryFactory(student=cls.student, course=cls.course, cost=5000, paid=True)
        cls.course_admin = CourseAdminFactory(admin=cls.administrator, course=cls.course, start='2020-01-05')
        cls.lesson = LessonFactory(name='Name', teacher=cls.teacher, course=cls.course,
                                   start=datetime.datetime(2020, 11, 1, 19, 0, 0))

    def test_all_teachers(self):
        """
        Тест преподавателей
        """
        response = self.query("""
            query {
                allTeachers {
                    id
                    user {
                        firstName
                        lastName
                    }
                    about
                }
            }
        """)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_teacher(self):
        """
        Тест преподавателя
        """
        response = self.query("""
            query ($id: Int!) {
                teacher(id: $id) {
                    id
                    user {
                        firstName
                        lastName
                    }
                    about
                }
            }
        """, variables={'id': self.teacher.id})
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_all_students(self):
        """
        Тест студентов
        """
        response = self.query("""
            query {
                allStudents {
                    id
                    user {
                        firstName
                        lastName
                    }
                    about
                }
            }
        """)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_student(self):
        """
        Тест студента
        """
        response = self.query("""
            query ($id: Int!) {
                student(id: $id) {
                    id
                    user {
                        firstName
                        lastName
                    }
                    about
                }
            }
        """, variables={'id': self.student.id})
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_all_administrators(self):
        """
        Тест администраторов
        """
        response = self.query("""
            query {
                allAdministrators {
                    id
                    user {
                        firstName
                        lastName
                    }
                    about
                }
            }
        """)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_administrator(self):
        """
        Тест администратора
        """
        response = self.query("""
            query ($id: Int!) {
                administrator(id: $id) {
                    id
                    user {
                        firstName
                        lastName
                    }
                    about
                }
            }
        """, variables={'id': self.administrator.id})
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_all_courses(self):
        """
        Тест курсов
        """
        response = self.query("""
            query {
                allCourses {
                    id
                    name
                    admins {
                        id
                        user {
                            firstName
                            lastName
                        }
                        about
                    }
                    students {
                        id
                        user {
                            firstName
                            lastName
                        }
                        about
                    }
                    lessonSet {
                        id
                        name
                        teacher {
                            id
                            user {
                                firstName
                                lastName
                            }
                            about
                        }
                    }
                }  
            }
        """)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_course(self):
        """
        Тест курса
        """
        response = self.query("""
            query ($id: Int!) {
                course (id: $id) {
                    id
                    name
                    admins {
                        id
                        user {
                            firstName
                            lastName
                        }
                        about
                    }
                    students {
                        id
                        user {
                            firstName
                            lastName
                        }
                        about
                    }
                    lessonSet {
                        id
                        name
                        teacher {
                            id
                            user {
                                firstName
                                lastName
                            }
                            about
                        }
                    }
                }  
            }
        """, variables={'id': self.course.id})
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_all_course_entries(self):
        """
        Тест записей студентов на курсы
        """
        response = self.query("""
            query {
                allCourseEntries {
                    id
                    course {
                        id
                        name
                    }
                    student {
                        id
                        user {
                            firstName
                            lastName
                        }
                    }
                    date
                    cost
                    paid
                }
            }
        """)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_course_entry(self):
        """
        Тест записи студента на курс
        """
        response = self.query("""
            query ($id: Int!) {
                courseEntry (id: $id) {
                    id
                    course {
                        id
                        name
                    }
                    student {
                        id
                        user {
                            firstName
                            lastName
                        }
                    }
                    date
                    cost
                    paid
                }
            }
        """, variables={'id': self.course_entry.id})
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_all_course_admins(self):
        """
        Тест связей администраторов с курсами
        """
        response = self.query("""
            query {
                allCourseAdmins {
                    id
                    course {
                        id
                        name
                    }
                    admin {
                        id
                        user {
                            firstName
                            lastName
                        }
                    }
                    start
                }
            }
        """)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_course_admin(self):
        """
        Тест связи администратора с курсом
        """
        response = self.query("""
            query ($id: Int!) {
                courseAdmin (id: $id) {
                    id
                    course {
                        id
                        name
                    }
                    admin {
                        id
                        user {
                            firstName
                            lastName
                        }
                    }
                    start
                }
            }
        """, variables={'id': self.course_admin.id})
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_all_lessons(self):
        """
        Тест уроков
        """
        response = self.query("""
            query {
                allLessons {
                    id
                    name
                    description
                    start
                    course {
                        id
                        name
                    }
                    teacher {
                        id
                        user {
                            firstName
                            lastName
                        }
                    }
                }
            }
        """)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

    def test_lesson(self):
        """
        Тест урока
        """
        response = self.query("""
            query ($id: Int!) {
                lesson (id: $id) {
                    id
                    name
                    description
                    start
                    course {
                        id
                        name
                    }
                    teacher {
                        id
                        user {
                            firstName
                            lastName
                        }
                    }
                }
            }
        """, variables={'id': self.lesson.id})
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
