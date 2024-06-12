from app.extensions import api
from app.posts.routes import CreatePostRoute, EditPostRoute, DeletePostRoute, PostDetailRoute, PostLikeRoute, \
    PostUnlikeRoute, CreateCommentRoute, DeleteCommentRoute, PostListCommentsRoute

api.add_resource(CreatePostRoute, '/create-post')
api.add_resource(EditPostRoute, '/edit-post/<id>')
api.add_resource(DeletePostRoute, '/delete-post/<id>')
api.add_resource(PostDetailRoute, '/detail-post/<id>')
api.add_resource(PostLikeRoute, '/post-like/<id>')
api.add_resource(PostUnlikeRoute, '/post-unlike/<id>')
api.add_resource(CreateCommentRoute, '/create-comment/<post_id>')
api.add_resource(DeleteCommentRoute, '/delete-comment/<comment_id>')
api.add_resource(DeleteCommentRoute, '/post-list-comments/<post_id>')
