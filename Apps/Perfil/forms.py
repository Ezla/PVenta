# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django import forms

class FormUser(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', }),
            'first_name': forms.TextInput(attrs={'class': 'form-control', }),
            'last_name': forms.TextInput(attrs={'class': 'form-control', }),
            'email': forms.EmailInput(attrs={'class': 'form-control', }),
            'avatar': forms.FileInput(attrs={'class': 'form-control', }),
        }

class FormUserUp(FormUser):
    pass




class FormCreateUser(FormUser):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }),
                                label='Contraseña')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }),
                                label='Confirma contraseña')


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2




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