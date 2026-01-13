from django.shortcuts import render

# Create your views here.
def carrinho(request):
   contexto = {
      'title': 'VTRSTORE Streetwear | Carrinho'
     
   }
   return render(
         request,
        'carrinho/carrinho.html',
         contexto,
    )