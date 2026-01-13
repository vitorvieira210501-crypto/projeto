from django.shortcuts import render
from colecao.models import Product


# Create your views here.
# views.py

# --- 1. A HOME (Só Destaques) ---
def home(request):
    # Filtra: Só traz produtos que você marcou a caixinha 'is_featured'
    produtos_destaque = Product.objects.filter(is_featured=True).order_by('-id')
    
    context = {
        'products': produtos_destaque, # Enviamos apenas os destaques
        'title': 'VTRSTORE | Home'
    }
    return render(request, 'home/home.html', context)

# --- 2. A COLEÇÃO (Loja Completa) ---
def colecao(request):
    # Pega TUDO (All)
    todos_produtos = Product.objects.all().order_by('-id')
    
    context = {
        'products': todos_produtos, # Enviamos a lista completa
        'title': 'VTRSTORE | Coleção Completa'
    }
    # Aqui usamos o seu arquivo colecao.html que mostra a grade completa
    return render(request, 'colecao/colecao.html', context)

# ... (suas outras views de camisetas, moletons, etc continuam iguais)
