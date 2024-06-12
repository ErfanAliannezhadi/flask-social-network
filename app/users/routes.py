import os
from flask import request, jsonify, url_for, current_app
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, create_refresh_token
from werkzeug.utils import secure_filename
from app.extensions import bcrypt, db
from app.users.models import UserModel, UserFollowModel
from app.users.schemas import UserRegisterSchema, UserLoginSchema, UpdatePasswordSchema, UserDetailSchema


class RegisterRoute(Resource):
    def post(self):
        user_schema = UserRegisterSchema()
        try:
            user_data = user_schema.load(request.json)
        except Exception as err:
            return jsonify(err.messages)

        hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        user = UserModel(email=user_data['email'], username=user_data['username'], password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return user_data


class LoginRoute(Resource):
    def post(self):
        user_schema = UserLoginSchema()
        user_data = user_schema.load(request.json)

        user = UserModel.query.filter_by(username=user_data['username']).first()

        if user and bcrypt.check_password_hash(user.password, user_data['password']):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            return jsonify(access_token=access_token, refresh_token=refresh_token)

        return jsonify({"msg": "username or password is wrong. "})


class RefreshTokenRoute(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token)


class UploadPhotoRoute(Resource):
    @jwt_required()
    def post(self):
        if 'photo' not in request.files:
            return {'message': 'No file part'}, 400

        photo = request.files['photo']
        if photo.filename == '':
            return {'message': 'No selected file'}, 400

        filename = secure_filename(photo.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profile_photos/', filename)
        photo.save(filepath)

        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        user.profile_photo = filename
        db.session.commit()

        file_url = url_for('static',
                           filename=os.path.join(current_app.config['UPLOAD_FOLDER'], 'profile_photos', filename),
                           _external=True)
        file_data = {
            "filename": filename,
            "file_size": os.path.getsize(filepath),
            "content_type": photo.content_type,
            "url": file_url
        }
        return jsonify(file_data)


class UpdatePasswordRoute(Resource):
    @jwt_required()
    def post(self):
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()

        pass_schema = UpdatePasswordSchema()
        try:
            pass_data = pass_schema.load(request.json)
        except Exception as err:
            return jsonify(err.messages)

        if bcrypt.check_password_hash(user.password, pass_data['old_password']):
            user.password = bcrypt.generate_password_hash(pass_data['new_password']).decode('utf-8')
            db.session.commit()
            return jsonify({"msg": "done"})
        else:
            return jsonify({"msg": "old password is wrong."})


class UserFollowRoute(Resource):
    @jwt_required()
    def get(self, id):
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()

        if not UserFollowModel.query.filter_by(from_user_id=user.id, to_user_id=id).first():
            follow = UserFollowModel(from_user_id=user.id, to_user_id=id)
            db.session.add(follow)
            db.session.commit()
            return jsonify({"msg": "you followed this user"})
        else:
            return jsonify({"msg": "you already follow this user"})


class UserUnfollowRoute(Resource):
    @jwt_required()
    def get(self, id):
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()

        if UserFollowModel.query.filter_by(from_user_id=user.id, to_user_id=id).first():
            UserFollowModel.query.filter_by(from_user_id=user.id, to_user_id=id).delete()
            db.session.commit()
            return jsonify({"msg": "you unfollowed this user"})
        else:
            return jsonify({"msg": "you are not following this user"})


class UserProfileRoute(Resource):
    @jwt_required()
    def get(self, id):
        user_schema = UserDetailSchema()
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        user_data = user_schema.dump(user)
        return user_data
