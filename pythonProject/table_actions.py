import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from models import Base, User, Post

load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")


def create_tables():
    """
    Создание таблиц (если их еще нет в базе данных)
    """
    inspector = inspect(engine)

    has_users_table = 'users' in inspector.get_table_names()
    has_posts_table = 'posts' in inspector.get_table_names()

    if not (has_users_table and has_posts_table):
        Base.metadata.create_all(engine)


def add_user(username: str, email: str, password: str):
    """
    Добавление пользователя в таблицу пользователей
    """
    with Session(engine) as session:
        new_user = User(username=username, email=email, password=password)
        session.add(new_user)
        session.commit()


def add_post(title: str, content: str, user_id: int):
    """
    Добавление поста в таблицу постов (связано с пользователем)
    """
    with Session(engine) as session:
        new_post = Post(title=title, content=content, user_id=user_id)
        session.add(new_post)
        session.commit()


def get_all_users():
    """
    Извлекает информацию о всех пользователях
    """
    with Session(engine) as session:
        users = session.query(User).all()
        return users


def get_all_posts():
    """
    Извлекает информацию о всех постах, хранящихся в таблице
    """
    with Session(engine) as session:
        posts = session.query(Post).all()
        return posts


def get_posts_by_user_id(user_id: int):
    """
    Извлекает информацию о постах определенного пользователя
    """
    with Session(engine) as session:
        posts = session.query(Post).filter(Post.user_id == user_id).all()
        return posts


def update_email(user_id: int, new_email: str):
    """
    Обновляет email ользователя
    """
    with Session(engine) as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user.email = new_email
            session.commit()


def update_content(post_id: int, new_content: str):
    """
    Обновляет content поста
    """
    with Session(engine) as session:
        post = session.query(Post).filter(Post.id == post_id).first()
        if post:
            post.content = new_content
            session.commit()


def delete_post(post_id: int):
    """
    Удаляет пост по id
    """
    with Session(engine) as session:
        post = session.query(Post).filter(Post.id == post_id).first()
        if post:
            session.delete(post)
            session.commit()


def delete_user(user_id: int):
    """
    Удаляет пользователя по id
    """
    with Session(engine) as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            session.query(Post).filter(Post.user_id == user.id).delete()
            session.delete(user)
            session.commit()
