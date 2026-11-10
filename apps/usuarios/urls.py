from django.urls import path
from . import views

urlpatterns = [
    path('accounts/registro/', views.registro_view, name='registro'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('juego/nuevo/', views.crear_videojuego_protegido, name='crear_juego'),
    path('perfil/', views.perfil_view, name='perfil'),
]