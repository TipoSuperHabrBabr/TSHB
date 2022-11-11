from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from backend import settings


class Post(models.Model):
    CATEGORY_CHOICES = (
        ('DESING', 'Дизайн'),
        ('WEB_DEVELOPMENT', 'Веб-разработка'),
        ('MOBIL_DEVELOPMENT', 'Мобильная разработка'),
        ('MARKETING', 'Маркетинг'),
    )

    category = models.CharField(choices=CATEGORY_CHOICES, blank=False, verbose_name='Категория', max_length=150)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body_text = models.TextField()
    body_image = models.ImageField(upload_to='posts/', blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    edit_date = models.DateTimeField(default=timezone.now)
    tags = models.CharField(max_length=250, blank=False)
    is_active = models.BooleanField(default=True)
    is_like = GenericRelation('Like')

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class Comment(models.Model):
    post_id = models.ForeignKey('blogapp.Post', on_delete=models.CASCADE, related_name='comments')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body_text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    parent_comment_id = models.IntegerField(default=0)
    head_comment = models.BooleanField(default=True)
    is_like = GenericRelation('Like')

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    @property
    def total_likes(self):
        return self.is_like.count()


class Like(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liked = models.BooleanField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent_object = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    body_text = models.TextField(verbose_name='текст сообщения')
    path = models.TextField(verbose_name='Ссылка', default=None)
    created_date = models.DateTimeField(default=timezone.now)
