# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django import forms


class FormUserUp(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }),
                                label='Contraseña')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }),
                                label='Confirma contraseña')
    avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'avatar')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', }),
            'first_name': forms.TextInput(attrs={'class': 'form-control', }),
            'last_name': forms.TextInput(attrs={'class': 'form-control', }),
            'email': forms.EmailInput(attrs={'class': 'form-control', }),
            'avatar': forms.FileInput(attrs={'class': 'form-control', }),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2

    # def clean_email(self):
    #     """Comprueba que no exista un email igual en la db"""
    #     username = self.cleaned_data['username']
    #     email = self.cleaned_data['email']
    #     email_valid = User.objects.filter(email=email).exclude(username=username)
    #     if email_valid:
    #         raise forms.ValidationError('Ya existe un email igual registrado.')
    #     return email


class FormCreateUser(FormUserUp):

    def clean_username(self):
        """Comprueba que no exista un username igual en la db"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado.')
        return username

    def clean_email(self):
        """Comprueba que no exista un email igual en la db"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Ya existe un email igual registrado.')
        return email


class FormEditPass(forms.ModelForm):

    password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('password1', 'password2')


    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2