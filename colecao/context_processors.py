def cart_counter(request):
    cart = request.session.get('cart', []) # Pega a lista, ou vazia []
    qtd_total = 0
    
    # Como 'cart' é uma lista, nós percorremos ela item por item
    for item in cart:
        # Somamos a quantidade de cada item
        # Se você tiver 2 camisas e 1 boné, aqui faz: 2 + 1 = 3
        qtd_total += item.get('quantity', 0)

    return {'cart_qtd': qtd_total}