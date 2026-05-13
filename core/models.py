import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def avatar_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'avatars/user_{instance.user.id}_{instance.user.username}.{ext}'


class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile',
        verbose_name='пользователь'
    )
    nickname = models.CharField(max_length=50, verbose_name='никнейм')
    avatar = models.ImageField(
        upload_to=avatar_upload_path, 
        null=True, 
        blank=True,
        verbose_name='аватар'
    )
    
    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'
    
    def __str__(self):
        return self.nickname or self.user.username
    
    def get_avatar_url(self):
        if self.avatar and os.path.exists(self.avatar.path):
            return self.avatar.url
        return '/static/img/avatars/default.jpg'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, nickname=instance.username)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()