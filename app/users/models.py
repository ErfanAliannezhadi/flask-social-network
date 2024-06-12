from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import String, Column, Integer, ForeignKey
from app.extensions import db
from app.posts.models import PostModel


class UserModel(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(1000), nullable=False)
    profile_photo = Column(String(100), nullable=True)
    registration_date = Column(String(100), default=datetime.now)
    posts = relationship(PostModel, backref='auther', lazy=True)

    @property
    def followers(self):
        fs = UserFollowModel.query.filter_by(from_user_id=self.id).all()
        return [f.to_user_id for f in fs]

    @property
    def followings(self):
        fs = UserFollowModel.query.filter_by(to_user_id=self.id).all()
        return [f.from_user_id for f in fs]


class UserFollowModel(db.Model):
    __tablename__ = 'users_follow'

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    to_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
