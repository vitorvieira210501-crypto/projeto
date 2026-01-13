from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.colecao, name='colecao'),
    path('produto/<int:pk>/', views.produto_detalhe, name='produto_detalhe'),
    path('camisetas/', views.camisetas, name='camisetas'),
    path('shorts/', views.shorts, name='shorts'),
    path('calcas/', views.calcas, name='calcas'),
    path('jaquetas/', views.jaquetas, name='jaquetas'),
    path('moletons/', views.moletons, name='moletons'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove/<int:item_index>/', views.remove_from_cart, name='remove_from_cart'),
   
]
