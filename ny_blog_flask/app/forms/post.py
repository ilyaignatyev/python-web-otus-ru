"""
Форма редактирования поста
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired

from config import ALLOWED_IMAGE_EXTENSIONS


class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    text = TextAreaField('Текст', validators=[DataRequired()])
    tags = StringField('Тэги')
    image = FileField('Изображение', validators=[FileAllowed(ALLOWED_IMAGE_EXTENSIONS, 'Только файлы изображений')])
