import os
from flask import request, jsonify, current_app
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.utils import secure_filename
from app.extensions import db
from app.users.models import UserModel
from app.posts.models import PostModel, PostLikeModel, CommentModel
from app.posts.schemas import CreatePostSchema, UpdatePostSchema, PostDetailSchema, CommentSchema, ListCommentSchema


class CreatePostRoute(Resource):
    @jwt_required()
    def post(self):
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        post_schema = CreatePostSchema()
        try:
            post_data = post_schema.load(request.form)
        except Exception as err:
            return jsonify(err.messages)

        photo = request.files.get('photo', None)
        if photo is None:
            return {'message': 'No file part'}, 400
        if photo.filename == '':
            return {'message': 'No selected file'}, 400

        filename = secure_filename(photo.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'post_photos/', filename)
        photo.save(filepath)

        post = PostModel(title=post_data['title'],
                         body=post_data['body'],
                         auther_id=user.id,
                         photo=filepath)
        db.session.add(post)
        db.session.commit()

        return jsonify({"message": "done"})


class EditPostRoute(Resource):
    @jwt_required()
    def post(self, id):
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        post = PostModel.query.filter_by(id=id).first()

        if post.auther_id != user.id:
            return jsonify({"msg": "This post doesnt belong to you"})

        post_schema = UpdatePostSchema()
        try:
            post_data = post_schema.load(request.form)
        except Exception as err:
            return jsonify(err.messages)

        photo = request.files.get('photo', None)
        if photo:
            filename = secure_filename(photo.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'post_photos/', filename)
            photo.save(filepath)
            post.photo = filepath

        if post_data.get('title'):
            post.title = post_data.get('title')

        if post_data.get('body'):
            post.body = post_data.get('body')
        db.session.commit()

        return jsonify({"msg": "done"})


class DeletePostRoute(Resource):
    @jwt_required()
    def get(self, id):
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        post = PostModel.query.filter_by(id=id).first()

        if post.auther_id != user.id:
            return jsonify({"msg": "This post doesnt belong to you"})

        db.session.delete(post)
        db.session.commit()
        return jsonify({"msg": "The post was deleted."})


class PostDetailRoute(Resource):
    def get(self, id):
        post = PostModel.query.filter_by(id=id).first()
        post_schema = PostDetailSchema()
        post_data = post_schema.dump(post)
        return post_data


class PostLikeRoute(Resource):
    @jwt_required()
    def get(self, id):
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()

        if PostLikeModel.query.filter_by(user_id=user.id, post_id=id).first():
            return jsonify({"msg": "you already liked this post"})
        else:
            like = PostLikeModel(user_id=user.id, post_id=id)
            db.session.add(like)
            db.session.commit()
            return jsonify({"msg": "you liked this post"})


class PostUnlikeRoute(Resource):
    @jwt_required()
    def get(self, id):
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()

        if PostLikeModel.query.filter_by(user_id=user.id, post_id=id).first():
            like = PostLikeModel.query.filter_by(user_id=user.id, post_id=id).first()
            db.session.delete(like)
            db.session.commit()
            return jsonify({"msg": "you unliked this post"})
        else:
            return jsonify({"msg": "you did not like this post"})


class CreateCommentRoute(Resource):
    @jwt_required()
    def post(self, post_id):
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        comment_schema = CommentSchema()
        try:
            comment_data = comment_schema.load(request.json)
        except Exception as err:
            return jsonify({err.messages})
        comment = CommentModel(post_id=post_id, auther_id=user.id, body=comment_data["body"],
                               reply_to=comment_data.get("reply_to"))
        db.session.add(comment)
        db.session.commit()

        return jsonify({"msg": "done"})


class DeleteCommentRoute(Resource):
    @jwt_required()
    def get(self, comment_id):
        user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        comment = CommentModel.query.filter_by(id=comment_id).first()

        if comment.auther_id != user.id:
            return jsonify({"msg": "This comment doesnt belong to you"})

        db.session.delete(comment)
        db.session.commit()
        return jsonify({"msg": "The comment was deleted."})


class PostListCommentsRoute(Resource):
    @jwt_required()
    def get(self, post_id):
        comments = CommentModel.query.filter_by(post_id=post_id)
        comment_schema = ListCommentSchema(many=True)
        return jsonify(comment_schema.dump(comments))
