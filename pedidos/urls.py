from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.finalizar_compra, name='checkout'),
    path('meus-pedidos/', views.meus_pedidos, name='meus_pedidos'),
    
    # AQUI ESTÁ A CORREÇÃO: O name deve ser 'detalhes_pedido'
    path('sucesso/<int:pk>/', views.pedido_confirmado, name='detalhes_pedido'),
]