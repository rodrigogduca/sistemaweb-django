"""
urls.py - Configuração raiz de URLs do projeto Django.

Este é o arquivo que o Django consulta primeiro ao receber uma requisição HTTP.
A variável ROOT_URLCONF em settings.py aponta para este arquivo ('setup.urls').

Funcionamento:
1. O Django recebe uma requisição HTTP (ex: GET /login/)
2. Consulta esta lista de urlpatterns de cima para baixo
3. Ao encontrar um padrão que corresponda, delega para o app correto
4. O app resolve a URL internamente e executa a View correspondente

A função include() delega a resolução de URLs para outro arquivo urls.py.
Isso permite que cada app seja independente e tenha suas próprias rotas.

Ordem dos includes:
- 'autenticacao.urls': rotas de login e logout (acesso público)
- 'sistemaweb.urls': rotas de membros e tarefas (acesso autenticado)
"""

from django.urls import path, include

urlpatterns = [
    # Rotas do app de autenticação (login, logout)
    path('', include('autenticacao.urls')),

    # Rotas do app principal (membros, tarefas)
    path('', include('sistemaweb.urls')),
]
