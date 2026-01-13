from django.shortcuts import render

# Create your views here.

def contato(request):
    contexto = {
        'title': 'VTRSTORE Streetwear | Contato'
    }
    return render(
        request,
        'contato/contato.html',
        contexto,
    )