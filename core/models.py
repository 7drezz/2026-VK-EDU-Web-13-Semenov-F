import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Q

def avatar_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'avatars/user_{instance.user.id}_{instance.user.username}.{ext}'

class ProfileManager(models.Manager):
    def best_members(self, limit=10):
        one_week_ago = timezone.now() - timedelta(days=7)
        
        from django.contrib.auth.models import User
        
        users = User.objects.filter(
            Q(questions__created_at__gte=one_week_ago) | 
            Q(answers__created_at__gte=one_week_ago)
        ).annotate(
            total_rating=(
                Sum('questions__rating', filter=Q(questions__created_at__gte=one_week_ago), default=0) +
                Sum('answers__rating', filter=Q(answers__created_at__gte=one_week_ago), default=0)
            )
        ).order_by('-total_rating')[:limit]
        
        return [
            {
                'id': u.id,
                'username': u.username,
                'nickname': u.profile.nickname,
                'total_rating': u.total_rating or 0
            }
            for u in users
        ]

class Profile(models.Model):
    objects = ProfileManager()
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