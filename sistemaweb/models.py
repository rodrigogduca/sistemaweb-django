"""
models.py - Definicao dos modelos de dados do sistema.

Este arquivo define as tabelas do banco de dados usando o ORM do Django.
Cada classe representa uma tabela no MySQL. O Django converte automaticamente
esses modelos em tabelas com o prefixo 'sistemaweb_' (ex: sistemaweb_membro).

Conceitos usados:
- models.Model: Classe base do Django que transforma a classe Python em tabela SQL
- CharField: Campo de texto com tamanho maximo definido
- EmailField: Campo de email com validacao automatica
- DateTimeField: Campo de data/hora
- OneToOneField: Relacao um-para-um entre tabelas
- ForeignKey: Relacao muitos-para-um entre tabelas
"""

from django.db import models
from django.contrib.auth.models import User


class Membro(models.Model):
    """
    Modelo que representa um membro (pessoa) no sistema.

    Cada membro possui um nome, email unico e data de criacao automatica.
    O campo 'user' conecta o membro a um usuario do Django (modelo User),
    permitindo que o membro faca login no sistema. Essa relacao e OneToOne
    (um-para-um): cada usuario do Django pode estar vinculado a no maximo
    um membro, e cada membro a no maximo um usuario.

    Tabela no banco: sistemaweb_membro
    """

    # Relacao um-para-um com o modelo User do Django (sistema de autenticacao)
    # on_delete=CASCADE: se o User for deletado, o Membro tambem e deletado
    # null=True e blank=True permitem membros sem usuario vinculado
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    # Nome completo do membro (maximo 100 caracteres)
    nome = models.CharField(max_length=100)

    # Email do membro - unique=True garante que nao pode repetir no banco
    email = models.EmailField(unique=True)

    # Data e hora em que o membro foi cadastrado (preenchido automaticamente)
    # auto_now_add=True: Django preenche com a data/hora atual ao criar o registro
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Retorna o nome do membro como representacao em texto."""
        return self.nome


class Tarefa(models.Model):
    """
    Modelo que representa uma tarefa atribuida a um membro.

    Cada tarefa tem titulo, descricao, status (pendente ou concluida),
    data de criacao e uma referencia ao membro dono da tarefa.
    A relacao ForeignKey (muitos-para-um) significa que um membro pode
    ter varias tarefas, mas cada tarefa pertence a apenas um membro.
    Ao deletar um membro, todas as suas tarefas sao removidas (CASCADE).

    Tabela no banco: sistemaweb_tarefa
    """

    # Titulo da tarefa (maximo 200 caracteres)
    titulo = models.CharField(max_length=200)

    # Descricao detalhada da tarefa (blank=True: pode ficar em branco)
    descricao = models.TextField(blank=True)

    # Status da tarefa: 'pendente' (padrao) ou 'concluida'
    # choices define as opcoes validas que aparecem no sistema
    status = models.CharField(
        max_length=20,
        choices=[('pendente', 'Pendente'), ('concluida', 'Concluída')],
        default='pendente'
    )

    # Data e hora de criacao da tarefa (preenchido automaticamente)
    data_criacao = models.DateTimeField(auto_now_add=True)

    # Chave estrangeira (ForeignKey) - liga esta tarefa a um membro especifico
    # on_delete=CASCADE: se o membro for deletado, suas tarefas tambem sao
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE)

    def __str__(self):
        """Retorna o titulo da tarefa como representacao em texto."""
        return self.titulo
