from django import forms
from .models import *
 
class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput)

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['nome', 'especie', 'genero', 'cidade', 'descricao', 'imagem']

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nome', 'instituicao', 'data_hora', 'local', 'descricao']
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }