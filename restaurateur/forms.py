from django import forms
import re

from django.contrib.auth.models import User


class Registration(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=50, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=30, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )
    confirm_password = forms.CharField(
        label='Подтверждение пароля', max_length=30, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        })
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            return self.add_error('username', 'Пользователь уже существует')

        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if len(password) < 8:
            return self.add_error('password', 'Пароль не должен быть меньше 8 символов')

        if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            return self.add_error('password', 'Пароль содержит недопустимые символы')

        if password and confirm_password and password != confirm_password:
            return self.add_error('confirm_password', 'Пароли не совпадают')

        return cleaned_data


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )

