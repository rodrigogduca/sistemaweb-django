
from django.urls import path, include

urlpatterns = [
    # Rotas do app de autenticação (login, logout)
    path('', include('autenticacao.urls')),

    # Rotas do app principal (membros, tarefas)
    path('', include('sistemaweb.urls')),
]
