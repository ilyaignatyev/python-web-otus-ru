"""
Функции для работы с изображениями
"""
import os
import uuid

from werkzeug.utils import secure_filename

from app import app
from app.utils import get_image_path


def allowed_image(filename):
    """
    Проверяет корректность расширения файла
    :param filename: Имя файла
    :return: Подходит ли файл
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_IMAGE_EXTENSIONS']


def delete_image(image_uuid: str):
    """
    Удаляет изображение
    :param image_uuid: Идентификатор изображения
    """
    if image_uuid is not None:
        os.remove(get_image_path(image_uuid))


def save_image(image) -> (str, str):
    """
    Созранение избражение, если оно корректно
    :param image: Изображение
    :return: Название и идентификатор изображения
    """
    image_name = None
    image_uuid = None
    if image is not None and allowed_image(image.filename):
        # Изображения постов храним в отдельной папке на диске, название файла поста генерируем в виде uuid,
        # оригинальные имена файлов также сохраняем в БД
        image_name = secure_filename(image.filename)
        image_uuid = str(uuid.uuid4())
        image.save(get_image_path(image_uuid))
    return image_name, image_uuid
