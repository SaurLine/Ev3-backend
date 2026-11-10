from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegistroUsuarioForm


def registro_view(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"¡Bienvenido, {user.username}! Tu cuenta ha sido creada exitosamente.")
            return redirect('inicio')
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario de registro.")
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuarios/registro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Has iniciado sesión correctamente, {username}.")
                return redirect('inicio')
        
        messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión de forma segura.")
    return redirect('login')



def es_admin(user):
    return user.is_authenticated and user.is_staff

@login_required(login_url='login')
@user_passes_test(es_admin, login_url='catalogo')
def crear_videojuego_protegido(request):

    ...


@login_required(login_url='/accounts/login/')
def perfil_view(request):
    context = {
        'user': request.user
    }
    return render(request, 'usuarios/perfil.html', context)