from django.urls import path
from authapp import views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.register, name='register'),
    path('edit/', authapp.edit, name='edit'),
    path('password_change/', authapp.password_change, name='password_change'),
    path('password_change/done/',authapp.password_change_done, name="change_password_done"),
    path('read/<int:pk>/', authapp.UserDetailView.as_view(), name='user_read'),
    path('profile/<int:pk>/', authapp.profile, name='profile'),
    path('profile_banned/<int:pk>/', authapp.profile, name='profile_banned'),
    path('profile_activate/<int:pk>/', authapp.profile, name='profile_activate'),
    path('profile_moderator_on/<int:pk>/', authapp.profile, name='profile_moderator_on'),
    path('profile_moderator_off/<int:pk>/', authapp.profile, name='profile_moderator_off'),
]
