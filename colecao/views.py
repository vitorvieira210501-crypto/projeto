from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
from .models import Product

# ========================================================
# 1. PÁGINA INICIAL (HOME) -> MOSTRA SÓ DESTAQUES
# ========================================================
# colecao/views.py

def home(request):
    # Busca os destaques no banco (isso continua igual)
    products = Product.objects.filter(is_featured=True).order_by('-id')
    
    context = {
        'products': products,
        'title': 'VTRSTORE | Home'
    }
    
    # ATENÇÃO AQUI: Aponte para a pasta do app HOME
    # Se o nome do seu app for "home", a pasta deve ser "templates/home/"
    return render(request, 'home/home.html', context)

# ========================================================
# 2. PÁGINA COLEÇÃO (LOJA) -> MOSTRA TUDO
# ========================================================
def colecao(request):
    # Busca TODOS os produtos do banco
    products = Product.objects.all().order_by('-id')
    
    context = {
        'products': products, 
        'title': 'VTRSTORE | Coleção Completa',
    }
    # Usa seu arquivo colecao.html para mostrar a grade completa
    return render(request, 'colecao/colecao.html', context)


# ========================================================
# 3. CARRINHO DE COMPRAS (COM PROTEÇÃO CONTRA ERROS)
# ========================================================
def add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('id')
            size = data.get('size')
            color = data.get('color')
            quantity = int(data.get('quantity'))

            if 'cart' not in request.session:
                request.session['cart'] = []

            cart = request.session['cart']
            product_found = False

            for item in cart:
                if item['product_id'] == product_id and item['size'] == size and item['color'] == color:
                    item['quantity'] += quantity
                    product_found = True
                    break

            if not product_found:
                cart.append({
                    'product_id': product_id,
                    'size': size,
                    'color': color,
                    'quantity': quantity,
                })

            request.session['cart'] = cart
            request.session.modified = True 
            return JsonResponse({'status': 'success', 'cart_count': len(cart)})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error'}, status=400)


def view_cart(request):
    
    cart = request.session.get('cart', [])
    cart_items = []
    total_price = 0
    valid_cart = [] # Lista para salvar apenas itens que realmente existem no banco

    for item in cart:
        try:
            # Tenta buscar o produto. Se não achar, o código pula para o 'except'
            product = Product.objects.get(id=item['product_id'])
            
            subtotal = product.price * item['quantity']
            total_price += subtotal
            
            cart_items.append({
                'index': len(valid_cart), # Mantém o índice correto para remoção
                'product': product,
                'size': item['size'],
                'color': item['color'],
                'quantity': item['quantity'],
                'subtotal': subtotal
            })
            
            # Se deu certo, adiciona na lista de itens válidos
            valid_cart.append(item)
            
        except Product.DoesNotExist:
            # Produto não encontrado (foi deletado ou ID errado na Home), apenas ignoramos
            continue

    # Atualiza a sessão removendo produtos inexistentes
    if len(valid_cart) != len(cart):
        request.session['cart'] = valid_cart
        request.session.modified = True

    context = {
        'title': 'VTRSTORE Streetwear | Carrinho',
        'cart_items': cart_items,
        'total_price': total_price
    }
    
    return render(request, 'colecao/cart.html', context)


def remove_from_cart(request, item_index):
    cart = request.session.get('cart', [])

    if 0 <= item_index < len(cart):
        del cart[item_index]
        request.session['cart'] = cart
        request.session.modified = True
    
    return redirect('view_cart')


# ========================================================
# 4. PÁGINAS DE CATEGORIAS
# ========================================================
def produto_detalhe(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product, 'title': f"{product.name} | VTRSTORE"}
    return render(request, 'colecao/produto_detalhe.html', context)

def camisetas(request):
    products = Product.objects.filter(name__icontains='Camiseta') 
    context = {'products': products, 'title': 'VTRSTORE | Camisetas'}
    return render(request, 'colecao/camisetas.html', context)

def shorts(request):
    products = Product.objects.filter(name__icontains='Short') 
    context = {'products': products, 'title': 'VTRSTORE | Shorts'}
    return render(request, 'colecao/shorts.html', context)

def calcas(request):
    products = Product.objects.filter(name__icontains='Calça') 
    context = {'products': products, 'title': 'VTRSTORE | Calças'}
    return render(request, 'colecao/calcas.html', context)

def jaquetas(request):
    products = Product.objects.filter(name__icontains='Jaqueta') 
    context = {'products': products, 'title': 'VTRSTORE | Jaquetas'}
    return render(request, 'colecao/jaquetas.html', context)

def moletons(request):
    products = Product.objects.filter(name__icontains='Moletom') 
    context = {'products': products, 'title': 'VTRSTORE | Moletons'}
    return render(request, 'colecao/moletons.html', context)