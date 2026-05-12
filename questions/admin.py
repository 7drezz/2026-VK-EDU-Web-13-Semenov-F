from django.contrib import admin
from .models import Tag, Question, Answer, QuestionLike, AnswerLike

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    raw_id_fields = ['author']
    readonly_fields = ('created_at', 'rating')
    fields = ('author', 'text', 'is_correct', 'rating')
    show_change_link = True

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'questions_count')
    search_fields = ('name',)
    list_filter = ('name',)
    
    def questions_count(self, obj):
        return obj.questions.count()
    questions_count.short_description = 'количество вопросов'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'rating', 'is_active', 'created_at', 'answers_count')
    list_filter = ('is_active', 'created_at', 'tags')
    search_fields = ('title', 'text', 'author__username')
    readonly_fields = ('created_at',)
    raw_id_fields = ('author',)
    filter_horizontal = ('tags',)
    inlines = [AnswerInline]
    
    def answers_count(self, obj):
        return obj.answers.count()
    answers_count.short_description = 'количество ответов'

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'author', 'rating', 'is_correct', 'is_active')
    list_filter = ('is_correct', 'is_active')
    search_fields = ('text', 'author__username', 'question__title')
    raw_id_fields = ('author', 'question')

@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    raw_id_fields = ('user', 'question')

@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'answer', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    raw_id_fields = ('user', 'answer')