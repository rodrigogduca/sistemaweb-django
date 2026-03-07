"""
apps.py - Configuração do app 'autenticacao'.

Todo app Django precisa de um arquivo apps.py que define sua configuração.
Essa classe é referenciada no INSTALLED_APPS do settings.py para que o Django
reconheça e carregue o app ao iniciar o projeto.

Conceitos de POO:
- HERANÇA: AutenticacaoConfig herda de AppConfig (classe base do Django).
  Isso significa que ela "ganha" todo o comportamento padrão de configuração
  e só precisa definir os atributos específicos deste app.
- ATRIBUTOS DE CLASSE: 'default_auto_field' e 'name' são propriedades da classe
  que o Django lê automaticamente ao registrar o app.
"""

from django.apps import AppConfig


class AutenticacaoConfig(AppConfig):
    """
    Classe de configuração do app 'autenticacao'.

    Atributos:
        default_auto_field: tipo padrão para chaves primárias automáticas.
            BigAutoField gera IDs inteiros grandes (bigint no banco).
        name: nome do app, deve corresponder ao nome da pasta do app.
            O Django usa esse nome para encontrar models, migrations, etc.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'autenticacao'
