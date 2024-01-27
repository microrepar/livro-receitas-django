from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from receitas.models import Receita


def cadastrar(request):
    """Cadastra um novo usuário no sistema
    """

    if request.method == 'POST':
        nome      = request.POST['nome']
        email     = request.POST['email']
        password  = request.POST['password']
        password2 = request.POST['password2']
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect('cadastrar')
        
        if not all([nome.strip(), email.strip(), password.strip(), password2.strip()]):
            messages.error(request, 'Todos os campos devem ser preenchidos')
            return redirect('cadastrar')
        
        if password != password2:
            messages.error('Os campos senha e senha2 devem ser iguais.')
            return redirect('cadastrar')
        
        user = User.objects.create_user(username=nome, email=email, password=password)
        user.save()

        messages.success(request, 'Usuário cadastrado como sucesso')
        return redirect('login')

    return render(request, 'usuarios/cadastro.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']

        if not all([email.strip(), senha.strip()]):
            messages.error(request, 'Os campos email e senha devem ser preenchidos')
            return redirect('login')

        if User.objects.filter(email=email).exists():
            username = User.objects.filter(email=email).values_list('username', flat=True).get()
            
            user = auth.authenticate(request, username=username, password=senha)

            if user is not None:
                auth.login(request, user=user)
                messages.success(request, 'Login realizado com sucesso')
                return redirect('dashboard')
        messages.error(request, 'Email ou senha incorreta.')

    return render(request, 'usuarios/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'Usuário desconectado')
    return redirect('index')


def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=user)
        dados = {
            'receitas': receitas
        }
        return render(request, 'usuarios/dashboard.html', context=dados)
    return redirect('index')


def usuario_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    
    dados_receita = {
        'receita': receita
    }
    
    return render(request, 'receitas/receita.html', dados_receita)