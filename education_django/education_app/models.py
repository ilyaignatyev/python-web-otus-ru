"""
Модели
"""

from django.db import models


class User(models.Model):
    """
    Пользователь
    """
    name = models.CharField(max_length=200, help_text='Имя')
    surname = models.CharField(max_length=200, help_text='Фамилия')
    joined = models.DateField(auto_now_add=True, help_text='Присоединился')

    def __str__(self):
        return f'{self.name} {self.surname}'

    @property
    def full_name(self):
        return f'{self.name} {self.surname}'


class Teacher(User):
    """
    Преподаватель
    """
    resume = models.TextField(help_text='Резюме')


class Student(User):
    """
    Студент
    """
    resume = models.TextField(help_text='Резюме')


class Course(models.Model):
    """
    Курс
    """
    name = models.CharField(max_length=200, help_text='Название')
    description = models.TextField(help_text='Описание', null=True, blank=True)
    start = models.DateField(help_text='Дата начала', db_index=True)
    cost = models.IntegerField(help_text='Стоимость', null=True, blank=True)
    admins = models.ManyToManyField(User, related_name='+', db_table='course_admin')
    students = models.ManyToManyField(Student, through='CourseEntry')

    def __str__(self):
        return self.name


class CourseEntry(models.Model):
    """
    Запись студента на курс
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, help_text='Дата записи на курс')
    cost = models.IntegerField(help_text='Стоимость с учетом скидок', null=True, blank=True)
    paid = models.BooleanField(help_text='Курс оплачен', default=False)

    class Meta:
        db_table = 'course_entry'
        unique_together = ['student', 'course']


class Lesson(models.Model):
    """
    Занятие
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, help_text='Название')
    description = models.TextField(help_text='Описание', null=True, blank=True)
    start = models.DateTimeField(help_text='Дата и время начала')
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)

    class Meta:
        index_together = ["course", "start"]

    def __str__(self):
        return self.name
