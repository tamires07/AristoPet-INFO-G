from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views import View
from django.contrib import messages
from .forms import *
from .models import Animal
from django.contrib.auth.hashers import check_password
from datetime import datetime

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
    query = request.GET.get('q', '').strip()  
    
    resultados_animais = Animal.objects.filter(nome__icontains=query)

    resultados_eventos = Evento.objects.filter(nome__icontains=query)

    return render(request, 'buscar.html', {
        'query': query,
        'resultados_animais': resultados_animais,
        'resultados_eventos': resultados_eventos,
    })


def cadastrarAnimalView(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            animal = form.save(commit=False)

            pessoa_id = request.session.get('pessoa_id')
            if pessoa_id:
                animal.doador = Pessoa.objects.get(id=pessoa_id)
            else:
                messages.error(request, 'Você precisa estar logado para cadastrar um animal.', extra_tags='login')
                return redirect('login')

            animal.save()
            messages.success(request, 'Animal cadastrado com sucesso!', extra_tags='animal_success')
            return redirect('cadastraranimal')
        else:
            messages.error(request, 'Erro no formulário. Verifique os dados.', extra_tags='animal_error')
    else:
        form = AnimalForm()

    return render(request, 'cadastraranimal.html', {'form': form})


def deletarAnimalView(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    
    pessoa_id = request.session.get('pessoa_id')
    
    if not pessoa_id:
        messages.error(request, 'Você precisa estar logado para executar esta ação.')
        return redirect('login')
    
    if pessoa_id != animal.doador.id:
        messages.error(request, 'Você só pode excluir seus próprios animais.')
        return redirect('index')
    
    animal.delete()
    messages.success(request, 'Animal excluído com sucesso!')
    return redirect('perfil')

def detalheAnimal(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, 'detalhe_animal.html', {'animal': animal})

def editarAnimalView(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    
    pessoa_id = request.session.get('pessoa_id')
    if pessoa_id != animal.doador.id:
        messages.error(request, 'Você só pode editar seus próprios animais.')
        return redirect('index')
    
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Animal atualizado com sucesso!')
    else:
        form = AnimalForm(instance=animal)
    
    return render(request, 'editar_animal.html', {'form': form, 'animal': animal})

def eventos(request, id=None):
    if id:
        evento = get_object_or_404(Evento, id=id)
    else:
        evento = None

    if request.method == "POST":
        nome = request.POST["nome"]
        instituicao = request.POST["instituicao"]
        data_hora_str = request.POST.get("data_hora", "")
        if data_hora_str:
            data_hora = datetime.strptime(data_hora_str, "%Y-%m-%dT%H:%M")
        else:
            data_hora = None 

        local = request.POST["local"]
        descricao = request.POST["descricao"]

        if evento:
            evento.nome = nome
            evento.instituicao = instituicao
            evento.data_hora = data_hora
            evento.local = local
            evento.descricao = descricao
            evento.save()
        else:
            Evento.objects.create(
                nome=nome,
                instituicao=instituicao,
                data_hora=data_hora,
                local=local,
                descricao=descricao,
            )
        return redirect("evento")

    eventos = Evento.objects.all()

    return render(request, "evento.html", {
        "evento": evento,
        "eventos": eventos,
    })

def perfil_usuario(request):
    pessoa_id = request.session.get('pessoa_id')
    if not pessoa_id:
        messages.error(request, 'Você precisa estar logado para acessar o perfil.')
        return redirect('login')
    
    pessoa = get_object_or_404(Pessoa, id=pessoa_id)
    
    animais_usuario = Animal.objects.filter(doador=pessoa)
    
    context = {
        'pessoa': pessoa,
        'animais': animais_usuario
    }
    
    return render(request, 'perfil.html', context)