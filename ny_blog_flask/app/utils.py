"""
Общие вспомогатеьные функции
"""

from app import app


def get_image_path(image_uuid: str):
    return f'{app.config["UPLOADS_PATH"]}/{image_uuid}' if image_uuid is not None else None
