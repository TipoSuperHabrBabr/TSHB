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
    path('delete_comment/<int:pk>/', blogapp.delete_comment, name='delete_comment'),
    path('edit_comment/<int:pk>/post/<int:pkp>/', blogapp.CommentUpdateView.as_view(), name="comment-update"),
]
