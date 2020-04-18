"""
Модели
"""
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.urls import reverse_lazy

from .managers import TeacherManager, StudentManager, AdministratorManager, CourseEntryManager, CourseAdminManager, \
    LessonManager, CourseManager


class UserAbstract(models.Model):
    """
    Пользователь
    """
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    about = models.TextField(verbose_name='О себе')

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @staticmethod
    def get_for_user(user_id: int) -> 'Teacher' or None:
        """
        Возвращает преподавателя по идентификатору пользователя
        :param user_id: Идентификатор пользователя
        :return: Преподаватель
        """
        return Teacher.objects.filter(user__id=user_id).first()


class Teacher(UserAbstract):
    """
    Преподаватель
    """
    objects = TeacherManager()

    @staticmethod
    def get_by_user(user_id: int) -> 'Teacher' or None:
        """
        Возвращает преподавателя по идентификатору пользователя
        :param user_id: Идентификатор пользователя
        :return: Преподаватель
        """
        return Teacher.objects.filter(user__id=user_id).first()


class Student(UserAbstract):
    """
    Студент
    """
    objects = StudentManager()

    @staticmethod
    def get_by_user(user_id: int) -> 'Student' or None:
        """
        Возвращает студента по идентификатору пользователя
        :param user_id: Идентификатор пользователя
        :return: Студент
        """
        return Student.objects.filter(user__id=user_id).first()

    def course_entries_with_courses(self):
        """
        Возвращает записи на курсы с данными по курсам
        """
        return self.courseentry_set.select_related('course').order_by('course__start')


class Administrator(UserAbstract):
    """
    Администратор
    """
    objects = AdministratorManager()

    @staticmethod
    def get_by_user(user_id: int) -> 'Administrator' or None:
        """
        Возвращает администратора по идентификатору пользователя
        :param user_id: Идентификатор пользователя
        :return: Администратор
        """
        return Administrator.objects.filter(user__id=user_id).first()


class Course(models.Model):
    """
    Курс
    """
    objects = CourseManager()

    name = models.CharField(verbose_name='Название', max_length=200)
    description = models.TextField(verbose_name='Описание', blank=True)
    start = models.DateField(verbose_name='Дата начала', db_index=True)
    cost = models.IntegerField(verbose_name='Стоимость', null=True, blank=True)
    admins = models.ManyToManyField(Administrator, verbose_name='Администраторы', through='CourseAdmin', blank=True)
    students = models.ManyToManyField(Student, verbose_name='Студенты', through='CourseEntry', blank=True)
    deleted = models.BooleanField(verbose_name='Удален', default=False, blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_url(course_id: int) -> str:
        """
        Возвращает ссылку на курс
        :param course_id: Идентификатор курса
        """
        return reverse_lazy('education_app:course', kwargs={'id': course_id})

    @staticmethod
    def can_update(course_id: int, user: User):
        """
        Может ли редактировать курс переданный пользвоатель.
        Курс может редактировать суперпользователь или администратор этого курса.
        :param course_id: Курс
        :param user: Пользователь
        :return: Права на редактирование
        """
        if user.is_superuser:
            return True

        return CourseAdmin.objects.filter(course__id=course_id, admin__user__id=user.id).exists()

    @staticmethod
    def is_admin(course_id: int, user_id: int):
        """
        Является ли пользователь администратором курса
        :param course_id:
        :param user_id:
        :return:
        """
        return CourseAdmin.objects.filter(course__id=course_id, admin__user__id=user_id).exists()

    def lessons_with_teachers(self):
        """
        Возвращает уроки курса с данными по учителям
        """
        return self.lesson_set.select_related('teacher').select_related('teacher__user').order_by('start')

    def course_entries_with_students(self):
        """
        Возвращает записи студентов на курс с данными по студентам
        """
        return self.courseentry_set.select_related('student').select_related('student__user')

    def course_admins_with_admins(self):
        """
        Возвращает связь администраторов с курсом с данными по администраторам
        """
        return self.courseadmin_set.select_related('admin').select_related('admin__user')


class CourseEntry(models.Model):
    """
    Запись студента на курс
    """
    student = models.ForeignKey(Student, verbose_name='Студент', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Дата записи на курс', auto_now_add=True)
    cost = models.IntegerField(verbose_name='Стоимость с учетом скидок', null=True, blank=True)
    paid = models.BooleanField(verbose_name='Курс оплачен', default=False)

    objects = CourseEntryManager()

    class Meta:
        db_table = 'education_app_course_entry'
        unique_together = ['student', 'course']


class CourseAdmin(models.Model):
    """
    Администратор курса
    """
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE)
    admin = models.ForeignKey(Administrator, verbose_name='Администратор', on_delete=models.CASCADE)
    start = models.DateField(verbose_name='Дата начала')

    objects = CourseAdminManager()

    class Meta:
        db_table = 'education_app_course_admin'
        unique_together = ['course', 'admin']


class Lesson(models.Model):
    """
    Занятие
    """
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Название', max_length=200)
    description = models.TextField(verbose_name='Описание', blank=True)
    start = models.DateTimeField(verbose_name='Дата и время начала')
    teacher = models.ForeignKey(Teacher, verbose_name='Преподаватель', null=True, blank=True, on_delete=models.PROTECT)

    objects = LessonManager()

    class Meta:
        index_together = ['course', 'start']
        ordering = ['start', 'id']

    @staticmethod
    def can_cud(course_id: int, user: User):
        """
        Может ли создавать, редактировать, удалять урок переданный пользвоатель.
        - создание: суперпользователь, администратор курса, к которому относится урок
        - изменение: суперпользователь, администратор курса, к которому относится урок, преподаватель урока
        - удаление: суперпользователь, администратор курса, к которому относится урок
        :param course_id: Курс
        :param user: Пользователь
        :return: Права на создание, изменение, удаление
        """
        if user.is_superuser:
            return True

        return Lesson.objects.filter(Q(course__id=course_id) & (
                                     Q(course__courseadmin__admin__user__id=user.id) |
                                     Q(teacher__user__id=user.id))).exists()

    def __str__(self):
        return self.name
