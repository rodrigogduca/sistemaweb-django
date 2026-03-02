"""
apps.py - Configuracao do aplicativo 'sistemaweb'.

Todo app Django precisa de uma classe de configuracao que herda de AppConfig.
Ela define metadados do app, como o nome e o tipo de chave primaria padrao.
O Django usa essa classe para registrar, carregar e identificar o app.

Este arquivo e criado automaticamente pelo comando 'startapp' do Django e
normalmente nao precisa ser alterado, a menos que se queira customizar
o comportamento do app (ex: signals, nome de exibicao, etc.).
"""

from django.apps import AppConfig


class SistemawebConfig(AppConfig):
    """
    Classe de configuracao do app 'sistemaweb'.

    - default_auto_field: Define que novos modelos usam BigAutoField
      (inteiro de 64 bits) como chave primaria automatica (id).
    - name: Nome do app. Deve corresponder ao nome da pasta do app.
      O Django usa esse nome para encontrar models, views, templates, etc.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sistemaweb'
