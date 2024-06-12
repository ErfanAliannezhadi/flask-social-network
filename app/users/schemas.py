from marshmallow import validates, ValidationError, fields, validates_schema
from app.extensions import ma
from app.users.models import UserModel, UserFollowModel


class UserRegisterSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        fields = ['email', 'username', 'password']

    email = fields.Email(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)

    @validates('username')
    def validate_username(self, value):
        user = UserModel.query.filter_by(username=value).first()
        if user:
            raise ValidationError('Username must be unique. ')
        return value

    @validates('email')
    def validate_email(self, value):
        user = UserModel.query.filter_by(email=value).first()
        if user:
            raise ValidationError('Email must be unique. ')
        return value


class UserLoginSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        fields = ['username', 'password']


class UpdatePasswordSchema(ma.Schema):
    old_password = fields.String(required=True)
    new_password = fields.String(required=True)
    confirm_new_password = fields.String(required=True)

    @validates_schema
    def validate_fields(self, data, **kwargs):
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise ValidationError('new password and confirm new password must match')

        if new_password == old_password:
            raise ValidationError('new password is the old password')


class UserDetailSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'profile_photo', 'registration_date', 'followers', 'followings']
