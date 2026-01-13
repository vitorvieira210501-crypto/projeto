from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pedido, ItemPedido
from colecao.models import Product
from accounts.models import Endereco

# --- FUNÇÃO 1: FINALIZAR A COMPRA ---
# ... (imports mantidos) ...
from django.contrib import messages # Importe messages para dar erro se faltar estoque

@login_required(login_url='login')
def finalizar_compra(request):
    carrinho = request.session.get('cart', [])
    
    if not carrinho:
        return redirect('colecao')

    # 1. VERIFICAÇÃO DE ENDEREÇO (Mantém igual)
    endereco_obj = Endereco.objects.filter(usuario=request.user).last()
    if not endereco_obj:
        return redirect('enderecos')

    # --- NOVO: VERIFICAÇÃO PRÉVIA DE ESTOQUE ---
    # Antes de criar qualquer coisa, vamos ver se tem produto pra todo mundo
    for item in carrinho:
        produto = Product.objects.get(id=item['product_id'])
        qtd_solicitada = int(item['quantity'])
        
        # Se o cara quer 5 e só tem 2:
        if qtd_solicitada > produto.stock:
            messages.error(request, f'Ops! O produto {produto.name} só tem {produto.stock} unidades disponíveis.')
            return redirect('cart_detail') # Manda de volta pro carrinho pra ele corrigir

    # 2. CRIA O PEDIDO (Mantém igual)
    texto_endereco = f"{endereco_obj.rua}, {endereco_obj.numero} - {endereco_obj.bairro}..." # (Seu código anterior)
    
    pedido = Pedido.objects.create(
        usuario=request.user,
        endereco_entrega=texto_endereco
    )
    
    valor_total_pedido = 0

    # 3. SALVA ITENS E BAIXA ESTOQUE
    for item in carrinho:
        try:
            produto = Product.objects.get(id=item['product_id']) 
            qtd = int(item['quantity'])
            
            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                tamanho=item['size'],
                cor=item['color'],
                quantidade=qtd,
                preco_unitario=produto.price
            )
            
            # --- A MÁGICA ACONTECE AQUI ---
            produto.stock = produto.stock - qtd # Tira do estoque
            produto.save() # Salva no banco a nova quantidade
            # ------------------------------

            valor_total_pedido += float(produto.price) * qtd
            
        except Product.DoesNotExist:
            continue

    pedido.valor_total = valor_total_pedido
    pedido.save()

    request.session['cart'] = []
    request.session.modified = True

    return redirect('detalhes_pedido', pk=pedido.id)

# --- FUNÇÃO 2: TELA DE SUCESSO / DETALHES ---
@login_required(login_url='login')
def pedido_confirmado(request, pk):
    # Busca o pedido pelo ID (pk), mas só se for do usuário logado
    pedido = get_object_or_404(Pedido, pk=pk, usuario=request.user)
    
    contexto = {'pedido': pedido,
                'title': 'VTRSTORE | Confirmação de pedido'}
    # Renderiza o template de sucesso (que agora serve como detalhes também)
    return render(request, 'pedidos/sucesso.html', contexto)


# --- FUNÇÃO 3: MEUS PEDIDOS ---
@login_required(login_url='login')
def meus_pedidos(request):
    # Busca os pedidos do usuário logado
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-data_criacao')
    
    contexto = {'pedidos': pedidos,
                'title': 'VTRSTORE | Meus Pedidos'}
    return render(request, 'pedidos/meus_pedidos.html', contexto)

