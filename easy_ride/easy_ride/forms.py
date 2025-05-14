from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from easy_ride.models import UserInformation, Rent


class RegistrationUserForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'name': 'username',
            'id': 'username',
            'placeholder': 'Придумайте логин'
        }),
        required=True
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'name': 'email',
            'id': 'email',
            'placeholder': 'Введите ваш email'
        })
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'name': 'password',
            'id': 'password',
            'placeholder': 'Придумайте пароль'
        })
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'name': 'confirm-password',
            'id': 'confirm-password',
            'placeholder': 'Повторите пароль'
        })
    )


class AuthorizationUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'login',
            'name': 'login',
            'placeholder': 'Логин'
        }),
        required=True
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password',
            'name': 'password',
            'placeholder': 'Пароль'
        }),
        required=True
    )


class UserInformationForm(forms.ModelForm):
    class Meta:
        model = UserInformation
        fields = ['surname', 'name', 'patronymic', 'phone_num', 'age', 'passport_series', 'passport_num', 'avatar']
        widgets = {
            'phone_num': forms.TextInput(attrs={'placeholder': '+79000000000'}),
            'avatar': forms.FileInput(attrs={'accept': 'image/*'})
        }


class RentForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date >= end_date:
                raise ValidationError("Дата окончания должна быть позже даты начала")
            if start_date < timezone.now():
                raise ValidationError("Нельзя арендовать машину в прошлом")
        return cleaned_data