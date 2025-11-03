"""
URLs del sistema de triage - Solo rutas esenciales.
Filosofía: "Menos es mejor"
"""

from django.urls import path
from . import views

app_name = 'triage'

urlpatterns = [
    # Dashboard principal - TODO INTEGRADO
    path('', views.dashboard_principal, name='dashboard'),
    
    # 📊 Reporte PDF ultra-simple
    path('reporte-diario/', views.reporte_diario_pdf, name='reporte_diario'),
    
    # Gestión de pacientes - Solo lo esencial
    path('paciente/<int:paciente_id>/atendido/', views.marcar_atendido, name='marcar_atendido'),
    
    # API simple
    path('api/lista-pacientes/', views.api_lista_pacientes, name='api_lista_pacientes'),
    path('api/estadisticas-dashboard/', views.api_estadisticas_dashboard, name='api_estadisticas_dashboard'),
    
    # 📱 PWA - Progressive Web App
    path('manifest.json', views.manifest, name='manifest'),
    path('sw.js', views.service_worker, name='service_worker'),
]