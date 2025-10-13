"""
URL configuration for Triage Digital project.

Sistema de clasificación hospitalaria asistido por software
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def redireccion_inicio(request):
    """Redirige la URL raíz al tablero o admin (temporal)"""
    if request.user.is_authenticated:
        return redirect('triage:dashboard')
    else:
        return redirect('admin:login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redireccion_inicio, name='inicio'),
    
    # Login personalizado con DNI
    path('login/', include('apps.triage.auth_urls')),
    
    # URLs de Apps - Backend funcionando
    path('triage/', include('apps.triage.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)