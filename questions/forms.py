from django import forms
from .models import Question, Answer, Tag


class AskForm(forms.ModelForm):
    tags = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'python, django, postgresql'})
    )

    class Meta:
        model = Question
        fields = ('title', 'text')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Question title'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Describe your question...'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError('Title is required.')
        if len(title) > 200:
            raise forms.ValidationError('Title must not exceed 200 characters.')
        if len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 characters long.')
        return title
    
    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text:
            raise forms.ValidationError('Text is required.')
        if len(text) < 20:
            raise forms.ValidationError('Question text must be at least 20 characters long.')
        return text

    def clean_tags(self):
        tags_str = self.cleaned_data.get('tags', '')
        tag_names = [t.strip().lower() for t in tags_str.split(',') if t.strip()]

        if len(tag_names) > 3:
            raise forms.ValidationError('Maximum 3 tags allowed.')

        tag_objects = []
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tag_objects.append(tag)

        return tag_objects

    def save(self, user, commit=True):
        question = super().save(commit=False)
        question.author = user
        question.title = self.cleaned_data['title']
        question.text = self.cleaned_data['text']
        if commit:
            question.save()
            question.tags.set(self.cleaned_data['tags'])
        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter your answer...'}),
        }

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text or not text.strip():
            raise forms.ValidationError('Answer cannot be empty.')
        return text

    def save(self, user, question, commit=True):
        answer = super().save(commit=False)
        answer.author = user
        answer.question = question
        if commit:
            answer.save()
        return answer