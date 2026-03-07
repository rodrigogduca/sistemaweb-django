# Sistema Web Django -- Gerenciamento de Membros e Tarefas

Sistema web didatico feito com Django para cadastrar, listar, editar e remover membros e suas tarefas. Utiliza Class-Based Views (POO), Tailwind CSS e autenticacao com login.

## Conceitos de Programacao Aplicados

Este projeto foi construido para demonstrar conceitos fundamentais de programacao:

### Programacao Orientada a Objetos (POO)
- **Classe**: Cada View e cada Model e uma classe (ex: `LoginView`, `Membro`)
- **Heranca**: As Views herdam de `View` (classe base do Django) e ganham funcionalidades prontas
- **Heranca Multipla**: Views protegidas usam `LoginRequiredMixin` + `View` juntas
- **Encapsulamento**: Cada classe cuida apenas da sua responsabilidade (login so faz login, etc.)
- **Metodo**: Funcoes dentro de classes (`get()`, `post()`) que definem o comportamento
- **Atributo**: Propriedades da classe (`login_url`, `template_name`) que configuram o comportamento

### Principios Basicos
- **Separacao de Interesses**: Autenticacao em um app, regras de negocio em outro
- **Responsabilidade Unica**: Cada classe faz apenas uma coisa
- **DRY (Don't Repeat Yourself)**: Reutilizamos funcoes do Django (`authenticate`, `login`, `logout`)
- **Variaveis**: Armazenam dados temporarios (nome, email, usuario)
- **Condicionais (if/else)**: Controlam o fluxo (admin vs membro, logado vs nao logado)
- **Estruturas de dados**: Dicionarios `{}` passam dados para os templates

## Arquitetura do Projeto (2 Apps)

O projeto e dividido em **2 apps Django**, cada um com sua responsabilidade:

```
  [Navegador] --> [setup/urls.py] --> [autenticacao/urls.py] --> Login/Logout
                                  |
                                  --> [sistemaweb/urls.py]   --> Membros/Tarefas
```

### App `autenticacao` -- Controle de Acesso
Responsavel por **quem pode entrar** no sistema:
- `LoginView`: Verifica usuario e senha, cria sessao
- `LogoutView`: Destroi a sessao do usuario
- Migration que cria o superusuario admin automaticamente

### App `sistemaweb` -- Regras de Negocio
Responsavel por **o que o sistema faz**:
- CRUD de Membros (Criar, Ler, Atualizar, Deletar)
- CRUD de Tarefas
- Controle de autorizacao (admin vs membro)
- Modelos de dados (Membro, Tarefa)

## Funcionalidades
- Tela de login com autenticacao do Django
- Controle de acesso: admin (superusuario) ve tudo, membro ve apenas suas tarefas
- Cadastro, listagem, edicao e remocao de membros (apenas admin)
- Cadastro, edicao e remocao de tarefas para cada membro
- Cada membro possui login proprio (usuario e senha)
- Interface com Tailwind CSS (via CDN)
- Views em Class-Based Views (POO) sem forms.py -- inputs manuais no HTML

## Tecnologias
- Python 3.14
- Django 3.2 LTS
- MySQL 5.7 (MAMP)
- Tailwind CSS (CDN)
- python-dotenv (variaveis de ambiente)

## Como rodar o projeto

1. **Clone o repositorio:**
	```
	git clone https://github.com/rodrigogduca/sistemaweb-django.git
	cd sistemaweb-django
	```

2. **Crie e ative o ambiente virtual:**
	```
	python -m venv venv
	.\venv\Scripts\activate
	```

3. **Instale as dependencias:**
	```
	pip install -r requirements.txt
	```

4. **Configure as variaveis de ambiente:**
	- Crie um arquivo `.env` na raiz do projeto com:
	```
	SECRET_KEY=sua_chave_secreta
	DEBUG=True
	DB_PASSWORD=root
	DB_PORT=3306
	```

5. **Inicie o MAMP e crie o banco de dados no phpMyAdmin:**
	```sql
	CREATE DATABASE sistemaweb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
	```

6. **Aplique as migracoes:**
	```
	python manage.py migrate
	```

	> **Nota:** Ao executar `migrate`, um superusuario padrao e criado automaticamente:
	> - **Usuario:** admin
	> - **Senha:** admin
	> - **Email:** admin@admin.com

7. **Rode o servidor:**
	```
	python manage.py runserver
	```

8. **Acesse no navegador:**
	- [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
	- Voce sera redirecionado para a tela de login.

## Estrutura do Projeto

```
sistemaweb-django/
|
|-- setup/                              # Pacote de configuracao do Django
|   |-- settings.py                     # Configuracoes (banco, apps, templates)
|   |-- urls.py                         # Rotas raiz (inclui URLs dos 2 apps)
|   |-- wsgi.py                         # Ponto de entrada WSGI (producao)
|   |-- asgi.py                         # Ponto de entrada ASGI (async)
|
|-- autenticacao/                       # App de autenticacao (login/logout)
|   |-- __init__.py                     # Marca a pasta como pacote Python
|   |-- apps.py                         # Configuracao do app (AutenticacaoConfig)
|   |-- views.py                        # LoginView e LogoutView (2 classes)
|   |-- urls.py                         # Rotas: /login/ e /logout/
|   |-- migrations/
|       |-- 0001_create_admin.py        # Cria superusuario admin automaticamente
|
|-- sistemaweb/                         # App principal (membros e tarefas)
|   |-- __init__.py                     # Marca a pasta como pacote Python
|   |-- models.py                       # Modelos de dados (Membro, Tarefa)
|   |-- views.py                        # 8 Class-Based Views (CRUD)
|   |-- urls.py                         # Rotas de membros e tarefas
|   |-- migrations/
|       |-- 0001_initial.py             # Cria tabelas Membro e Tarefa
|
|-- templates/
|   |-- autenticacao/
|   |   |-- login.html                  # Tela de login (formulario)
|   |-- sistemaweb/
|       |-- base.html                   # Template base (navbar + layout)
|       |-- index.html                  # Pagina inicial (admin)
|       |-- listar_membros.html         # Lista de membros (admin)
|       |-- cadastrar_membro.html       # Formulario de cadastro
|       |-- editar_membro.html          # Formulario de edicao
|       |-- detalhes_membro.html        # Detalhes + tarefas do membro
|       |-- remover_membro.html         # Confirmacao de remocao
|       |-- editar_tarefa.html          # Edicao de tarefa
|       |-- remover_tarefa.html         # Confirmacao de remocao de tarefa
|
|-- manage.py                           # Utilitario de linha de comando do Django
|-- requirements.txt                    # Dependencias do projeto
|-- .env                                # Variaveis de ambiente (nao versionado)
|-- .gitignore                          # Arquivos ignorados pelo Git
|-- LICENSE                             # Licenca MIT
```

## Fluxo de uma Requisicao HTTP

Para entender como o Django processa cada acesso:

```
1. Usuario acessa /login/ no navegador
2. Django consulta setup/urls.py
3. setup/urls.py delega para autenticacao/urls.py
4. autenticacao/urls.py encontra o padrao 'login/' -> LoginView
5. Django cria uma instancia de LoginView e chama dispatch()
6. dispatch() verifica o metodo HTTP (GET ou POST)
7. GET -> chama self.get() -> render() retorna o HTML
8. POST -> chama self.post() -> authenticate() + login() -> redirect()
```

## Mapa de URLs e Views

| URL | App | View | Acesso |
|-----|-----|------|--------|
| `/login/` | autenticacao | `LoginView` | Publico |
| `/logout/` | autenticacao | `LogoutView` | Publico |
| `/` | sistemaweb | `PaginaInicialView` | Logado |
| `/membros/` | sistemaweb | `ListarMembrosView` | Admin |
| `/cadastrar/` | sistemaweb | `CadastrarMembroView` | Admin |
| `/editar/<id>/` | sistemaweb | `EditarMembroView` | Admin/Dono |
| `/remover/<id>/` | sistemaweb | `RemoverMembroView` | Admin |
| `/detalhes/<id>/` | sistemaweb | `DetalhesMembroView` | Admin/Dono |
| `/tarefa/editar/<id>/` | sistemaweb | `EditarTarefaView` | Admin/Dono |
| `/tarefa/remover/<id>/` | sistemaweb | `RemoverTarefaView` | Admin/Dono |

## Observacoes
- O projeto utiliza autenticacao com login/logout separada em app proprio.
- Todas as paginas sao protegidas -- so usuarios logados acessam o sistema.
- Nao utiliza forms.py -- os inputs sao escritos direto no HTML e tratados na view.
- O painel administrativo do Django esta desabilitado.
- Utiliza `legacy-cgi` para compatibilidade entre Django 3.2 e Python 3.14.
- Todos os arquivos Python possuem docstrings explicativas para fins didaticos.

---
Feito para fins didaticos.
