"""
views.py - Logica de controle das paginas (Views) do sistema.

Este arquivo contem todas as Views do sistema, usando Class-Based Views (CBVs).
Cada classe herda de View (do Django) e define metodos get() e/ou post()
para tratar requisicoes HTTP GET e POST respectivamente.

- GET: Quando o usuario acessa uma pagina pelo navegador (clicando em link ou digitando URL)
- POST: Quando o usuario envia um formulario (clicando em botao de submit)

O mixin LoginRequiredMixin protege as views: se o usuario nao estiver logado,
ele e redirecionado automaticamente para a pagina de login.

Controle de acesso:
- Superusuario (admin): acessa tudo (listar, cadastrar, editar, remover membros e tarefas)
- Membro comum: so acessa seus proprios dados e tarefas
- Visitante nao logado: e redirecionado para a tela de login

Nao usamos forms.py do Django. Todos os inputs sao escritos diretamente
no HTML e os dados sao capturados aqui com request.POST.get('nome_do_campo').
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Membro, Tarefa


class LoginView(View):
    """
    View de login - Tela de autenticacao do sistema.

    GET: Exibe o formulario de login (usuario e senha).
         Se o usuario ja estiver autenticado, redireciona para a pagina inicial.
    POST: Recebe usuario e senha do formulario, tenta autenticar.
          - Login valido + superusuario: redireciona para a pagina inicial (index)
          - Login valido + membro comum: redireciona para a pagina de detalhes do membro
          - Login invalido: exibe mensagem de erro na mesma tela

    Nao usa LoginRequiredMixin pois e a propria pagina de login (acesso publico).
    """

    def get(self, request):
        """Exibe a tela de login. Se ja estiver logado, vai para o index."""
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'sistemaweb/login.html')

    def post(self, request):
        """Processa o formulario de login (autentica usuario e senha)."""
        # Captura os dados enviados pelo formulario HTML
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate() verifica se usuario e senha estao corretos no banco
        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            # login() cria a sessao do usuario no Django (armazena no banco/cookie)
            login(request, usuario)

            # Superusuario (admin) vai para a pagina inicial completa
            if usuario.is_superuser:
                return redirect('index')

            # Membro comum vai direto para sua pagina de detalhes/tarefas
            try:
                membro = Membro.objects.get(user=usuario)
                return redirect('detalhes_membro', membro_id=membro.id)
            except Membro.DoesNotExist:
                return redirect('index')

        # Se autenticacao falhar, mostra erro na tela de login
        return render(request, 'sistemaweb/login.html', {'erro': 'Usuario ou senha invalidos.'})


class LogoutView(View):
    """
    View de logout - Encerra a sessao do usuario.

    GET: Faz o logout (destroi a sessao no servidor) e redireciona para a tela de login.
    """

    def get(self, request):
        """Encerra a sessao e redireciona para o login."""
        logout(request)
        return redirect('login')


class PaginaInicialView(LoginRequiredMixin, View):
    """
    View da pagina inicial do sistema (rota raiz '/').

    Protegida por LoginRequiredMixin: usuario nao logado e redirecionado para login.

    GET:
    - Superusuario: exibe a pagina inicial com boas-vindas e links de navegacao
    - Membro comum: redireciona para sua pagina de detalhes (suas tarefas)
    - Usuario sem membro vinculado: faz logout por seguranca

    login_url: define para onde redirecionar se o usuario nao estiver logado.
    """
    login_url = 'login'

    def get(self, request):
        """Exibe pagina inicial (admin) ou redireciona para detalhes (membro)."""
        # Superusuario ve a pagina inicial completa
        if request.user.is_superuser:
            return render(request, 'sistemaweb/index.html')

        # Membro comum e redirecionado para sua propria pagina de detalhes
        try:
            membro = Membro.objects.get(user=request.user)
            return redirect('detalhes_membro', membro_id=membro.id)
        except Membro.DoesNotExist:
            # Seguranca: se nao tem membro vinculado, encerra a sessao
            logout(request)
            return redirect('login')


class ListarMembrosView(LoginRequiredMixin, View):
    """
    View para listar todos os membros cadastrados.

    Acesso: APENAS superusuario (admin). Membros comuns sao redirecionados.

    GET: Busca todos os membros no banco (Membro.objects.all()) e exibe
         em uma tabela com nome, email e botoes de acao (editar/remover).
    """
    login_url = 'login'

    def get(self, request):
        """Lista todos os membros. Apenas admin pode acessar."""
        # Verifica se e admin - se nao for, redireciona para a pagina inicial
        if not request.user.is_superuser:
            return redirect('index')

        # Busca todos os membros do banco de dados
        membros = Membro.objects.all()
        return render(request, 'sistemaweb/listar_membros.html', {'membros': membros})


class CadastrarMembroView(LoginRequiredMixin, View):
    """
    View para cadastrar um novo membro no sistema.

    Acesso: APENAS superusuario (admin).

    GET: Exibe o formulario de cadastro (nome, email, username, senha).
    POST: Valida os dados, cria um User do Django (para login) e um Membro vinculado.
          Validacoes: campos obrigatorios, username unico, email unico.
          Apos cadastrar, redireciona para a lista de membros.
    """
    login_url = 'login'

    def get(self, request):
        """Exibe o formulario de cadastro. Apenas admin pode acessar."""
        if not request.user.is_superuser:
            return redirect('index')
        return render(request, 'sistemaweb/cadastrar_membro.html')

    def post(self, request):
        """Processa o cadastro: cria User + Membro no banco."""
        if not request.user.is_superuser:
            return redirect('index')

        # Captura os dados do formulario HTML
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validacao dos dados
        erro = None
        if not (nome and email and username and password):
            erro = 'Todos os campos sao obrigatorios.'
        elif User.objects.filter(username=username).exists():
            erro = 'Esse nome de usuario ja esta em uso.'
        elif Membro.objects.filter(email=email).exists():
            erro = 'Esse email ja esta cadastrado.'

        # Se houver erro, reexibe o formulario com a mensagem e os valores preenchidos
        if erro:
            return render(request, 'sistemaweb/cadastrar_membro.html', {
                'erro': erro,
                'nome': nome,
                'email': email,
                'username': username,
            })

        # create_user() cria o usuario COM a senha hasheada (criptografada)
        # Nunca usar User.objects.create() pois salvaria a senha em texto puro
        user = User.objects.create_user(username=username, password=password, email=email)

        # Cria o Membro vinculado ao User recem-criado
        Membro.objects.create(nome=nome, email=email, user=user)
        return redirect('listar_membros')


class EditarMembroView(LoginRequiredMixin, View):
    """
    View para editar os dados de um membro existente.

    Acesso: Superusuario (admin) OU o proprio membro (dono do perfil).

    GET: Exibe o formulario de edicao preenchido com os dados atuais do membro.
    POST: Salva as alteracoes (nome e email).
          - Admin: volta para a lista de membros apos salvar
          - Membro: volta para sua pagina de detalhes apos salvar
    """
    login_url = 'login'

    def get(self, request, membro_id):
        """Exibe formulario de edicao. Verifica se tem permissao."""
        membro = get_object_or_404(Membro, id=membro_id)

        # Controle de acesso: admin ou o proprio dono do perfil
        if not request.user.is_superuser and (membro.user is None or membro.user != request.user):
            return redirect('index')
        return render(request, 'sistemaweb/editar_membro.html', {'membro': membro})

    def post(self, request, membro_id):
        """Salva as alteracoes do membro no banco de dados."""
        membro = get_object_or_404(Membro, id=membro_id)

        # Controle de acesso: admin ou o proprio dono
        if not request.user.is_superuser and (membro.user is None or membro.user != request.user):
            return redirect('index')

        nome = request.POST.get('nome')
        email = request.POST.get('email')

        if nome and email:
            membro.nome = nome
            membro.email = email
            membro.save()  # Salva as alteracoes no banco de dados

            # Admin volta para a lista, membro volta para seus detalhes
            if request.user.is_superuser:
                return redirect('listar_membros')
            return redirect('detalhes_membro', membro_id=membro.id)

        return render(request, 'sistemaweb/editar_membro.html', {'membro': membro})


class RemoverMembroView(LoginRequiredMixin, View):
    """
    View para remover um membro do sistema.

    Acesso: APENAS superusuario (admin).

    GET: Exibe tela de confirmacao ("Tem certeza que deseja remover?").
    POST: Remove o membro. Se o membro tiver um User vinculado, deleta o User
          (o CASCADE automaticamente deleta o Membro e suas Tarefas).
          Se nao tiver User, deleta o Membro diretamente.
    """
    login_url = 'login'

    def get(self, request, membro_id):
        """Exibe tela de confirmacao de remocao. Apenas admin."""
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
            # Se nao tem User, deleta o Membro diretamente
            membro.delete()
        return redirect('listar_membros')


class DetalhesMembroView(LoginRequiredMixin, View):
    """
    View de detalhes do membro: exibe informacoes, lista tarefas e permite adicionar novas.

    Acesso: Superusuario (admin) OU o proprio membro (dono).

    GET: Busca o membro e suas tarefas, exibe a pagina de detalhes com:
         - Dados do membro (nome, email)
         - Tabela com todas as tarefas do membro
         - Formulario para adicionar nova tarefa
    POST: Cria uma nova tarefa para o membro (recebe titulo e descricao do formulario).
    """
    login_url = 'login'

    def get(self, request, membro_id):
        """Exibe detalhes do membro e suas tarefas."""
        membro = get_object_or_404(Membro, id=membro_id)

        # Controle de acesso: admin ou o proprio dono
        if not request.user.is_superuser and (membro.user is None or membro.user != request.user):
            return redirect('index')

        # Busca todas as tarefas deste membro especifico
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

        # Se dados incompletos, recarrega a pagina
        tarefas = Tarefa.objects.filter(membro=membro)
        return render(request, 'sistemaweb/detalhes_membro.html', {'membro': membro, 'tarefas': tarefas})


class EditarTarefaView(LoginRequiredMixin, View):
    """
    View para editar uma tarefa existente.

    Acesso: Superusuario (admin) OU o membro dono da tarefa.
    O acesso e verificado pelo membro vinculado a tarefa (tarefa.membro.user).

    GET: Exibe formulario de edicao preenchido com titulo e descricao atuais.
    POST: Salva as alteracoes e redireciona para a pagina de detalhes do membro.
    """
    login_url = 'login'

    def get(self, request, tarefa_id):
        """Exibe formulario de edicao da tarefa."""
        tarefa = get_object_or_404(Tarefa, id=tarefa_id)
        membro = tarefa.membro  # Busca o membro dono da tarefa

        # Controle de acesso: admin ou dono da tarefa
        if not request.user.is_superuser and (membro.user is None or membro.user != request.user):
            return redirect('index')
        return render(request, 'sistemaweb/editar_tarefa.html', {'tarefa': tarefa})

    def post(self, request, tarefa_id):
        """Salva as alteracoes da tarefa no banco de dados."""
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

    Acesso: Superusuario (admin) OU o membro dono da tarefa.

    GET: Exibe tela de confirmacao ("Tem certeza que deseja remover a tarefa?").
    POST: Remove a tarefa do banco e redireciona para a pagina de detalhes do membro.
    """
    login_url = 'login'

    def get(self, request, tarefa_id):
        """Exibe tela de confirmacao de remocao da tarefa."""
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
