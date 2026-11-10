from django.urls import path
from . import views

urlpatterns = [
    path('catalogo/', views.catalogo_view, name='catalogo'),
    path('juego/nuevo/', views.crear_juego_view, name='crear_juego'),
    path('juego/editar/<int:pk>/', views.editar_juego_view, name='editar_juego'),
    path('juego/eliminar/<int:pk>/', views.eliminar_juego_view, name='eliminar_juego'),
    path('juego/<slug:slug>/', views.detalle_juego_view, name='detalle_juego_slug'),
    path('juego/detalle/<slug:slug>/', views.detalle_juego_view, name='detalle_juego_slug'),
    path('juego/detalle/id/<int:pk>/', views.detalle_juego_view, name='detalle_juego'),
]