"""
Vistas de autenticación para profesionales médicos.
Login con DNI + contraseña para enfermeros y médicos.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache


@never_cache
@require_http_methods(["GET", "POST"])
def login_profesional(request):
    """
    Login personalizado con DNI para profesionales médicos.
    """
    if request.user.is_authenticated:
        return redirect('triage:dashboard')
    
    if request.method == 'POST':
        dni = request.POST.get('dni', '').strip()
        password = request.POST.get('password', '')
        
        if not dni or not password:
            messages.error(request, 'Por favor complete todos los campos.')
            return render(request, 'registration/login.html')
        
        # Buscar profesional por DNI
        try:
            from .models import Profesional
            profesional = Profesional.objects.select_related('user').get(dni=dni, activo=True)
            user = profesional.user
        except Profesional.DoesNotExist:
            messages.error(request, 'DNI no autorizado o profesional inactivo.')
            return render(request, 'registration/login.html')
        
        # Autenticar con el username del usuario y password
        authenticated_user = authenticate(request, username=user.username, password=password)
        
        if authenticated_user is not None:
            login(request, authenticated_user)
            messages.success(request, f'Bienvenido/a, {authenticated_user.get_full_name() or authenticated_user.username}')
            
            # Redirigir a dashboard o a página solicitada
            next_url = request.GET.get('next', 'triage:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'DNI o contraseña incorrectos.')
    
    return render(request, 'registration/login.html')


@require_http_methods(["GET", "POST"])
def logout_profesional(request):
    """
    Logout del profesional médico.
    """
    if request.user.is_authenticated:
        nombre = request.user.get_full_name() or request.user.username
        logout(request)
        messages.success(request, f'Sesión cerrada correctamente. ¡Hasta pronto!')
    return redirect('login')