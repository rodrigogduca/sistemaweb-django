"""
views.py - Lógica de controle das páginas (Views) do app 'sistemaweb'.

Este arquivo contém APENAS as Views de membros e tarefas (regras de negócio).
A autenticação (login/logout) está no app 'autenticacao', seguindo o princípio
de Separação de Interesses (Separation of Concerns):
    - autenticacao/views.py -> cuida de login e logout (quem é o usuário?)
    - sistemaweb/views.py   -> cuida de membros e tarefas (o que o usuário faz?)

Conceitos de Programação Orientada a Objetos (POO) usados neste arquivo:

1. CLASSE (class): Um "molde" para criar objetos. Cada View é uma classe.
   Exemplo: ListarMembrosView é uma classe que sabe listar membros.

2. HERANÇA: Todas as Views herdam de View (classe base do Django).
   Com o LoginRequiredMixin, usamos herança múltipla — a View ganha
   tanto o comportamento de View quanto a proteção de login.
   Ordem de herança: (LoginRequiredMixin, View) — o mixin vem primeiro.

3. MÉTODO: Funções definidas dentro de uma classe (get, post).
   O parâmetro 'self' é uma referência ao próprio objeto (instância).

4. ENCAPSULAMENTO: Cada classe cuida apenas da sua responsabilidade.
   EditarMembroView só edita membros. RemoverTarefaView só remove tarefas.

Conceitos básicos de programação:
- Variáveis: armazenam dados (nome, email, membro_id)
- Condicionais (if/else): controlam o fluxo conforme a lógica de negócio
- Estrutura de dados: dicionários {} passam dados para os templates
- Funções: get_object_or_404() encapsula a busca + tratamento de erro

Controle de acesso (autorização):
- Superusuário (admin): acessa tudo
- Membro comum: só acessa seus próprios dados e tarefas
- Visitante não logado: redirecionado para login pelo LoginRequiredMixin
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Membro, Tarefa


class PaginaInicialView(LoginRequiredMixin, View):
    """
    View da página inicial do sistema (rota raiz '/').

    Protegida por LoginRequiredMixin: usuário não logado é redirecionado para login.

    GET:
    - Superusuário: exibe a página inicial com boas-vindas e links de navegação
    - Membro comum: redireciona para sua página de detalhes (suas tarefas)
    - Usuário sem membro vinculado: faz logout por segurança

    login_url: define para onde redirecionar se o usuário não estiver logado.
    """
    login_url = 'login'

    def get(self, request):
        """Exibe página inicial (admin) ou redireciona para detalhes (membro)."""
        # Superusuário vê a página inicial completa
        if request.user.is_superuser:
            return render(request, 'sistemaweb/index.html')

        # Membro comum é redirecionado para sua própria página de detalhes
        try:
            membro = Membro.objects.get(user=request.user)
            return redirect('detalhes_membro', membro_id=membro.id)
        except Membro.DoesNotExist:
            # Segurança: se não tem membro vinculado, encerra a sessão
            logout(request)
            return redirect('login')


class ListarMembrosView(LoginRequiredMixin, View):
    """
    View para listar todos os membros cadastrados.

    Acesso: APENAS superusuário (admin). Membros comuns são redirecionados.

    GET: Busca todos os membros no banco (Membro.objects.all()) e exibe
         em uma tabela com nome, email e botões de ação (editar/remover).
    """
    login_url = 'login'

    def get(self, request):
        """Lista todos os membros. Apenas admin pode acessar."""
        # Verifica se é admin - se não for, redireciona para a página inicial
        if not request.user.is_superuser:
            return redirect('index')

        # Busca todos os membros do banco de dados
        membros = Membro.objects.all()
        return render(request, 'sistemaweb/listar_membros.html', {'membros': membros})


class CadastrarMembroView(LoginRequiredMixin, View):
    """
    View para cadastrar um novo membro no sistema.

    Acesso: APENAS superusuário (admin).

    GET: Exibe o formulário de cadastro (nome, email, username, senha).
    POST: Valida os dados, cria um User do Django (para login) e um Membro vinculado.
          Validações: campos obrigatórios, username único, email único.
          Após cadastrar, redireciona para a lista de membros.
    """
    login_url = 'login'

    def get(self, request):
        """Exibe o formulário de cadastro. Apenas admin pode acessar."""
        if not request.user.is_superuser:
            return redirect('index')
        return render(request, 'sistemaweb/cadastrar_membro.html')

    def post(self, request):
        """Processa o cadastro: cria User + Membro no banco."""
        if not request.user.is_superuser:
            return redirect('index')

        # Captura os dados do formulário HTML
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validação dos dados
        erro = None
        if not (nome and email and username and password):
            erro = 'Todos os campos são obrigatórios.'
        elif User.objects.filter(username=username).exists():
            erro = 'Esse nome de usuário já está em uso.'
        elif Membro.objects.filter(email=email).exists():
            erro = 'Esse email já está cadastrado.'

        # Se houver erro, reexibe o formulário com a mensagem e os valores preenchidos
        if erro:
            return render(request, 'sistemaweb/cadastrar_membro.html', {
                'erro': erro,
                'nome': nome,
                'email': email,
                'username': username,
            })

        # create_user() cria o usuário COM a senha hasheada (criptografada)
        # Nunca usar User.objects.create() pois salvaria a senha em texto puro
        user = User.objects.create_user(username=username, password=password, email=email)

        # Cria o Membro vinculado ao User recém-criado
        Membro.objects.create(nome=nome, email=email, user=user)
        return redirect('listar_membros')


class EditarMembroView(LoginRequiredMixin, View):
    """
    View para editar os dados de um membro existente.

    Acesso: Superusuário (admin) OU o próprio membro (dono do perfil).

    GET: Exibe o formulário de edição preenchido com os dados atuais do membro.
    POST: Salva as alterações (nome e email).
          - Admin: volta para a lista de membros após salvar
          - Membro: volta para sua página de detalhes após salvar
    """
    login_url = 'login'

    def get(self, request, membro_id):
        """Exibe formulário de edição. Verifica se tem permissão."""
        membro = get_object_or_404(Membro, id=membro_id)

        # Controle de acesso: admin ou o próprio dono do perfil
        if not request.user.is_superuser and (membro.user is None or membro.user != request.user):
            return redirect('index')
        return render(request, 'sistemaweb/editar_membro.html', {'membro': membro})

    def post(self, request, membro_id):
        """Salva as alterações do membro no banco de dados."""
        membro = get_object_or_404(Membro, id=membro_id)

        # Controle de acesso: admin ou o próprio dono
        if not request.user.is_superuser and (membro.user is None or membro.user != request.user):
            return redirect('index')

        nome = request.POST.get('nome')
        email = request.POST.get('email')

        if nome and email:
            membro.nome = nome
            membro.email = email
            membro.save()  # Salva as alterações no banco de dados

            # Admin volta para a lista, membro volta para seus detalhes
            if request.user.is_superuser:
                return redirect('listar_membros')
            return redirect('detalhes_membro', membro_id=membro.id)

        return render(request, 'sistemaweb/editar_membro.html', {'membro': membro})


class RemoverMembroView(LoginRequiredMixin, View):
    """
    View para remover um membro do sistema.

    Acesso: APENAS superusuário (admin).

    GET: Exibe tela de confirmação ("Tem certeza que deseja remover?").
    POST: Remove o membro. Se o membro tiver um User vinculado, deleta o User
          (o CASCADE automaticamente deleta o Membro e suas Tarefas).
          Se não tiver User, deleta o Membro diretamente.
    """
    login_url = 'login'

    def get(self, request, membro_id):
        """Exibe tela de confirmação de remoção. Apenas admin."""
        if not request.user.is_superuser:
            return redirect('index')
        membro = get_object_or_404(Membro, id=membro_id)
        return render(request, 'sistemaweb/remover_membro.html', {'membro': membro})

    def post(self, request, membro_id):
        """Remove o membro (e seu User, se existir) do banco de dados."""
        if not request.user.is_superuser:
            return redirect('index')
        membro = get_object_or_404(Membro, id=membro_id)

        if membro.user:
            # Deletar o User faz CASCADE: deleta Membro e todas as Tarefas
            membro.user.delete()
        else:
            # Se não tem User, deleta o Membro diretamente
            membro.delete()
        return redirect('listar_membros')


class DetalhesMembroView(LoginRequiredMixin, View):
    """
    View de detalhes do membro: exibe informações, lista tarefas e permite adicionar novas.

    Acesso: Superusuário (admin) OU o próprio membro (dono).

    GET: Busca o membro e suas tarefas, exibe a página de detalhes com:
         - Dados do membro (nome, email)
         - Tabela com todas as tarefas do membro
         - Formulário para adicionar nova tarefa
    POST: Cria uma nova tarefa para o membro (recebe título e descrição do formulário).
    """
    login_url = 'login'

    def get(self, request, membro_id):
        """Exibe detalhes do membro e suas tarefas."""
        membro = get_object_or_404(Membro, id=membro_id)

        # Controle de acesso: admin ou o próprio dono
        if not request.user.is_superuser and (membro.user is None or membro.user != request.user):
            return redirect('index')

        # Busca todas as tarefas deste membro específico
        tarefas = Tarefa.objects.filter(membro=membro)
        return render(request, 'sistemaweb/detalhes_membro.html', {'membro': membro, 'tarefas': tarefas})

    def post(self, request, membro_id):
        """Cria uma nova tarefa para o membro."""
        membro = get_object_or_404(Membro, id=membro_id)

        # Controle de acesso
        if not request.user.is_superuser and (membro.user is None or membro.user != request.user):
            return redirect('index')

        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')

        if titulo and descricao:
            # Cria a tarefa vinculada ao membro
            Tarefa.objects.create(membro=membro, titulo=titulo, descricao=descricao)
            return redirect('detalhes_membro', membro_id=membro.id)

        # Se dados incompletos, recarrega a página
        tarefas = Tarefa.objects.filter(membro=membro)
        return render(request, 'sistemaweb/detalhes_membro.html', {'membro': membro, 'tarefas': tarefas})


class EditarTarefaView(LoginRequiredMixin, View):
    """
    View para editar uma tarefa existente.

    Acesso: Superusuário (admin) OU o membro dono da tarefa.
    O acesso é verificado pelo membro vinculado à tarefa (tarefa.membro.user).

    GET: Exibe formulário de edição preenchido com título e descrição atuais.
    POST: Salva as alterações e redireciona para a página de detalhes do membro.
    """
    login_url = 'login'

    def get(self, request, tarefa_id):
        """Exibe formulário de edição da tarefa."""
        tarefa = get_object_or_404(Tarefa, id=tarefa_id)
        membro = tarefa.membro  # Busca o membro dono da tarefa

        # Controle de acesso: admin ou dono da tarefa
        if not request.user.is_superuser and (membro.user is None or membro.user != request.user):
            return redirect('index')
        return render(request, 'sistemaweb/editar_tarefa.html', {'tarefa': tarefa})

    def post(self, request, tarefa_id):
        """Salva as alterações da tarefa no banco de dados."""
        tarefa = get_object_or_404(Tarefa, id=tarefa_id)
        membro = tarefa.membro

        # Controle de acesso
        if not request.user.is_superuser and (membro.user is None or membro.user != request.user):
            return redirect('index')

        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')

        if titulo and descricao:
            tarefa.titulo = titulo
            tarefa.descricao = descricao
            tarefa.save()  # Salva no banco
            return redirect('detalhes_membro', membro_id=membro.id)

        return render(request, 'sistemaweb/editar_tarefa.html', {'tarefa': tarefa})


class RemoverTarefaView(LoginRequiredMixin, View):
    """
    View para remover uma tarefa.

    Acesso: Superusuário (admin) OU o membro dono da tarefa.

    GET: Exibe tela de confirmação ("Tem certeza que deseja remover a tarefa?").
    POST: Remove a tarefa do banco e redireciona para a página de detalhes do membro.
    """
    login_url = 'login'

    def get(self, request, tarefa_id):
        """Exibe tela de confirmação de remoção da tarefa."""
        tarefa = get_object_or_404(Tarefa, id=tarefa_id)
        membro = tarefa.membro

        # Controle de acesso: admin ou dono
        if not request.user.is_superuser and (membro.user is None or membro.user != request.user):
            return redirect('index')
        return render(request, 'sistemaweb/remover_tarefa.html', {'tarefa': tarefa})

    def post(self, request, tarefa_id):
        """Remove a tarefa do banco de dados."""
        tarefa = get_object_or_404(Tarefa, id=tarefa_id)
        membro = tarefa.membro

        # Controle de acesso
        if not request.user.is_superuser and (membro.user is None or membro.user != request.user):
            return redirect('index')

        membro_id = membro.id
        tarefa.delete()  # Remove a tarefa do banco
        return redirect('detalhes_membro', membro_id=membro_id)
