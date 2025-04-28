from django import forms
from .models import *

import re

class FotoForm(forms.ModelForm):
    class Meta:
        model = Foto
        # fields = "__all__"
        fields = ['local', 'image_local', 'name_foto_local']
        widgets = {
            'image_local': forms.FileInput(attrs={'class':'form-control '}),
            'name_foto_local': forms.TextInput(attrs={'class':'form-control'}),
        }
        labels = {
            'name_foto_local': 'Descripción',
            'image_local': 'Select'
        }

class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        # fields = '__all__'
        fields = ['prop', 'direccion', 'referencia', 'provincia', 'municipio', 'sector', 'user']
        widgets = {
            'direccion': forms.TextInput(attrs={'autofocus':'', 'placeholder':' ...Calle y No. Casa | Apto | Planta.'}),
            'referencia': forms.TextInput(attrs={'placeholder':' ...Referir en camino para proximo destino.'}),

        }

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    phone = forms.CharField(max_length=11, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','autofocus':''}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\d{11}$', phone):
            raise forms.ValidationError("El número de teléfono debe tener 11 dígitos, solo números.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data