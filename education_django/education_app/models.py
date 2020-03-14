"""
Модели
"""

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy


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


class Teacher(UserAbstract):
    """
    Преподаватель
    """
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
    @staticmethod
    def get_by_user(user_id: int) -> 'Student' or None:
        """
        Возвращает студента по идентификатору пользователя
        :param user_id: Идентификатор пользователя
        :return: Студент
        """
        return Student.objects.filter(user__id=user_id).first()


class Administrator(UserAbstract):
    """
    Администратор
    """
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


class CourseEntry(models.Model):
    """
    Запись студента на курс
    """
    student = models.ForeignKey(Student, verbose_name='Студент', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Дата записи на курс', auto_now_add=True)
    cost = models.IntegerField(verbose_name='Стоимость с учетом скидок', null=True, blank=True)
    paid = models.BooleanField(verbose_name='Курс оплачен', default=False)

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

    class Meta:
        index_together = ['course', 'start']
        ordering = ['start', 'id']

    def __str__(self):
        return self.name
