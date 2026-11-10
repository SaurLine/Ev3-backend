from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Videojuego, Genero
from .forms import VideojuegoForm

@login_required(login_url='/accounts/login/')
def catalogo_view(request):

    genero_id = request.GET.get('genero')
    generos = Genero.objects.all()
    
    if genero_id and genero_id.isdigit():
        juegos = Videojuego.objects.filter(genero__id=int(genero_id))
    else:
        juegos = Videojuego.objects.all()
        
    context = {
        'juegos': juegos,
        'generos': generos,
        'genero_seleccionado': int(genero_id) if genero_id and genero_id.isdigit() else None,
    }
    return render(request, 'juegos/catalogo.html', context)


def detalle_juego_view(request, slug=None, pk=None):
    """
    Muestra la información detallada de un videojuego.
    Soporta la búsqueda tanto por slug como por id (pk).
    """
    if slug:
        juego = get_object_or_404(Videojuego, slug=slug, activo=True)
    else:
        juego = get_object_or_404(Videojuego, pk=pk, activo=True)
        
    return render(request, 'juegos/detalle_juego.html', {'juego': juego})

def es_admin(user):
    """Verifica si el usuario tiene privilegios de administrador."""
    if user.is_authenticated:
        if user.is_staff or user.is_superuser:
            return True
        if hasattr(user, 'perfilusuario') and user.perfilusuario.rol == 'Admin':
            return True
    return False


@login_required
@user_passes_test(es_admin, login_url='inicio')
def crear_juego_view(request):
    if request.method == 'POST':
        form = VideojuegoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Videojuego creado con éxito!")
            return redirect('catalogo')
    else:
        form = VideojuegoForm()
    return render(request, 'juegos/form_juego.html', {'form': form, 'accion': 'Crear'})

@login_required
@user_passes_test(es_admin, login_url='inicio')
def editar_juego_view(request, pk):
    juego = get_object_or_404(Videojuego, pk=pk)
    if request.method == 'POST':
        form = VideojuegoForm(request.POST, request.FILES, instance=juego)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Videojuego actualizado con éxito!")
            return redirect('catalogo')
    else:
        form = VideojuegoForm(instance=juego)
    return render(request, 'juegos/form_juego.html', {'form': form, 'accion': 'Editar'})

@login_required
@user_passes_test(es_admin, login_url='inicio')
def eliminar_juego_view(request, pk):
    juego = get_object_or_404(Videojuego, pk=pk)
    if request.method == 'POST':
        juego.delete()
        messages.success(request, "¡Videojuego eliminado correctamente!")
        return redirect('catalogo')
    return render(request, 'juegos/eliminar_juego.html', {'juego': juego})