from django.contrib import admin
from .models import Product
from django.utils.html import format_html

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # O QUE APARECE NA LISTA (TABELA)
    list_display = ('name', 'mostrar_imagem', 'price', 'stock', 'is_featured')
    
    # O QUE PODE EDITAR DIRETO NA LISTA
    list_editable = ('price', 'stock', 'is_featured')
    
    search_fields = ('name',)
    list_filter = ('is_featured',)

    # ORGANIZAÇÃO DO FORMULÁRIO DE EDIÇÃO (QUANDO CLICA NO NOME)
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'description', 'price')
        }),
        ('Estoque e Destaque', {
            'fields': ('stock', 'is_featured')
        }),
        ('Mídia', {
            'fields': ('image',), # <--- AQUI ESTÁ A IMAGEM
            'description': 'Faça o upload da foto do produto aqui.'
        }),
    )

    # FUNÇÃO EXTRA: MOSTRAR MINIATURA DA FOTO NA LISTA
    def mostrar_imagem(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.image.url)
        return "Sem Imagem"
    
    mostrar_imagem.short_description = 'Foto'