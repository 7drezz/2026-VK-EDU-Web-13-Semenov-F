from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .managers import QuestionManager, AnswerManager, TagManager

class Tag(models.Model):
    objects = TagManager()
    
    name = models.CharField(max_length=50, unique=True, verbose_name='название')
    
    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
    
    def __str__(self):
        return self.name


class Question(models.Model):
    objects = QuestionManager()
    
    title = models.CharField(max_length=200, verbose_name='заголовок')
    text = models.TextField(verbose_name='текст вопроса')
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='questions',
        verbose_name='автор'
    )
    tags = models.ManyToManyField(Tag, related_name='questions', verbose_name='теги')
    rating = models.IntegerField(default=0, verbose_name='рейтинг')
    is_active = models.BooleanField(default=True, verbose_name='активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    
    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('questions:question', kwargs={'question_id': self.id})
    
    def answers_count(self):
        return self.answers.count()


class Answer(models.Model):
    objects = AnswerManager()
    
    text = models.TextField(verbose_name='текст ответа')
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='answers',
        verbose_name='автор'
    )
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        related_name='answers',
        verbose_name='вопрос'
    )
    rating = models.IntegerField(default=0, verbose_name='рейтинг')
    is_correct = models.BooleanField(default=False, verbose_name='правильный ответ')
    is_active = models.BooleanField(default=True, verbose_name='активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    
    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'
        ordering = ['-rating', '-created_at']
    
    def __str__(self):
        return f'Ответ #{self.id} на вопрос #{self.question_id}'


class QuestionLike(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='пользователь'
    )
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='вопрос'
    )
    value = models.SmallIntegerField(
        default=1,
        choices=[(1, 'лайк'), (-1, 'дизлайк')],
        verbose_name='значение'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    
    class Meta:
        verbose_name = 'лайк вопроса'
        verbose_name_plural = 'лайки вопросов'
        unique_together = ['user', 'question']  
    
    def __str__(self):
        return f'{self.user.username} -> {self.question.title[:20]}'


class AnswerLike(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='пользователь'
    )
    answer = models.ForeignKey(
        Answer, 
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='ответ'
    )
    value = models.SmallIntegerField(
        default=1,
        choices=[(1, 'лайк'), (-1, 'дизлайк')],
        verbose_name='значение'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    
    class Meta:
        verbose_name = 'лайк ответа'
        verbose_name_plural = 'лайки ответов'
        unique_together = ['user', 'answer']
    
    def __str__(self):
        return f'{self.user.username} -> ответ #{self.answer.id}'