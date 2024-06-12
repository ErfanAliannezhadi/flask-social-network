from app.extensions import api
from app.users.routes import RegisterRoute, LoginRoute, RefreshTokenRoute, UploadPhotoRoute, UpdatePasswordRoute, \
    UserFollowRoute, UserUnfollowRoute, UserProfileRoute

api.add_resource(RegisterRoute, '/register')
api.add_resource(LoginRoute, '/login')
api.add_resource(RefreshTokenRoute, '/refresh')
api.add_resource(UploadPhotoRoute, '/upload-photo')
api.add_resource(UpdatePasswordRoute, '/update-password')
api.add_resource(UserFollowRoute, '/follow/<id>')
api.add_resource(UserUnfollowRoute, '/unfollow/<id>')
api.add_resource(UserProfileRoute, '/profile/<id>')
