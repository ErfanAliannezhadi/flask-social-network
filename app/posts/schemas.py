from marshmallow import fields
from app.extensions import ma
from app.posts.models import PostModel, CommentModel


class CreatePostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PostModel
        fields = ['title', 'body']

    title = fields.String(required=True)
    body = fields.String(required=True)


class UpdatePostSchema(ma.Schema):
    title = fields.String()
    body = fields.String()


class PostDetailSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PostModel
        fields = ['title', 'body', 'photo', 'created_date', 'auther_id']


class CommentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = CommentModel
        fields = ["body", "reply_to"]

    body = fields.String(required=True)


class ListCommentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = CommentModel
        fields = ["id", "auther_id", "post_id", "body", "reply_to", "created_date"]
