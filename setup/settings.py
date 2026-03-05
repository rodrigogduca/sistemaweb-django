"""
settings.py - Configurações gerais do projeto Django.

Este é o arquivo central de configuração. Aqui são definidos:
- Banco de dados (MAMP + MySQL)
- Apps instalados
- Middlewares (camadas de processamento de requisição)
- Templates (onde o Django busca os HTMLs)
- Internacionalização (idioma e fuso horário)
- Segurança (chave secreta, debug, CSRF)

O pacote de configuração se chama 'setup' (renomeado do padrão 'sistemaweb').
As variáveis sensíveis (SECRET_KEY, senha do banco) vem do arquivo .env
usando a biblioteca python-dotenv, para não expor senhas no código-fonte.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# BASE_DIR: Caminho absoluto da raiz do projeto (pasta que contém manage.py)
# Path(__file__) = caminho deste arquivo (setup/settings.py)
# .resolve() = caminho absoluto | .parent.parent = sobe 2 níveis (setup/ -> raiz/)
BASE_DIR = Path(__file__).resolve().parent.parent


# Carrega as variáveis de ambiente do arquivo .env na raiz do projeto
# Exemplo: SECRET_KEY, PASSWORD ficam disponíveis via os.getenv()
load_dotenv()

# Chave secreta usada pelo Django para criptografia (sessões, tokens CSRF, etc.)
# NUNCA deve ser exposta publicamente em produção
SECRET_KEY = os.getenv('SECRET_KEY')

# Modo debug: mostra erros detalhados no navegador
# Deve ser False em produção por segurança
DEBUG = os.getenv('DEBUG')

# Lista de domínios/IPs que podem acessar o sistema
# Em produção, colocar o domínio real (ex: 'meusistema.com.br')
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# =============================================
# APPS INSTALADOS
# =============================================
# Cada app é um módulo do Django que adiciona funcionalidades ao projeto.
# Os apps do Django (django.contrib.*) fornecem funcionalidades prontas.
INSTALLED_APPS = [
    # 'django.contrib.admin',       # Painel administrativo (desabilitado neste projeto)
    # 'django.contrib.messages',       # Sistema de mensagens temporárias (flash messages)
    # 'django.contrib.staticfiles',    # Servir arquivos estáticos (CSS, JS, imagens)
    'django.contrib.auth',           # Sistema de autenticação (User, login, logout, permissões)
    'django.contrib.contenttypes',   # Rastreamento de tipos de modelo (usado internamente)
    'django.contrib.sessions',       # Gerenciamento de sessões (manter usuário logado)
    'sistemaweb',                    # Nosso app principal (membros e tarefas)
]

# =============================================
# MIDDLEWARES
# =============================================
# Middlewares são funções que processam CADA requisição HTTP antes de chegar
# na View, e CADA resposta antes de voltar ao navegador. Executam em ordem.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',         # Proteções de segurança (HTTPS, headers)
    'django.contrib.sessions.middleware.SessionMiddleware',  # Gerencia sessões de usuário
    'django.middleware.common.CommonMiddleware',             # Configurações comuns (URL trailing slash)
    'django.middleware.csrf.CsrfViewMiddleware',             # Proteção contra ataques CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',# Associa o usuário logado a cada request
    'django.contrib.messages.middleware.MessageMiddleware',  # Mensagens entre requisições
    'django.middleware.clickjacking.XFrameOptionsMiddleware',# Proteção contra clickjacking
]

# Arquivo raiz de URLs do projeto (setup/urls.py)
# O Django começa a resolver URLs a partir deste arquivo
ROOT_URLCONF = 'setup.urls'

# =============================================
# TEMPLATES
# =============================================
# Configuração de como o Django encontra e processa os arquivos HTML
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Busca templates na pasta templates/ da raiz
        'APP_DIRS': True,                   # Também busca em cada app/templates/
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',  # Disponibiliza 'request' nos templates
                'django.contrib.auth.context_processors.auth',  # Disponibiliza 'user' nos templates
                'django.contrib.messages.context_processors.messages',  # Disponibiliza mensagens
            ],
        },
    },
]

# Aplicação WSGI - ponto de entrada para servidores web em produção
WSGI_APPLICATION = 'setup.wsgi.application'


# =============================================
# BANCO DE DADOS
# =============================================
# Configuração da conexão com o MySQL via MAMP
# A senha e a porta vem do arquivo .env (variáveis DB_PASSWORD e DB_PORT)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Driver MySQL
        'NAME': 'sistemaweb',                  # Nome do banco de dados
        'USER': 'root',                        # Usuário do MySQL
        'PASSWORD': os.getenv('DB_PASSWORD'),   # Senha (vem do .env)
        'HOST': 'localhost',                   # Servidor (local)
        'PORT': os.getenv('DB_PORT'),  # Porta do MAMP
    }
}


# =============================================
# VALIDAÇÃO DE SENHAS
# =============================================
# Regras que o Django aplica ao criar senhas de usuários
# (mínimo de caracteres, não pode ser muito comum, etc.)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# =============================================
# INTERNACIONALIZAÇÃO
# =============================================
# Idioma padrão: Português do Brasil
LANGUAGE_CODE = 'pt-BR'

# Fuso horário: Brasília (UTC-3)
TIME_ZONE = 'America/Sao_Paulo'

# Ativa tradução de textos internos do Django para pt-BR
USE_I18N = True

# Ativa suporte a fuso horário (datas são armazenadas em UTC no banco)
USE_TZ = True


# =============================================
# CAMPO ID PADRÃO
# =============================================
# Define o tipo de chave primária (id) para novos modelos
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =============================================
# ARQUIVOS ESTÁTICOS
# =============================================
# URL base para acessar arquivos estáticos (CSS, JS, imagens)
#STATIC_URL = 'static/'
