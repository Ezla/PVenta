# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class AuthenticationFormCustom(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

    error_messages = {
        'invalid_login': "Porfavor introdusca un nombre de usuario y/o contraseña validos. Considere que ambos campos son sensibles al uso de mayúsculas.",
        'inactive': "Este usuario esta inactivo",
    }
