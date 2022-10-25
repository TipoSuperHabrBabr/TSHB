from django.db import models
from django.utils import timezone

from backend import settings


class Post(models.Model):
    CATEGORY_CHOICES = (
        ('DESING', 'Дизайн'),
        ('WEB_DEVELOPMENT', 'Веб-разработка'),
        ('MOBIL_DEVELOPMENT', 'Мобильная разработка'),
        ('MARKETING', 'Маркетинг'),
    )

    category = models.CharField(choices=CATEGORY_CHOICES, blank=True, verbose_name='Категория', max_length=150)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body_text = models.TextField()
    body_image = models.ImageField(upload_to='posts/', blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    edit_date = models.DateTimeField(default=timezone.now)
    tags = models.CharField(max_length=250, blank=True)
    is_active = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class Comment(models.Model):
    post_id = models.ForeignKey('blogapp.Post', on_delete=models.CASCADE, related_name='comments')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body_text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()
