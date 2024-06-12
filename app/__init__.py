import os
from datetime import timedelta
from flask import Flask
from app.extensions import db, migrate, api, bcrypt, ma, jwt
from app.users.urls import *
from app.posts.urls import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["JWT_SECRET_KEY"] = "4u3829y7894q65f7hy9yhr7f8rhe43rs67oha79yy348q"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config['UPLOAD_FOLDER'] = 'media/'
os.makedirs(f'{app.config["UPLOAD_FOLDER"]}/', exist_ok=True)
os.makedirs(f'{app.config["UPLOAD_FOLDER"]}/profile_photos/', exist_ok=True)
os.makedirs(f'{app.config["UPLOAD_FOLDER"]}/post_photos/', exist_ok=True)

# initialize the app with the extension
db.init_app(app)

migrate.init_app(app, db)

api.init_app(app)

bcrypt.init_app(app)

ma.init_app(app)

jwt.init_app(app)
