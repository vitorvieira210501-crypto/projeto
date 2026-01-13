from django.shortcuts import render

# Create your views here.
def drops(request):
     contexto = {
        'title': 'VTRSTORE Streetwear | Drops',
    }
     return render(
        request,
        'drops/drops.html',
        contexto
    )