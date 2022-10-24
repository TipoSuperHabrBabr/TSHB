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
    is_banned = models.BooleanField(verbose_name='заблокирован', default=False)
    start_banned_time = models.DateTimeField(verbose_name='Время начала блокировки', blank=True, null=True)
    banned_time = models.DateTimeField(verbose_name='Период блокировки', blank=True, null=True)

