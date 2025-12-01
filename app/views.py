from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views import View
from django.contrib import messages
from .forms import *
from .models import Animal, Pessoa, Conversa, Mensagem
from django.contrib.auth.hashers import check_password
from datetime import datetime
from django.utils import timezone

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
            senha=make_password(senha)
        )
        pessoa.save()

        request.session['pessoa_id'] = pessoa.id
        messages.success(request, 'Cadastro realizado com sucesso!', extra_tags='cadastro_sucesso')
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

    from django.db.models import Q
    
    resultados_animais = Animal.objects.filter(Q(especie__icontains=query) | Q(nome__icontains=query))

    resultados_evento = Evento.objects.filter(nome__icontains=query)

    resultados_usuario = Pessoa.objects.filter(nome__icontains=query)

    return render(request, 'buscar.html', {
        'query': query,
        'resultados_animais': resultados_animais,
        'resultados_evento': resultados_evento,
        'resultados_usuario': resultados_usuario,
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
            return redirect('index')
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
    
    if request.method == 'POST':
        confirmacao = request.POST.get('confirmacao')
        if confirmacao == 'EXCLUIR':
            if animal.imagem:
                animal.imagem.delete(save=False)
            
            nome_animal = animal.nome
            animal.delete()
            
            messages.success(request, f'Animal "{nome_animal}" excluído com sucesso!')
            return redirect('index')
    else:
        return render(request, 'confirmar_exclusao_animal.html', {'animal': animal})


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
            messages.success(request, 'Animal atualizado com sucesso!', extra_tags="atualizaranimal_success")
            return redirect('index')
    else:
        form = AnimalForm(instance=animal)
    
    return render(request, 'editar_animal.html', {'form': form, 'animal': animal})


def evento_view(request):
    eventos = Evento.objects.all().order_by('data_hora')
    
    context = {
        'eventos': eventos
    }
    return render(request, 'evento.html', context)


def criar_evento_view(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        instituicao = request.POST.get('instituicao')
        data_hora = request.POST.get('data_hora')
        local = request.POST.get('local')
        cidade = request.POST.get('cidade')
        site_instituicao = request.POST.get('site_instituicao')
        
        evento = Evento.objects.create(
            nome=nome,
            instituicao=instituicao,
            data_hora=data_hora,
            local=local,
            cidade=cidade,
            site_instituicao=site_instituicao,
        )
        
        messages.success(request, 'Evento criado com sucesso!', extra_tags='evento_sucesso')
        return redirect('evento')
    
    return render(request, 'evento.html')


def detalhe_evento_view(request, evento_id):
    try:
        evento = Evento.objects.get(id=evento_id)
    except Evento.DoesNotExist:
        messages.error(request, 'Evento não encontrado!')
        return redirect('evento')
    
    context = {
        'evento': evento
    }
    return render(request, 'detalhe_evento.html', context)



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


def editar_perfil_view(request):
    pessoa_id = request.session.get('pessoa_id')
    if not pessoa_id:
        messages.error(request, 'Você precisa estar logado.')
        return redirect('login')
    
    pessoa = get_object_or_404(Pessoa, id=pessoa_id)
    
    if request.method == 'POST':
        form = PessoaForm(request.POST, request.FILES, instance=pessoa)
        
        if Pessoa.objects.filter(email=pessoa.email).exclude(id=pessoa.id).exists():
            messages.error(request, 'Este email já está em uso.')
        else:
            pessoa.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    
    return render(request, 'editar_perfil.html', {'pessoa': pessoa})


def excluir_perfil_view(request):
    pessoa_id = request.session.get('pessoa_id')
    if not pessoa_id:
        messages.error(request, 'Você precisa estar logado.')
        return redirect('login')
    
    pessoa = get_object_or_404(Pessoa, id=pessoa_id)
    
    if request.method == 'POST':
        confirmacao = request.POST.get('confirmacao')
        if confirmacao == 'EXCLUIR':
            Animal.objects.filter(doador=pessoa).delete()
            
            if 'pessoa_id' in request.session:
                del request.session['pessoa_id']
            
            pessoa.delete()
            
            messages.success(request, 'Sua conta foi excluída com sucesso.')
            return redirect('index')
        else:
            messages.error(request, 'Confirmação incorreta.')
    
    return render(request, 'excluir_perfil.html', {'pessoa': pessoa})

def quero_adotar_view(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    adotante = get_object_or_404(Pessoa, id=request.session.get('pessoa_id'))
    
    conversa_existente = Conversa.objects.filter(
        animal=animal,
        participante_adotante=adotante
    ).first()
    
    if conversa_existente:
        return redirect('chat', conversa_id=conversa_existente.id)
    
    conversa = Conversa.objects.create(
        animal=animal,
        participante_doador=animal.doador,
        participante_adotante=adotante
    )
    
    Mensagem.objects.create(
        conversa=conversa,
        remetente=animal.doador,
        texto=f"Olá! Obrigado pelo interesse em adotar o {animal.nome}. Como posso ajudar?"
    )
    
    messages.success(request, f'Conversa iniciada com {animal.doador.nome}!')
    return redirect('chat', conversa_id=conversa.id)


def chat_view(request, conversa_id):
    conversa = get_object_or_404(Conversa, id=conversa_id)
    pessoa_logada = get_object_or_404(Pessoa, id=request.session.get('pessoa_id'))
    
    if pessoa_logada not in [conversa.participante_doador, conversa.participante_adotante]:
        messages.error(request, 'Você não tem acesso a esta conversa.')
        return redirect('index')
    
    if request.method == 'POST':
        texto = request.POST.get('mensagem')
        if texto:
            Mensagem.objects.create(
                conversa=conversa,
                remetente=pessoa_logada,
                texto=texto
            )
            return redirect('chat', conversa_id=conversa_id)
    
    mensagens = Mensagem.objects.filter(conversa=conversa)
    
    context = {
        'conversa': conversa,
        'mensagens': mensagens,
        'pessoa_logada': pessoa_logada,
    }
    
    return render(request, 'chat.html', context)


def minhas_conversas_view(request):
    pessoa_logada = get_object_or_404(Pessoa, id=request.session.get('pessoa_id'))
    
    conversas = Conversa.objects.filter(
        models.Q(participante_doador=pessoa_logada) |
        models.Q(participante_adotante=pessoa_logada)
    ).order_by('-data_criacao')


    mensagens_nao_lidas = 0
    for conversa in conversas:
        mensagens_nao_lidas += conversa.mensagens.filter(
            lida=False
        ).exclude(remetente=pessoa_logada).count()
    
    context = {
        'conversas': conversas,
        'pessoa_logada': pessoa_logada,
        'mensagens_nao_lidas': mensagens_nao_lidas
    }
    
    return render(request, 'minhas_conversas.html', context)