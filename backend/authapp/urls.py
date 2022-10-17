from django.urls import path
from authapp import views as authapp
from django.contrib.auth import views as djviews
app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.register, name='register'),
    path('edit/', authapp.edit, name='edit'),
    path('password_change/', authapp.password_change, name='password_change'),
    path('password_change/done/',authapp.password_change_done, name="change_password_done"),
]
