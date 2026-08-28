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
    
    # 📋 Tablero Kanban de Guardia
    path('kanban/', views.kanban_view, name='kanban'),
    
    # 📊 Reporte PDF
    path('reporte-diario/', views.reporte_diario_pdf, name='reporte_diario'),
    
    # Gestión y transición de pacientes
    path('paciente/<int:paciente_id>/iniciar-atencion/', views.iniciar_atencion, name='iniciar_atencion'),
    path('paciente/<int:paciente_id>/atendido/', views.marcar_atendido, name='marcar_atendido'),
    
    # APIs en tiempo real
    path('api/lista-pacientes/', views.api_lista_pacientes, name='api_lista_pacientes'),
    path('api/kanban-pacientes/', views.api_kanban_pacientes, name='api_kanban_pacientes'),
    path('api/estadisticas-dashboard/', views.api_estadisticas_dashboard, name='api_estadisticas_dashboard'),
    
    # 📱 PWA - Progressive Web App
    path('manifest.json', views.manifest, name='manifest'),
    path('sw.js', views.service_worker, name='service_worker'),
]