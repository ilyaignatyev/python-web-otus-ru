"""
Роутинг постов (список всех постов и карточки поста)
"""

from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from fake_posts import test_posts

posts_app = Blueprint('posts_app', __name__)


@posts_app.route('/', methods=['GET'], endpoint='posts')
def post_list():
    return render_template('posts.html', posts=test_posts)


@posts_app.route('/<int:post_id>/', methods=['GET'], endpoint='post')
def post(post_id: int):
    found_posts = list(filter(lambda post: post['id'] == post_id, test_posts))
    if not found_posts:
        raise NotFound(f'Post {post_id} not found')
    return render_template('post.html', post=found_posts[0])

# @posts_app.route('/<int:post_id>/', methods=['POST'])
# def update_post(post_id: int):
#     # raise NotFound(f'No product {id}')
#     # TODO: update post
#     return render_template('post.html', post_id=post_id)
