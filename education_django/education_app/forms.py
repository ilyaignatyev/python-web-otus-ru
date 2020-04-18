"""
Формы
"""

from django.forms import ModelForm, Form, CharField, Textarea, ModelChoiceField

from education_app.models import Course, CourseEntry, Lesson, CourseAdmin
from .models import Administrator, Student, Teacher


class CourseForm(ModelForm):
    """
    Создание/редактирование курса
    """
    class Meta:
        model = Course
        fields = ['name', 'description', 'start', 'cost']


class CourseEntryForm(ModelForm):
    """
    Запись на курс
    """
    class Meta:
        model = CourseEntry
        fields = ['course', 'student', 'cost', 'paid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].disabled = True

    student = ModelChoiceField(label='Студент', queryset=Student.objects.with_user_data)


class CourseEntryCreateForm(CourseEntryForm):
    """
    Создание записи на курс
    """
    pass


class CourseEntryUpdateForm(CourseEntryForm):
    """
    Редактирвоание записи на курс
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].disabled = True
        self.fields['student'].disabled = True


class LessonForm(ModelForm):
    """
    Создание/редактирвоание урока
    """
    class Meta:
        model = Lesson
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].disabled = True

    teacher = ModelChoiceField(label='Преподаватель', queryset=Teacher.objects.with_user_data)


class CourseAdminForm(ModelForm):
    """
    Связь администратора курса с курсом
    """
    class Meta:
        model = CourseAdmin
        fields = ['course', 'admin', 'start']

    admin = ModelChoiceField(label='Администратор', queryset=Administrator.objects.with_user_data)

class CourseAdminCreateForm(CourseAdminForm):
    """
    Создание администратора курса
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].disabled = True


class CourseAdminUpdateForm(CourseAdminForm):
    """
    Редактирование администратора курса
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].disabled = True
        self.fields['admin'].disabled = True


class SendEmailForm(Form):
    """
    Отправка email на странице "Контакты"
    """
    theme = CharField(max_length=140)
    message = CharField(widget=Textarea(attrs={'rows': 10}))
