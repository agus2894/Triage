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
    
    # Detectar modo de base de datos
    from django.conf import settings
    db_engine = settings.DATABASES['default']['ENGINE']
    is_offline = 'sqlite3' in db_engine
    
    # Log para debugging
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Login attempt - DB Engine: {db_engine}, is_offline: {is_offline}")
    
    if request.method == 'POST':
        dni = request.POST.get('dni', '').strip()
        password = request.POST.get('password', '')
        
        logger.info(f"POST recibido - DNI: {dni}, Password length: {len(password)}")
        
        if not dni or not password:
            logger.warning("DNI o password vacíos")
            messages.error(request, 'Por favor complete todos los campos.')
            return render(request, 'registration/login.html', {'is_offline': is_offline})
        
        # Si es admin, intentar login directo sin Profesional
        if dni.lower() == 'admin':
            authenticated_user = authenticate(request, username='admin', password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, f'Bienvenido/a Administrador')
                next_url = request.GET.get('next', 'triage:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Contraseña de administrador incorrecta.')
                return render(request, 'registration/login.html', {'is_offline': is_offline})
        
        # Buscar profesional por DNI
        try:
            from .models import Profesional
            logger.info(f"Buscando profesional con DNI: {dni}")
            profesional = Profesional.objects.select_related('user').get(dni=dni, activo=True)
            user = profesional.user
            logger.info(f"Profesional encontrado: {user.username}")
        except Profesional.DoesNotExist:
            if is_offline:
                # En modo offline, dar pista sin mostrar credenciales
                messages.error(request, f'DNI {dni} no encontrado en base de datos offline.')
            else:
                messages.error(request, 'DNI no autorizado o profesional inactivo.')
            return render(request, 'registration/login.html', {'is_offline': is_offline})
        except Exception as e:
            # Log del error para debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error buscando profesional {dni}: {e}")
            messages.error(request, 'Error al buscar profesional. Verifique la conexión a la base de datos.')
            return render(request, 'registration/login.html', {'is_offline': is_offline})
        
        # Autenticar con el username del usuario y password
        logger.info(f"Intentando authenticate con username: {user.username}")
        authenticated_user = authenticate(request, username=user.username, password=password)
        
        logger.info(f"Resultado authenticate: {authenticated_user}")
        
        if authenticated_user is not None:
            logger.info(f"Login exitoso para {authenticated_user.username}")
            login(request, authenticated_user)
            messages.success(request, f'Bienvenido/a, {authenticated_user.get_full_name() or authenticated_user.username}')
            
            # Redirigir a dashboard o a página solicitada
            next_url = request.GET.get('next', 'triage:dashboard')
            return redirect(next_url)
        else:
            logger.warning(f"Authenticate falló para username: {user.username}")
            messages.error(request, 'DNI o contraseña incorrectos.')
    
    return render(request, 'registration/login.html', {'is_offline': is_offline})


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