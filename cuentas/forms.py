from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, DiaEntrenamiento, Ejercicio


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

class ConfigurarDiasForm(forms.Form):
    DIAS_CHOICES = DiaEntrenamiento.DIAS_CHOICES

    dias = forms.MultipleChoiceField(
        choices=DIAS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="¿Qué días entrenas?"
    )
    parte_cuerpo = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Pecho y tríceps', 'class': 'input-field'}),
        label="¿Qué parte del cuerpo vas a trabajar?"
    )


class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = ['nombre', 'repeticiones']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del ejercicio', 'class': 'input-field'}),
            'repeticiones': forms.TextInput(attrs={'placeholder': 'Ej: 4x12', 'class': 'input-field'}),
        }