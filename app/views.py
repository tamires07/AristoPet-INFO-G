from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views import View
from django.contrib import messages
from .forms import *
from .models import Animal
from django.contrib.auth.hashers import check_password

class IndexView(View):
    def get(self, request, *args, **kwargs):
        animais = Animal.objects.all()  # pega todos os animais do banco
        return render(request, 'index.html', {'animais': animais})
    
    def get(self, request, *args, **kwargs):
        animais = Animal.objects.all()
        pessoa_id = request.session.get('pessoa_id')
        pessoa = Pessoa.objects.filter(id=pessoa_id).first()
        return render(request, 'index.html', {'animais': animais, 'pessoa': pessoa})


class PessoaView(View):
    def get(self, request, *args, **kwargs):
        pessoa = Pessoa.objects.all()
        return render(request, 'pessoa.html', {'pessoa':pessoa})
    
def cadastrar_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data_nasc = request.POST.get('data_nascimento')
        endereco = request.POST.get('endereco')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        telefone = request.POST.get('telefone')

        if Pessoa.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return redirect('cadastro')

        pessoa = Pessoa(
            nome=nome,
            data_nasc=data_nasc,
            endereco=endereco,
            telefone=telefone,
            email=email,
            senha=make_password(senha)  # 🔐 CORREÇÃO AQUI
        )
        pessoa.save()  # Remove o set_password() anterior

        request.session['pessoa_id'] = pessoa.id
        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('index')

    return render(request, 'pessoa.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        senha_digitada = request.POST.get('senha').strip()

        pessoa = Pessoa.objects.filter(email=email).first()

        if pessoa and check_password(senha_digitada, pessoa.senha):
            request.session['pessoa_id'] = pessoa.id
            messages.success(request, f'Bem-vindo(a), {pessoa.nome}!')
            return redirect('index')
        else:
            messages.error(request, 'Email ou senha incorretos.')

    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    messages.success(request, 'Você saiu da sua conta com sucesso.')
    return redirect('index')


def buscarView(request):
    query = request.GET.get('q', '')
    resultados = []
    if query:
        resultados = Animal.objects.filter(nome__icontains=query)  # busca no nome, exemplo
    return render(request, 'buscar.html', {'resultados': resultados, 'query': query})


def cadastrarAnimalView(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            animal = form.save(commit=False)

            pessoa_id = request.session.get('pessoa_id')
            if pessoa_id:
                animal.doador = Pessoa.objects.get(id=pessoa_id)
            else:
                messages.error(request, 'Você precisa estar logado para cadastrar um animal.')
                return redirect('login')

            animal.save()
            messages.success(request, 'Animal cadastrado com sucesso!')
            return redirect('index')
        else:
            messages.error(request, 'Erro no formulário. Verifique os dados.')
    else:
        form = AnimalForm()

    return render(request, 'cadastraranimal.html', {'form': form})


def deletarAnimalView(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    animal.delete()
    messages.success(request, 'Animal deletado com sucesso!')
    return redirect('index')

def detalhe_animal(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, 'detalhe_animal.html', {'animal': animal})