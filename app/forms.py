from django import forms
from .models import *
 
class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput)

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['nome', 'especie', 'genero', 'cidade', 'imagem', 'descricao']

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nome', 'instituicao', 'data_hora', 'local', 'cidade']
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['nome', 'data_nasc', 'endereco', 'email', 'telefone', 'imagem']