"""
Формы
"""

from django.forms import ModelForm, Form, CharField, Textarea

from education_app.models import Course, CourseEntry, Lesson, CourseAdmin


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


class CourseAdminForm(ModelForm):
    """
    Связь администратора курса с курсом
    """
    class Meta:
        model = CourseAdmin
        fields = ['course', 'admin', 'start']


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
