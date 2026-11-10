from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.juegos.models import Videojuego

@login_required(login_url='/accounts/login/')
def inicio_view(request):
    
    ultimos_juegos = Videojuego.objects.all().order_by('-creado')[:4]
    
    context = {
        'ultimos_juegos': ultimos_juegos,
    }
    return render(request, 'inicio/index.html', context)