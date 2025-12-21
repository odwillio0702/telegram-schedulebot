from .database import add_or_update_user, increment_views, add_like

def register_user(data):
    add_or_update_user(data)
    increment_views(data['id'])

def like_user(user_id):
    add_like(user_id)