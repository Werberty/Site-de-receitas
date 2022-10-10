from dataclasses import fields

from django import forms
from django.contrib.auth.models import User
from pyexpat import model


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
