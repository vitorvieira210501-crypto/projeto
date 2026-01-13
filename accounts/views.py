from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as realizar_login
from django.contrib.auth import logout as realizar_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Endereco 

# --- 1. VIEW DE CADASTRO ---
def cadastro(request):
    if request.method == 'POST':
        # Traduzindo: 'form' vira 'formulario'
        formulario = UserCreationForm(request.POST)
        
        if formulario.is_valid():
            usuario = formulario.save()
            # Faz o login automático assim que cria a conta
            realizar_login(request, usuario)
            messages.success(request, f"Bem-vindo, {usuario.username}!")
            return redirect('home') # Redireciona para a Home
    else:
        formulario = UserCreationForm()

    contexto = {'formulario': formulario,
                'title': 'VTRSTORE Streetwear | Cadastro' 
                }
    return render(request, 'accounts/cadastro.html', contexto)

# --- 2. VIEW DE LOGIN ---
def pagina_login(request):
    if request.method == 'POST':
        formulario = AuthenticationForm(data=request.POST)
        
        if formulario.is_valid():
            usuario = formulario.get_user()
            realizar_login(request, usuario)
            
            # Verifica se tinha uma página "next" (proxima) na URL
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            
            return redirect('home')
    else:
        formulario = AuthenticationForm()
    
    contexto = {
        'formulario': formulario,
        'title': 'VTRSTORE Streetwear | Login',
                }
    return render(request, 'accounts/login.html', contexto)

# --- 3. VIEW DE LOGOUT (SAIR) ---
def sair(request):
    realizar_logout(request)
    return redirect('home')




@login_required(login_url='login')
def dashboard(request):
    contexto = {'title': 'VTRSTORE | Minhaconta'}
    return render(request, 'accounts/dashboard.html', contexto)



# ... (suas outras views) ...

@login_required(login_url='login')
def meus_dados(request):
    contexto = {'title': 'VTRSTORE | Meus Dados'}
    usuario = request.user
    
    if request.method == 'POST':
        # Pega os dados enviados pelo formulário
        nome_completo = request.POST.get('nome')
        email = request.POST.get('email')
        
        # Atualiza o usuário (vamos separar o primeiro nome do resto)
        if nome_completo:
            nomes = nome_completo.split()
            usuario.first_name = nomes[0]
            usuario.last_name = ' '.join(nomes[1:]) if len(nomes) > 1 else ''
        
        if email:
            usuario.email = email
            
        usuario.save()
        
        # Avisa que deu certo (opcional, mas bom ter)
        return redirect('dashboard')

    return render(request, 'accounts/meus_dados.html', contexto)





def gerenciar_enderecos(request):
    # 1. Cria o dicionário inicial
    contexto = {'title': 'VTRSTORE | Endereços'}

    if request.method == 'POST':
        Endereco.objects.create(
            usuario=request.user,
            cep=request.POST.get('cep'),
            rua=request.POST.get('rua'),
            numero=request.POST.get('numero'),
            bairro=request.POST.get('bairro'),
            cidade=request.POST.get('cidade'),
            estado=request.POST.get('estado')
        )
        return redirect('enderecos')

    # 2. Busca os dados (Removi as chaves {} que estavam em volta)
    meus_enderecos = Endereco.objects.filter(usuario=request.user)
    
    # 3. Adiciona os endereços DENTRO do dicionário 'contexto' existente
    contexto['enderecos'] = meus_enderecos

    # 4. Passa o dicionário completo para o render
    return render(request, 'accounts/enderecos.html', context=contexto)