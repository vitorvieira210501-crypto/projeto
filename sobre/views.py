from django.shortcuts import render


# Create your views here.
def sobre(request):
     contexto = {
        'title': 'VTRSTORE Streetwear | Sobre'
    }
     return render(
        request,
        'sobre/sobre.html',
        contexto
    )