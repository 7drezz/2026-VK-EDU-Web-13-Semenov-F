from django.db import models

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
    
    def popular(self):
        return self.get_queryset().all()