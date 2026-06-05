from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
import re
from .models import CustomUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'phone', 'email', 'password1', 'password2')
        labels = {
            'username': 'Логин'
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой почтой уже существует.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and CustomUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Пользователь с таким телефоном уже существует.')
        return phone

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not re.fullmatch(r'[A-Za-z0-9]+', username):
            raise ValidationError('Логин должен содержать только латинские буквы и цифры')

        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует')

        return username

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')

        if not re.fullmatch(r'[А-Яа-яЁё\s]+', full_name):
            raise ValidationError('ФИО должно содержать только кириллицу и пробелы')

        return full_name


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'phone', 'email']
        labels = {
            'username': 'Логин',
            'full_name': 'ФИО',
            'phone': 'Телефон',
            'email': 'Email',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '8(XXX)XXX-XX-XX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if CustomUser.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует')

        if not re.fullmatch(r'[A-Za-z0-9]+', username):
            raise ValidationError('Логин должен содержать только латинские буквы и цифры')

        return username

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')

        if not re.fullmatch(r'[А-Яа-яЁё\s]+', full_name):
            raise ValidationError('ФИО должно содержать только кириллицу и пробелы')

        return full_name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not re.fullmatch(r'8\(\d{3}\)\d{3}-\d{2}-\d{2}', phone):
            raise ValidationError('Телефон должен быть в формате 8(XXX)XXX-XX-XX')

        if CustomUser.objects.exclude(pk=self.instance.pk).filter(phone=phone).exists():
            raise ValidationError('Пользователь с таким телефоном уже существует')

        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if CustomUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')

        return email