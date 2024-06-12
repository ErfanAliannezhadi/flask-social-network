from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey
from app.extensions import db


class PostModel(db.Model):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    body = Column(String(10000), nullable=False)
    photo = Column(String(100), nullable=True)
    created_date = Column(String(100), default=datetime.now)
    auther_id = Column(Integer, ForeignKey('users.id'), nullable=False)


class CommentModel(db.Model):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    auther_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    body = Column(String(1000), nullable=False)
    created_date = Column(String(100), default=datetime.now)
    reply_to = Column(Integer, nullable=True, default=None)


class PostLikeModel(db.Model):
    __tablename__ = 'post_likes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
