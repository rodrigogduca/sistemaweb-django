"""
urls.py - Definição das rotas (URLs) do aplicativo sistemaweb.

Cada path() conecta um endereço URL a uma View (classe).
Quando o usuário acessa uma URL no navegador, o Django percorre esta lista
de cima para baixo até encontrar um padrão que corresponda, e então
executa a View associada.

Parâmetros do path():
- Primeiro argumento: o padrão da URL (ex: 'login/', 'editar/<int:membro_id>/')
- Segundo argumento: a View que será executada (Classe.as_view())
- name: nome interno usado nos templates ({% url 'nome' %}) e nos redirects das views

Exemplo de uso nos templates:
  <a href="{% url 'login' %}">Login</a>  -->  gera o link /login/

Exemplo de uso nas views:
  return redirect('login')  -->  redireciona para /login/

O <int:membro_id> captura um número inteiro da URL e passa como parâmetro
para o método da View (ex: def get(self, request, membro_id)).
"""

from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    PaginaInicialView,
    ListarMembrosView,
    CadastrarMembroView,
    EditarMembroView,
    RemoverMembroView,
    DetalhesMembroView,
    EditarTarefaView,
    RemoverTarefaView,
)

urlpatterns = [
    # Autenticação
    path('login/', LoginView.as_view(), name='login'),       # Tela de login
    path('logout/', LogoutView.as_view(), name='logout'),     # Encerra sessão

    # Página inicial (rota raiz)
    path('', PaginaInicialView.as_view(), name='index'),

    # CRUD de Membros
    path('membros/', ListarMembrosView.as_view(), name='listar_membros'),                   # Lista todos (admin)
    path('cadastrar/', CadastrarMembroView.as_view(), name='cadastrar_membro'),             # Cadastra novo (admin)
    path('editar/<int:membro_id>/', EditarMembroView.as_view(), name='editar_membro'),      # Edita (dono ou admin)
    path('remover/<int:membro_id>/', RemoverMembroView.as_view(), name='remover_membro'),   # Remove (admin)
    path('detalhes/<int:membro_id>/', DetalhesMembroView.as_view(), name='detalhes_membro'),# Detalhes + tarefas

    # CRUD de Tarefas
    path('tarefa/editar/<int:tarefa_id>/', EditarTarefaView.as_view(), name='editar_tarefa'),   # Edita tarefa
    path('tarefa/remover/<int:tarefa_id>/', RemoverTarefaView.as_view(), name='remover_tarefa'), # Remove tarefa
]
