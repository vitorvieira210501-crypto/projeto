from django.contrib import admin
from .models import Pedido, ItemPedido

# Essa classe permite ver os itens DENTRO da tela do Pedido
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0 # Não mostra linhas vazias extras
    readonly_fields = ('produto', 'preco_unitario', 'quantidade', 'tamanho', 'cor') # Para não editar itens de pedidos já feitos
    can_delete = False # Para evitar apagar itens acidentalmente

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Colunas que aparecem na lista geral de pedidos
    list_display = ('id', 'usuario', 'status', 'valor_total', 'data_criacao')
    
    # Filtros laterais para facilitar a busca
    list_filter = ('status', 'data_criacao')
    
    # Injeta a tabela de itens dentro do pedido
    inlines = [ItemPedidoInline]
    
    # Mostra o endereço apenas como leitura para conferência
    readonly_fields = ('data_criacao', 'endereco_entrega', 'valor_total')

    # Organização dos campos na tela
    fieldsets = (
        ('Dados do Pedido', {
            'fields': ('usuario', 'status', 'data_criacao', 'valor_total')
        }),
        ('Entrega', {
            'fields': ('endereco_entrega',)
        }),
    )

# Não precisamos registrar ItemPedido separado, pois ele já aparece dentro de Pedido
# admin.site.register(ItemPedido)