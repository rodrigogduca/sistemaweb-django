"""
views.py - Views de autenticação (Login e Logout).

Este arquivo contém as Views responsáveis pelo controle de acesso ao sistema.
A autenticação é o processo de verificar a identidade do usuário (quem ele é),
enquanto a autorização define o que ele pode fazer após estar autenticado.

Conceitos de Programação Orientada a Objetos (POO) usados aqui:

1. CLASSE (class): Um "molde" para criar objetos. Cada View é uma classe.
2. HERANÇA: LoginView e LogoutView herdam de View (classe base do Django).
   Isso significa que elas "ganham" as funcionalidades da classe pai (View),
   como o método dispatch() que roteia GET/POST automaticamente.
3. MÉTODO: Funções definidas dentro de uma classe (get, post).
   O primeiro parâmetro 'self' é uma referência ao próprio objeto.
4. ENCAPSULAMENTO: Cada classe cuida apenas da sua responsabilidade.
   LoginView cuida do login, LogoutView cuida do logout.

Fluxo de autenticação do Django:
1. authenticate(username, password) -> verifica credenciais no banco de dados
2. login(request, usuario)          -> cria uma sessão (cookie) para o usuário
3. logout(request)                  -> destrói a sessão do usuário

Princípios de programação aplicados:
- Responsabilidade Única: cada classe faz apenas uma coisa
- DRY (Don't Repeat Yourself): reutilizamos as funções do Django em vez de reescrever
- Separação de Interesses: autenticação fica isolada neste app, separada das regras de negócio
"""

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout

# Importamos o modelo Membro do app 'sistemaweb' para redirecionar
# membros comuns para sua página de detalhes após o login
from sistemaweb.models import Membro


class LoginView(View):
    """
    View de login - Tela de autenticação do sistema.

    Herança: LoginView -> View (classe base do Django)
    A classe View fornece o método dispatch() que direciona a requisição
    para o método correto: self.get() para GET, self.post() para POST.

    GET: Exibe o formulário de login (usuário e senha).
         Se o usuário já estiver autenticado, redireciona para a página inicial.
    POST: Recebe usuário e senha do formulário, tenta autenticar.
          - Login válido + superusuário: redireciona para a página inicial (index)
          - Login válido + membro comum: redireciona para a página de detalhes do membro
          - Login inválido: exibe mensagem de erro na mesma tela

    Não usa LoginRequiredMixin pois é a própria página de login (acesso público).
    """

    # Atributo de classe: define qual template HTML esta View utiliza.
    # Usar atributos de classe é uma boa prática de POO — facilita manutenção
    # pois se precisar mudar o template, basta alterar aqui.
    template_name = 'autenticacao/login.html'

    def get(self, request):
        """
        Método GET - Exibe a tela de login.

        Parâmetros:
            self: referência ao próprio objeto (padrão em POO)
            request: objeto que contém todos os dados da requisição HTTP
                     (cookies, sessão, usuário logado, método HTTP, etc.)

        Retorno:
            HttpResponse com o HTML renderizado ou um redirect.
        """
        # request.user.is_authenticated: propriedade booleana (True/False)
        # que verifica se o usuário já tem uma sessão ativa
        if request.user.is_authenticated:
            return redirect('index')

        # render() combina o template HTML com os dados e retorna o HTML final
        return render(request, self.template_name)

    def post(self, request):
        """
        Método POST - Processa o formulário de login (autentica usuário e senha).

        Parâmetros:
            self: referência ao próprio objeto
            request: contém os dados enviados pelo formulário em request.POST

        request.POST é um dicionário com os dados do formulário HTML.
        O método .get('campo') busca o valor de forma segura (retorna None se não existir).
        """
        # Captura os dados enviados pelo formulário HTML
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate() verifica se o par (usuário, senha) existe no banco de dados.
        # Retorna o objeto User se válido, ou None se inválido.
        # A senha é comparada usando hashing (nunca em texto puro).
        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            # login() cria a sessão do usuário no Django.
            # Uma sessão é um registro no banco que associa o cookie do navegador
            # ao usuário logado. Assim o Django "lembra" quem está logado.
            login(request, usuario)

            # Superusuário (admin) vai para a página inicial completa
            if usuario.is_superuser:
                return redirect('index')

            # Membro comum vai direto para sua página de detalhes/tarefas
            try:
                membro = Membro.objects.get(user=usuario)
                return redirect('detalhes_membro', membro_id=membro.id)
            except Membro.DoesNotExist:
                # Se o usuário não tem Membro vinculado, vai pro index
                # (a PaginaInicialView tratará isso)
                return redirect('index')

        # Se authenticate() retornou None, as credenciais são inválidas.
        # Reexibimos o formulário de login com uma mensagem de erro.
        # O dicionário {'erro': '...'} é passado ao template para exibir a mensagem.
        return render(request, self.template_name, {
            'erro': 'Usuário ou senha inválidos.'
        })


class LogoutView(View):
    """
    View de logout - Encerra a sessão do usuário.

    Herança: LogoutView -> View

    GET: Faz o logout (destrói a sessão no servidor) e redireciona para a tela de login.

    Ao chamar logout(request), o Django:
    1. Remove os dados da sessão do banco de dados
    2. Invalida o cookie de sessão no navegador
    3. O próximo request.user será AnonymousUser (usuário anônimo)
    """

    def get(self, request):
        """Encerra a sessão e redireciona para o login."""
        logout(request)
        return redirect('login')
