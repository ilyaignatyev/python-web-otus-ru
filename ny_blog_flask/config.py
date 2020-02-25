"""
Конфигурация
"""

CSRF_ENABLED = True

SECRET_KEY = 'sdjfgkjdfhgdfgdsfjhgeruiytiuerwyt324658973645'

#  Длина "Соли" для хешрования паролей
PASSWORD_SALT_LENGTH = 100

SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.sqlite'

SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOADS_FOLDER = 'uploads'

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Количество постов на странице для постраничной навигации
POSTS_PER_PAGE = 2
