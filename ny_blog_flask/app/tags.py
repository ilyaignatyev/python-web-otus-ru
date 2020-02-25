"""
Функции для работы с тэгами
"""

from typing import List

from sqlalchemy import exists, and_

from app import db
from app.models import Tag, post_tag, Post


def get_tag_names_from_str(tags: str) -> list:
    """
    Возвращает список тэгов из строки
    :param tags: Строка тэгов
    :return: Список тэгов
    """
    return list(filter(bool, [tag.strip() for tag in tags.split(',')]))


def get_tags_by_names(tag_names: List[str]) -> List[Tag]:
    """
    Возвращает список тэгов по списку названий тэгов
    :param tag_names: Список названий тэгов
    :return: Список тэгов
    """
    if not tag_names:
        return []

    # Поиск существующих тэгов и создание новых в случае отсутствия существующих
    tags = db.session.query(Tag).filter(Tag.name.in_(tag_names)).all()
    for tag_name in set(tag_names) - set(tag.name for tag in tags):
        tags.append(Tag(name=tag_name))
    return tags


def update_post_tags(post: Post, new_tag_names: List[str]):
    """
    Обновляет тэги поста по списку названий тэгов
    :param post: Пост
    :param new_tag_names: Список тэгов
    """
    deleted_tags = [tag for tag in post.tags if tag.name not in new_tag_names]
    post.tags = get_tags_by_names(new_tag_names)

    # Удалям тэги, которые не используются в других постах
    delete_unused_tags(deleted_tags)


def delete_unused_tags(tags: List[Tag]):
    """
    Удаляет неиспользуемые тэги
    :param tags: Список тэгов
    """
    if not tags:
        return

    tag_ids = [tag.id for tag in tags]
    db.session.query(Tag). \
        filter(Tag.id.in_(tag_ids)). \
        filter(
            ~exists().where(
                and_(
                    post_tag.c.tag_id == Tag.id,
                    post_tag.c.post_id.isnot(None)
                )
        )
    ).delete(synchronize_session=False)
