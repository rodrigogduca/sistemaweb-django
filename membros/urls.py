from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_membros, name='listar_membros'),
    path('cadastrar/', views.cadastrar_membro, name='cadastrar_membro'),
    path('editar/<int:membro_id>/', views.editar_membro, name='editar_membro'),
    path('remover/<int:membro_id>/', views.remover_membro, name='remover_membro'),
    path('detalhes/<int:membro_id>/', views.detalhes_membro, name='detalhes_membro'),
    path('tarefa/editar/<int:tarefa_id>/', views.editar_tarefa, name='editar_tarefa'),
    path('tarefa/remover/<int:tarefa_id>/', views.remover_tarefa, name='remover_tarefa'),
]