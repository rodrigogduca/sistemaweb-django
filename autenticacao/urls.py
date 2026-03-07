"""
urls.py - Rotas (URLs) do app de autenticação.

Este arquivo mapeia URLs para Views do app 'autenticacao'.
Apenas duas rotas simples: login e logout.

Quando o Django recebe uma requisição HTTP, ele percorre a lista de urlpatterns
de cima para baixo até encontrar um padrão que corresponda à URL acessada.
Ao encontrar, executa a View associada.

Conceito de POO: as_view()
    .as_view() é um método de classe (classmethod) que converte a classe View
    em uma função que o Django pode chamar. Internamente, ele:
    1. Cria uma instância da classe (objeto)
    2. Chama o método dispatch() do objeto
    3. dispatch() verifica se é GET ou POST e chama self.get() ou self.post()

Parâmetros do path():
    - Primeiro argumento: padrão da URL (string)
    - Segundo argumento: a View que trata a requisição
    - name: nome interno usado para gerar URLs nos templates e redirects
"""

from django.urls import path
from .views import LoginView, LogoutView

urlpatterns = [
    # Rota de login: /login/
    # Quando acessar /login/, o Django executa LoginView
    path('login/', LoginView.as_view(), name='login'),

    # Rota de logout: /logout/
    # Quando acessar /logout/, o Django executa LogoutView
    path('logout/', LogoutView.as_view(), name='logout'),
]
