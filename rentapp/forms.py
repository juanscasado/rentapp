import datetime
from django import forms
from .models import *


class RentaForm(forms.ModelForm):
    class Meta:
        model = Renta
        fields = ['user', 'direccion', 'sector', 'municipio', 'provincia', 'referencia']
        # fields = "__all__"
        # widgets = {
            
        #     'user': forms.Select(attrs={'style':'margin:10px 10px 10px 0px;','class':'form-control '}),
        #     'direccion': forms.TextInput(attrs={'style':'margin:10px 10px 10px 0px;', 'class':'form-control ','placeholder': 'ex: 23, nombre Calle...'}),
        #     'referencia': forms.TextInput(attrs={'style':'margin:10px 10px 10px 0px;','class':'form-control ','placeholder': 'ex: Lugar de referencia...'}),
        #     'provincia': forms.Select(attrs={'class':'form-control '}),
        #     'municipio': forms.Select(attrs={'class':'form-control '}),
        #     'sector': forms.Select(attrs={'class':'form-control '}),
            
        #     }
        # labels = {
        #     'user': 'Usuario',
        # }
class FotoForm(forms.ModelForm):
    class Meta:
        model = Foto
        # fields = "__all__"
        fields = ['renta', 'image_renta', 'name_foto_renta']
        widgets = {
            'renta': forms.Select(attrs={'style':'margin:10px 10px 10px 0px;','class':'form-control '}),
            'image_renta': forms.FileInput(attrs={'title':'Asd','style':'margin:10px 0px 10px 10px;','class':'form-control form-control-md '}),
            'name_foto_renta': forms.TextInput(attrs={'style':'margin:10px 10px 10px 0px;','class':'form-control ', 'placeholder': 'ex: Descripción Foto.'}),
        }
        labels = {
            'name_foto_renta': 'Descripción',
            'image_renta': 'Select'
        }

class RentaForm(forms.ModelForm):
    class Meta:
        model = Renta
        fields = '__all__'
        

import re


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    phone_number = forms.CharField(max_length=12, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'phone_number']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'^\d{12}$', phone_number):
            raise forms.ValidationError("El número de teléfono debe tener 12 dígitos.")
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data