from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.pagina_login, name='login'), 
    path('logout/', views.sair, name='logout'),       
    path('minha-conta/', views.dashboard, name='dashboard'),
    path('minha-conta/dados/', views.meus_dados, name='meus_dados'),
    path('minha-conta/enderecos/', views.gerenciar_enderecos, name='enderecos'),
]