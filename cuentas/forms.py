from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['nombre_completo', 'documento', 'sexo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_completo'].widget.attrs.update({'placeholder': 'Nombre completo', 'class': 'input-field'})
        self.fields['documento'].widget.attrs.update({'placeholder': 'Documento de identidad', 'class': 'input-field'})
        self.fields['sexo'].widget.attrs.update({'class': 'input-field'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Contraseña', 'class': 'input-field'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirmar contraseña', 'class': 'input-field'})


class LoginForm(forms.Form):
    documento = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Documento de identidad', 'class': 'input-field'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'input-field'})
    )