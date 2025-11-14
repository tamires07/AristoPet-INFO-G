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
    path('animal/<int:pk>/', detalhe_animal, name='detalheanimal'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)