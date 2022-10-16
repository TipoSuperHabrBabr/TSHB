from django.urls import path
from blogapp import views as blogapp

app_name = 'blogapp'

urlpatterns = [
    path('category', blogapp.blog, name='category'),
]
