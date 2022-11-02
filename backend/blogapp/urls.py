from blogapp import views as blogapp
from django.urls import path

app_name = 'blogapp'

urlpatterns = [
    path('create_post/', blogapp.PostCreateView.as_view(), name='create_post'),
    path('category', blogapp.blog, name='category'),
    path('edit_post/<int:pk>/', blogapp.edit_post, name='edit_post'),
    # path('read_post/<int:pk>/', blogapp.PostRead.as_view(), name='read_post'),
    path('read_post/<int:pk>/', blogapp.post_detail, name='read_post'),
    path('delete_post/<int:pk>/', blogapp.delete_post, name='delete_post'),
    path('comment_delete/<int:pk>/', blogapp.delete_comment, name='comment_delete'),
    path('comment_update/<int:pk>/post/<int:pkp>/', blogapp.CommentUpdateView.as_view(), name="comment_update"),
    path('comment_reply/<int:pk>/', blogapp.comment_reply, name='comment_reply'),
    path('like/<obj>/<pk>/<pkc>', blogapp.like, name='like'),
]
