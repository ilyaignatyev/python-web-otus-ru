"""
Формы
"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import Form, CharField, Textarea, ChoiceField, EmailField

from education_app.const import USER_TYPE


class RegisterForm(Form):
    """
    Регистрация пользователя
    """
    first_name = CharField(max_length=140, label='Имя')
    last_name = CharField(max_length=140, label='Фамилия')
    user_type = ChoiceField(
        choices=(
            (USER_TYPE.STUDENT, 'Студент'),
            (USER_TYPE.TEACHER, 'Преподаватель'),
            (USER_TYPE.ADMINISTRATOR, 'Администратор курса')
        ),
        initial=USER_TYPE.STUDENT,
        label='Тип пользователя'
    )
    email = EmailField(max_length=140, label='Email')
    username = CharField(max_length=140, label='Логин')
    password = CharField(max_length=140, label='Пароль')
    password_confirm = CharField(max_length=140, label='Повторите пароль')
    about = CharField(widget=Textarea(attrs={'rows': 10}), label='О себе')

    def clean(self) -> dict:
        """
        Проверка данных
        """
        data = self.cleaned_data
        user_type = int(data['user_type']) if data.get('user_type') is not None else None

        check_fields = {
            'first_name': 'Не заполнено имя',
            'last_name': 'Не заполнена фамилия',
            'email': 'Не заполнен email',
            'username': 'Не заполнен логин',
            'password': 'Не заполнен пароль',
            'password_confirm': 'Не заполнено подтверждение пароля',
            'about': 'Не заполнено о себе',
        }

        for field in check_fields:
            if not data.get(field):
                raise ValidationError(check_fields[field])

        if user_type not in (USER_TYPE.TEACHER, USER_TYPE.STUDENT, USER_TYPE.ADMINISTRATOR):
            raise ValidationError('Не заполнен тип пользователя')

        if data['password'] != data['password_confirm']:
            raise ValidationError('Пароли не совпадают')

        if User.objects.filter(username=data['username']).exists():
            raise ValidationError(f'Пользователь с логином {data["username"]} уже существует')

        return data
