"""
settings.py - Configuracoes gerais do projeto Django.

Este e o arquivo central de configuracao. Aqui sao definidos:
- Banco de dados (MySQL)
- Apps instalados
- Middlewares (camadas de processamento de requisicao)
- Templates (onde o Django busca os HTMLs)
- Internacionalizacao (idioma e fuso horario)
- Seguranca (chave secreta, debug, CSRF)

O pacote de configuracao se chama 'setup' (renomeado do padrao 'sistemaweb').
As variaveis sensiveis (SECRET_KEY, senha do banco) vem do arquivo .env
usando a biblioteca python-dotenv, para nao expor senhas no codigo-fonte.
"""

from pathlib import Path

# BASE_DIR: Caminho absoluto da raiz do projeto (pasta que contem manage.py)
# Path(__file__) = caminho deste arquivo (setup/settings.py)
# .resolve() = caminho absoluto | .parent.parent = sobe 2 niveis (setup/ -> raiz/)
BASE_DIR = Path(__file__).resolve().parent.parent

import os
from dotenv import load_dotenv

# Carrega as variaveis de ambiente do arquivo .env na raiz do projeto
# Exemplo: SECRET_KEY, PASSWORD ficam disponiveis via os.getenv()
load_dotenv()

# Chave secreta usada pelo Django para criptografia (sessoes, tokens CSRF, etc.)
# NUNCA deve ser exposta publicamente em producao
SECRET_KEY = os.getenv('SECRET_KEY')

# Modo debug: mostra erros detalhados no navegador
# Deve ser False em producao por seguranca
DEBUG = os.getenv('DEBUG')

# Lista de dominios/IPs que podem acessar o sistema
# Em producao, colocar o dominio real (ex: 'meusistema.com.br')
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# =============================================
# APPS INSTALADOS
# =============================================
# Cada app e um modulo do Django que adiciona funcionalidades ao projeto.
# Os apps do Django (django.contrib.*) fornecem funcionalidades prontas.
INSTALLED_APPS = [
    # 'django.contrib.admin',       # Painel administrativo (desabilitado neste projeto)
    'django.contrib.auth',           # Sistema de autenticacao (User, login, logout, permissoes)
    'django.contrib.contenttypes',   # Rastreamento de tipos de modelo (usado internamente)
    'django.contrib.sessions',       # Gerenciamento de sessoes (manter usuario logado)
    'django.contrib.messages',       # Sistema de mensagens temporarias (flash messages)
    'django.contrib.staticfiles',    # Servir arquivos estaticos (CSS, JS, imagens)
    'sistemaweb',                    # Nosso app principal (membros e tarefas)
]

# =============================================
# MIDDLEWARES
# =============================================
# Middlewares sao funcoes que processam CADA requisicao HTTP antes de chegar
# na View, e CADA resposta antes de voltar ao navegador. Executam em ordem.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',         # Protecoes de seguranca (HTTPS, headers)
    'django.contrib.sessions.middleware.SessionMiddleware',  # Gerencia sessoes de usuario
    'django.middleware.common.CommonMiddleware',             # Configuracoes comuns (URL trailing slash)
    'django.middleware.csrf.CsrfViewMiddleware',             # Protecao contra ataques CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',# Associa o usuario logado a cada request
    'django.contrib.messages.middleware.MessageMiddleware',  # Mensagens entre requisicoes
    'django.middleware.clickjacking.XFrameOptionsMiddleware',# Protecao contra clickjacking
]

# Arquivo raiz de URLs do projeto (setup/urls.py)
# O Django comeca a resolver URLs a partir deste arquivo
ROOT_URLCONF = 'setup.urls'

# =============================================
# TEMPLATES
# =============================================
# Configuracao de como o Django encontra e processa os arquivos HTML
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Busca templates na pasta templates/ da raiz
        'APP_DIRS': True,                   # Tambem busca em cada app/templates/
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',  # Disponibiliza 'request' nos templates
                'django.contrib.auth.context_processors.auth',  # Disponibiliza 'user' nos templates
                'django.contrib.messages.context_processors.messages',  # Disponibiliza mensagens
            ],
        },
    },
]

# Aplicacao WSGI - ponto de entrada para servidores web em producao
WSGI_APPLICATION = 'setup.wsgi.application'


# =============================================
# BANCO DE DADOS
# =============================================
# Configuracao da conexao com o MySQL Server 8.0
# A senha vem do arquivo .env (variavel PASSWORD)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Driver MySQL
        'NAME': 'sistemaweb',                  # Nome do banco de dados
        'USER': 'root',                        # Usuario do MySQL
        'PASSWORD': os.getenv('PASSWORD'),     # Senha (vem do .env)
        'HOST': 'localhost',                   # Servidor (local)
        'PORT': '3306',                        # Porta padrao do MySQL
    }
}


# =============================================
# VALIDACAO DE SENHAS
# =============================================
# Regras que o Django aplica ao criar senhas de usuarios
# (minimo de caracteres, nao pode ser muito comum, etc.)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# =============================================
# INTERNACIONALIZACAO
# =============================================
# Idioma padrao: Portugues do Brasil
LANGUAGE_CODE = 'pt-BR'

# Fuso horario: Brasilia (UTC-3)
TIME_ZONE = 'America/Sao_Paulo'

# Ativa traducao de textos internos do Django para pt-BR
USE_I18N = True

# Ativa suporte a fuso horario (datas sao armazenadas em UTC no banco)
USE_TZ = True


# =============================================
# ARQUIVOS ESTATICOS
# =============================================
# URL base para acessar arquivos estaticos (CSS, JS, imagens)
# Exemplo: /static/sistemaweb/css/estilo.css
STATIC_URL = 'static/'

# Tipo padrao de chave primaria para novos modelos
# BigAutoField = inteiro de 64 bits com auto-incremento (1, 2, 3, ...)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
