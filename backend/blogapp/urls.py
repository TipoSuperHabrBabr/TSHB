from django.urls import path
from blogapp import views as blogapp

app_name = 'blogapp'

urlpatterns = [
    path('', blogapp.index, name='index'),
    path('category/<int:pk>/', blogapp.blog, name='category'),
]
