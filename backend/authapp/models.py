from django.contrib.auth.models import AbstractUser
from django.db import models


class BlogUser(AbstractUser):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )
    avatar = models.ImageField(upload_to='users_avatars', blank=True, verbose_name='Аватар')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', default=18)
    is_active = models.BooleanField(verbose_name='активность', default=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name='Пол')
    about_me = models.TextField(verbose_name='О себе', blank=True, max_length=512)

