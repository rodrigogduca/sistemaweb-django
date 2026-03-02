from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    IndexView,
    ListarMembrosView,
    CadastrarMembroView,
    EditarMembroView,
    RemoverMembroView,
    DetalhesMembroView,
    EditarTarefaView,
    RemoverTarefaView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', IndexView.as_view(), name='index'),
    path('membros/', ListarMembrosView.as_view(), name='listar_membros'),
    path('cadastrar/', CadastrarMembroView.as_view(), name='cadastrar_membro'),
    path('editar/<int:membro_id>/', EditarMembroView.as_view(), name='editar_membro'),
    path('remover/<int:membro_id>/', RemoverMembroView.as_view(), name='remover_membro'),
    path('detalhes/<int:membro_id>/', DetalhesMembroView.as_view(), name='detalhes_membro'),
    path('tarefa/editar/<int:tarefa_id>/', EditarTarefaView.as_view(), name='editar_tarefa'),
    path('tarefa/remover/<int:tarefa_id>/', RemoverTarefaView.as_view(), name='remover_tarefa'),
]
