import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Profile


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your login'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '••••••••'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = 'Invalid username or password.'


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your login'})
    )
    nickname = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'How should we call you?'})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '••••••••'}),
        validators=[validate_password]
    )
    password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '••••••••'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'nickname', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if not username:
            raise forms.ValidationError('Username is required.')
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError('Username must contain only Latin letters, numbers and underscores.')
        
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters long.')
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        
        return username
    
    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if not nickname or not nickname.strip():
            raise forms.ValidationError('Nickname cannot be empty.')
        if len(nickname) < 3:
            raise forms.ValidationError('Nickname must be at least 3 characters long.')
        return nickname

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.nickname = self.cleaned_data['nickname']
            profile.save()
        return user


class ProfileForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ('nickname',)
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email
            self.fields['nickname'].initial = self.user.profile.nickname

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(id=self.user.id).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if not username:
            raise forms.ValidationError('Username is required.')
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError('Username must contain only Latin letters, numbers and underscores.')
        
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters long.')
        
        if User.objects.filter(username=username).exclude(id=self.user.id).exists():
            raise forms.ValidationError('This username is already taken.')
        
        return username
    
    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if not nickname or not nickname.strip():
            raise forms.ValidationError('Nickname cannot be empty.')
        if len(nickname) < 3:
            raise forms.ValidationError('Nickname must be at least 3 characters long.')
        return nickname

    def save(self, commit=True):
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']
        if commit:
            self.user.save()

        profile = self.user.profile
        profile.nickname = self.cleaned_data['nickname']
        if commit:
            profile.save()
        return profile