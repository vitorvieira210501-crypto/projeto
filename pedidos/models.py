from django.db import models
from django.contrib.auth.models import User
from colecao.models import Product  # Importe seu model de Produto aqui!

class Pedido(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pendente'),
        ('A', 'Aprovado'),
        ('E', 'Enviado'),
        ('C', 'Cancelado'),
    )

    # Liga o pedido ao Usuário que cadastrou
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Dados básicos
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    
    # Podemos salvar o total aqui para não precisar recalcular sempre
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    endereco_entrega = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"


class ItemPedido(models.Model):
    # Liga este item ao Pedido pai
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    
    # Liga ao Produto original
    produto = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    
    # Detalhes específicos dessa compra
    tamanho = models.CharField(max_length=5) # P, M, G...
    cor = models.CharField(max_length=20)    # Preto, Branco...
    quantidade = models.PositiveIntegerField(default=1)
    
    # IMPORTANTE: Salvamos o preço NO MOMENTO da compra. 
    # Se o produto aumentar de preço amanhã, esse pedido antigo não muda.
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.name}"
    
    # Calcula o subtotal deste item (preço x quantidade)
    def subtotal(self):
        return self.preco_unitario * self.quantidade
    
