from django import forms
from .models import Aluno
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = '__all__'
