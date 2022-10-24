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
]
