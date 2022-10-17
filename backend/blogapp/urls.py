from blogapp import views as blogapp
from django.urls import path

app_name = 'blogapp'

urlpatterns = [
    path('create_post/', blogapp.PostCreateView.as_view(), name='create_post'),
    path('edit_post/<int:pk>/', blogapp.edit_post, name='edit_post'),
    # path('delete_post/<int:pk>/', blogapp.PostDeleteView.as_view(), name='delete_post'),
    path('delete_post/<int:pk>/', blogapp.delete_post, name='delete_post'),
    path('error_user/', blogapp.error_user, name='error_user'),

]