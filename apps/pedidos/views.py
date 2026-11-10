from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.juegos.models import Videojuego
from .models import Pedido, ItemPedido

@login_required(login_url='/accounts/login/')
def ver_carrito(request):

    pedido, creado = Pedido.objects.get_or_create(usuario=request.user, completado=False)
    

    items = ItemPedido.objects.filter(pedido=pedido)
    
    context = {
        'pedido': pedido,
        'items': items,
    }
    return render(request, 'pedidos/carrito.html', context)

@login_required(login_url='/accounts/login/')
def agregar_al_carrito(request, juego_id):
    juego = get_object_or_404(Videojuego, id=juego_id)
    

    if juego.stock <= 0 or not juego.activo:
        messages.error(request, f'Lo sentimos, "{juego.titulo}" no tiene stock disponible.')
        return redirect('catalogo')
    

    pedido, creado = Pedido.objects.get_or_create(usuario=request.user, completado=False)
    

    item, creado_item = ItemPedido.objects.get_or_create(
        pedido=pedido, 
        juego=juego
    )
    
    if not creado_item:

        if item.cantidad < juego.stock:
            item.cantidad += 1
            item.save()
            messages.success(request, f"¡Se actualizó la cantidad de '{juego.titulo}' en el carrito!")
        else:
            messages.warning(request, f"Has alcanzado el límite de stock disponible para '{juego.titulo}'.")
            return redirect('ver_carrito')
    else:
        messages.success(request, f"¡Se añadió '{juego.titulo}' al carrito!")
    
    return redirect('ver_carrito')

@login_required(login_url='/accounts/login/')
def eliminar_item_carrito(request, item_id):
    item = get_object_or_404(ItemPedido, id=item_id)
    item.delete()
    messages.success(request, "Producto eliminado del carrito.")
    return redirect('ver_carrito')