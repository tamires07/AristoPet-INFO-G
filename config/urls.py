from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', login_view, name='login'),
    path('pessoa/', PessoaView.as_view(), name='pessoa'),
    path('buscar/', buscarView, name='buscar'),
    path('cadastraranimal/', cadastrarAnimalView, name='cadastraranimal'),
    path('deletaranimal/<int:pk>/', deletarAnimalView, name='deletaranimal'),
    path('cadastro/', cadastrar_usuario, name='cadastro'),
    path('logout/', logout_view, name='logout'),
    path('animal/<int:pk>/', detalheAnimal, name='detalheanimal'),
    path('editar-animal/<int:pk>/', editarAnimalView, name='editaranimal'),
    path('evento/', evento_view, name='evento'),
    path('evento/criar/', criar_evento_view, name='criar_evento'),  

    path('evento/editar/<int:evento_id>/', editar_evento_view, name='editar_evento'),

    path('perfil/', perfil_usuario, name='perfil'),
    path('perfil/editar/', editar_perfil_view, name='editar_perfil'),
    path('perfil/excluir/', excluir_perfil_view, name='excluir_perfil'),
    path('quero-adotar/<int:animal_id>/', quero_adotar_view, name='quero_adotar'),
    path('chat/<int:conversa_id>/', chat_view, name='chat'),
    path('minhas-conversas/', minhas_conversas_view, name='minhas_conversas'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)