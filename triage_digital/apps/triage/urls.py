"""
URLs del sistema de triage - Solo rutas esenciales.
Filosofía: "Menos es mejor"
"""

from django.urls import path
from . import views

app_name = 'triage'

urlpatterns = [
    # Dashboard principal
    path('', views.dashboard_principal, name='dashboard'),
    
    # Vista única inteligente para triage completo
    path('triage-completo/', views.triage_completo, name='triage_completo'),
    
    # 📊 Reporte PDF ultra-simple
    path('reporte-diario/', views.reporte_diario_pdf, name='reporte_diario'),
    
    # Gestión de pacientes - Solo lo esencial
    path('paciente/<int:paciente_id>/atendido/', views.marcar_atendido, name='marcar_atendido'),
    
    # API simple
    path('api/lista-pacientes/', views.api_lista_pacientes, name='api_lista_pacientes'),
    
    # 📱 PWA - Progressive Web App
    path('manifest.json', views.manifest, name='manifest'),
    path('sw.js', views.service_worker, name='service_worker'),
]