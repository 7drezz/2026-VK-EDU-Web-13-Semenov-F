from django.db import models
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

class QuestionManager(models.Manager):
    
    def new(self):
        return self.get_queryset().filter(is_active=True).order_by('-created_at')
    
    def hot(self):
        return self.get_queryset().filter(is_active=True).order_by('-rating', '-created_at')
    
    def by_tag(self, tag_name):
        return self.get_queryset().filter(tags__name=tag_name, is_active=True)
    
    def active(self):
        return self.get_queryset().filter(is_active=True)


class AnswerManager(models.Manager):
    
    def active(self):
        return self.get_queryset().filter(is_active=True)


class TagManager(models.Manager):
    
    def popular(self, limit=20):
        three_months_ago = timezone.now() - timedelta(days=90)
        return self.filter(
            questions__is_active=True,
            questions__created_at__gte=three_months_ago
        ).annotate(
            question_count=Count('questions')
        ).order_by('-question_count')[:limit]