from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Q
from django.db import models
from django.utils import timezone
from django.core.cache import cache
from datetime import timedelta

from apps.patients.models import Paciente
from .models import SignosVitales, Profesional


def _lazy_import_pdf():
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    return canvas, letter


def _crear_signos_vitales(request, paciente, profesional):
    def safe_int(value, default=0):
        if value in [None, '', 'undefined', 'null']:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    def safe_float(value, default=0.0):
        if value in [None, '', 'undefined', 'null']:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def safe_str(value, default=''):
        if value in [None, 'undefined', 'null']:
            return default
        return str(value)
    
    # Validar y convertir valores de forma segura
    frecuencia_respiratoria = safe_int(request.POST.get('frecuencia_respiratoria'))
    saturacion_oxigeno = safe_int(request.POST.get('saturacion_oxigeno'))
    tension_sistolica = safe_int(request.POST.get('tension_sistolica'))
    frecuencia_cardiaca = safe_int(request.POST.get('frecuencia_cardiaca'))
    nivel_conciencia = safe_str(request.POST.get('nivel_conciencia'))
    temperatura = safe_float(request.POST.get('temperatura'))
    
    signos = SignosVitales.objects.create(
        paciente=paciente,
        profesional=profesional,
        frecuencia_respiratoria=frecuencia_respiratoria,
        saturacion_oxigeno=saturacion_oxigeno,
        tension_sistolica=tension_sistolica,
        frecuencia_cardiaca=frecuencia_cardiaca,
        nivel_conciencia=nivel_conciencia,
        temperatura=temperatura
    )
    
    return signos


def _obtener_profesional(request):
    try:
        return request.user.profesional
    except Profesional.DoesNotExist:
        return None


@login_required
@require_http_methods(["GET", "POST"])
def dashboard_principal(request):
    if request.method == 'POST':
        try:
            # Obtener profesional
            profesional = _obtener_profesional(request)
            if not profesional:
                messages.error(request, 'Usuario no tiene perfil de profesional asociado.')
                return redirect('triage:dashboard')
            
            # 1. Crear paciente con datos del formulario
            nombre = request.POST.get('nombre', '').strip() or None
            apellido = request.POST.get('apellido', '').strip() or None
            dni = request.POST.get('dni', '').strip() or None
            edad = request.POST.get('edad')
            
            paciente = Paciente.objects.create(
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                edad=int(edad) if edad else None,
                motivo_consulta=request.POST.get('motivo_consulta', '').strip()
            )
            
            # 2. Crear signos vitales usando helper
            signos = _crear_signos_vitales(request, paciente, profesional)
            
            # 3. Mensaje de éxito
            messages.success(
                request, 
                f'✅ Triage completado para {paciente.nombre_completo}: '
                f'{signos.nivel_urgencia} (NEWS: {signos.news_score}) - '
                f'Tiempo máximo: {signos.tiempo_atencion_max} minutos'
            )
            
            # 4. Limpiar cache para actualización inmediata
            cache.delete('dashboard_stats')
            cache.delete('patients_waiting')
            
            return redirect('triage:dashboard')
            
        except Exception as e:
            messages.error(request, f'❌ Error al completar triage: {str(e)}')
            return redirect('triage:dashboard')
    
    # 🔍 LÓGICA GET ORIGINAL (mostrar dashboard)
    # Intentar obtener del cache primero
    cache_key = 'dashboard_stats'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        # Cache miss - calcular datos
        hace_24h = timezone.now() - timedelta(hours=24)
        
        # 🔥 CONSULTAS OPTIMIZADAS - Usando select_related y prefetch_related
        estadisticas = SignosVitales.objects.filter(
            fecha_hora__gte=hace_24h,
            nivel_urgencia__isnull=False,
            paciente__activo=True,
            paciente__estado_atencion__in=['ESPERANDO', 'EN_ATENCION']
        ).aggregate(
            total=Count('id'),
            rojos=Count('id', filter=Q(nivel_urgencia='ROJO')),
            amarillos=Count('id', filter=Q(nivel_urgencia='AMARILLO')),
            verdes=Count('id', filter=Q(nivel_urgencia='VERDE'))
        )
        
        # Casos críticos - OPTIMIZADO con select_related
        casos_criticos = list(SignosVitales.objects.filter(
            nivel_urgencia__in=['ROJO', 'AMARILLO'],
            paciente__activo=True,
            paciente__estado_atencion__in=['ESPERANDO', 'EN_ATENCION']
        ).select_related(
            'paciente',
            'profesional__user'
        ).order_by('-fecha_hora')[:10])
        
        # Pacientes pendientes (OPTIMIZADO con manager personalizado)
        pacientes_recientes = list(Paciente.objects.activos_en_espera()[:5])
        
        cached_data = {
            'estadisticas': estadisticas,
            'casos_criticos': casos_criticos,
            'pacientes_recientes': pacientes_recientes,
        }
        
        # Cache por 2 minutos (balance entre velocidad y actualización)
        cache.set(cache_key, cached_data, timeout=120)
    
    # 🔒 Agregar información del profesional (no cacheada)
    profesional = _obtener_profesional(request)
    cached_data['profesional'] = profesional
    
    return render(request, 'triage/dashboard.html', cached_data)


@login_required
@require_http_methods(["POST"])
def marcar_atendido(request, paciente_id):
    """Marca un paciente como atendido (AJAX) y actualiza caches."""
    try:
        paciente = get_object_or_404(Paciente, id=paciente_id, activo=True)
        paciente.marcar_atendido()
        
        # 🚀 LIMPIAR CACHES para actualización inmediata
        cache.delete('dashboard_stats')
        cache.delete('patients_waiting')
        
        
        return JsonResponse({
            'success': True,
            'mensaje': f'Paciente {paciente.nombre_completo} marcado como atendido',
            'estado': paciente.get_estado_atencion_display(),
            'tiempo': paciente.tiempo_espera
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_http_methods(["GET"])
def api_lista_pacientes(request):
    """
    API optimizada para obtener lista de pacientes en espera.
    AUTO-CACHE que se invalida automáticamente con signals.
    """
    # Cache inteligente para API
    cache_key = 'patients_waiting'
    cached_patients = cache.get(cache_key)
    
    if cached_patients is None:
        try:
            # Obtener pacientes en espera - USANDO MANAGER OPTIMIZADO
            pacientes = Paciente.objects.activos_en_espera()
            
            data = []
            pacientes_rojos_con_prioridad = []  # 🚨 Para ordenar códigos rojos por prioridad
            
            for paciente in pacientes:
                try:
                    # Obtener último triage si existe - usando prefetch_related
                    nivel_urgencia = 'SIN TRIAGE'
                    prioridad_critica = 0
                    
                    # Usar los signos vitales pre-cargados
                    signos_vitales = list(paciente.signos_vitales.all())
                    if signos_vitales:
                        ultimo_signo = signos_vitales[0]  # Ya ordenados por fecha_hora desc
                        if ultimo_signo.nivel_urgencia:
                            nivel_urgencia = ultimo_signo.nivel_urgencia
                            # 🚨 Calcular prioridad crítica para códigos rojos
                            if nivel_urgencia == 'ROJO':
                                prioridad_critica = ultimo_signo.calcular_prioridad_critica()
                    
                    paciente_data = {
                        'id': paciente.id,
                        'nombre_completo': paciente.nombre_completo,
                        'dni': paciente.dni or 'Sin DNI',
                        'edad': paciente.edad,
                        'tiempo_espera': paciente.tiempo_espera,
                        'tiempo_espera_minutos': paciente.tiempo_espera_minutos,
                        'nivel_urgencia': nivel_urgencia,
                        'motivo_consulta': paciente.motivo_consulta or '',
                        'prioridad_critica': prioridad_critica  # 🚨 Nueva prioridad
                    }
                    
                    if nivel_urgencia == 'ROJO':
                        pacientes_rojos_con_prioridad.append(paciente_data)
                    else:
                        data.append(paciente_data)
                        
                except Exception:
                    continue  # Saltar este paciente pero seguir con los demás
            
            # 🚨 ORDENAR CÓDIGOS ROJOS POR PRIORIDAD CRÍTICA (mayor prioridad primero)
            pacientes_rojos_con_prioridad.sort(key=lambda x: x['prioridad_critica'], reverse=True)
            
            # 🚨 ORDEN FINAL: Rojos priorizados + resto
            data = pacientes_rojos_con_prioridad + data
            
            # Cache por 1 minuto (se invalida automáticamente con signals)
            cache.set(cache_key, data, timeout=60)
            cached_patients = data
            
        except Exception as e:
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)
    
    return JsonResponse(cached_patients, safe=False)


@login_required
def reporte_diario_pdf(request):
    """
    📋 REPORTE PDF COMPLETO PARA ADMINISTRADORES
    🔒 Solo administradores y médicos pueden descargar
    
    Incluye:
    - 👩‍⚕️ Profesional que atendió cada paciente
    - 📊 NEWS Score detallado de cada caso
    - ⏰ Horarios de atención
    - 📈 Estadísticas por profesional
    """
    # 🔒 Verificar permisos de descarga
    profesional = _obtener_profesional(request)
    if not profesional.puede_descargar_reportes():
        messages.error(request, f'❌ Sin permisos para descargar reportes. Tu rol: {profesional.get_tipo_display()}')
        return redirect('triage:dashboard')
    
    # Import lazy para ahorrar memoria
    canvas, letter = _lazy_import_pdf()
    
    # Datos del día actual
    hoy = timezone.now().date()
    
    # 📊 CONSULTA OPTIMIZADA: Todos los datos necesarios en una sola query
    signos_del_dia = SignosVitales.objects.filter(
        fecha_hora__date=hoy
    ).select_related(
        'paciente', 'profesional__user'
    ).order_by('-fecha_hora')
    
    # 📈 Estadísticas generales
    total = signos_del_dia.count()
    rojos = signos_del_dia.filter(nivel_urgencia='ROJO').count()
    amarillos = signos_del_dia.filter(nivel_urgencia='AMARILLO').count()
    verdes = signos_del_dia.filter(nivel_urgencia='VERDE').count()
    
    # 👩‍⚕️ Estadísticas por profesional
    from django.db.models import Count
    stats_profesionales = signos_del_dia.values(
        'profesional__user__first_name',
        'profesional__user__last_name',
        'profesional__tipo'
    ).annotate(
        total_atenciones=Count('id'),
        casos_rojos=Count('id', filter=models.Q(nivel_urgencia='ROJO')),
        casos_amarillos=Count('id', filter=models.Q(nivel_urgencia='AMARILLO')),
        casos_verdes=Count('id', filter=models.Q(nivel_urgencia='VERDE'))
    ).order_by('-total_atenciones')
    
    # Crear PDF completo
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_triage_{hoy}.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # 🏥 HEADER INSTITUCIONAL
    p.setFont("Helvetica-Bold", 24)
    p.drawString(50, height - 50, f"🏥 REPORTE DIARIO DE TRIAGE")
    
    p.setFont("Helvetica", 16)
    p.drawString(50, height - 80, f"📅 Fecha: {hoy.strftime('%d/%m/%Y')}")
    p.drawString(50, height - 100, f"👤 Generado por: {profesional.user.get_full_name()} ({profesional.get_tipo_display()})")
    p.drawString(50, height - 120, f"⏰ Hora: {timezone.now().strftime('%H:%M')}")
    
    # 📊 RESUMEN ESTADÍSTICO
    y_pos = height - 160
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, y_pos, "📊 RESUMEN DEL DÍA")
    
    y_pos -= 30
    p.setFont("Helvetica", 14)
    p.drawString(70, y_pos, f"🔴 Casos Críticos (ROJO): {rojos}")
    y_pos -= 20
    p.drawString(70, y_pos, f"🟡 Casos Urgentes (AMARILLO): {amarillos}")
    y_pos -= 20
    p.drawString(70, y_pos, f"🟢 Casos Leves (VERDE): {verdes}")
    y_pos -= 20
    p.setFont("Helvetica-Bold", 14)
    p.drawString(70, y_pos, f"📈 TOTAL ATENCIONES: {total}")
    
    # 👩‍⚕️ RENDIMIENTO POR PROFESIONAL
    y_pos -= 50
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, y_pos, "👩‍⚕️ RENDIMIENTO POR PROFESIONAL")
    
    y_pos -= 25
    p.setFont("Helvetica-Bold", 12)
    p.drawString(70, y_pos, "PROFESIONAL")
    p.drawString(250, y_pos, "TOTAL")
    p.drawString(300, y_pos, "ROJOS")
    p.drawString(350, y_pos, "AMARILLOS")
    p.drawString(420, y_pos, "VERDES")
    
    y_pos -= 15
    p.setFont("Helvetica", 10)
    for stat in stats_profesionales:
        nombre = f"{stat['profesional__user__first_name']} {stat['profesional__user__last_name']}"
        tipo_icon = "🔧" if stat['profesional__tipo'] == 'administrador' else \
                   "👨‍⚕️" if stat['profesional__tipo'] == 'medico' else "👩‍⚕️"
        
        p.drawString(70, y_pos, f"{tipo_icon} {nombre}")
        p.drawString(260, y_pos, str(stat['total_atenciones']))
        p.drawString(310, y_pos, str(stat['casos_rojos']))
        p.drawString(370, y_pos, str(stat['casos_amarillos']))
        p.drawString(440, y_pos, str(stat['casos_verdes']))
        y_pos -= 15
    
    # 📋 DETALLE DE CASOS (si hay espacio)
    if y_pos > 200 and total <= 15:  # Solo si cabe en la página
        y_pos -= 30
        p.setFont("Helvetica-Bold", 18)
        p.drawString(50, y_pos, "📋 DETALLE DE CASOS")
        
        y_pos -= 25
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y_pos, "HORA")
        p.drawString(100, y_pos, "PACIENTE")
        p.drawString(220, y_pos, "NEWS")
        p.drawString(260, y_pos, "NIVEL")
        p.drawString(320, y_pos, "PROFESIONAL")
        
        y_pos -= 15
        p.setFont("Helvetica", 9)
        
        for signo in signos_del_dia[:15]:  # Máximo 15 casos
            if y_pos < 50:  # Si no hay espacio, parar
                break
                
            hora = signo.fecha_hora.strftime('%H:%M')
            paciente = signo.paciente.nombre_completo[:15]
            news = str(signo.news_score)
            nivel_icon = "🔴" if signo.nivel_urgencia == 'ROJO' else \
                        "🟡" if signo.nivel_urgencia == 'AMARILLO' else "🟢"
            profesional_nombre = signo.profesional.user.first_name[:12]
            
            p.drawString(50, y_pos, hora)
            p.drawString(100, y_pos, paciente)
            p.drawString(230, y_pos, news)
            p.drawString(260, y_pos, f"{nivel_icon} {signo.nivel_urgencia}")
            p.drawString(320, y_pos, profesional_nombre)
            y_pos -= 12
    
    # 📝 FOOTER
    p.setFont("Helvetica", 8)
    p.drawString(50, 30, f"📄 Reporte generado por Sistema Triage Digital - {timezone.now().strftime('%d/%m/%Y %H:%M')}")
    p.drawString(50, 20, f"🔒 Acceso autorizado para: {profesional.get_tipo_display()}")
    
    # Finalizar PDF
    p.showPage()
    p.save()
    
    return response
    p.drawString(50, 750, f"🏥 REPORTE TRIAGE DIARIO - {hoy.strftime('%d/%m/%Y')}")
    
    # Datos esenciales
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 700, "📊 RESUMEN DEL DÍA:")
    
    p.setFont("Helvetica", 14)
    p.drawString(70, 670, f"🔴 CRÍTICOS (ROJO): {rojos} pacientes")
    p.drawString(70, 650, f"🟡 MODERADOS (AMARILLO): {amarillos} pacientes")
    p.drawString(70, 630, f"🟢 ESTABLES (VERDE): {verdes} pacientes")
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(70, 600, f"📈 TOTAL ATENDIDOS: {total} pacientes")
    
    # Pie simple
    p.setFont("Helvetica", 10)
    p.drawString(50, 50, f"Generado el {timezone.now().strftime('%d/%m/%Y %H:%M')} | Sistema Triage Digital")
    
    p.showPage()
    p.save()
    
    return response


@login_required
def api_estadisticas_dashboard(request):
    """
    API para obtener estadísticas del dashboard en tiempo real.
    🚀 OPTIMIZADA para actualizaciones inmediatas post-atención.
    """
    hace_24h = timezone.now() - timedelta(hours=24)
    
    # Calcular estadísticas actualizadas
    estadisticas = SignosVitales.objects.filter(
        fecha_hora__gte=hace_24h,
        nivel_urgencia__isnull=False,
        paciente__activo=True,
        paciente__estado_atencion__in=['ESPERANDO', 'EN_ATENCION']
    ).aggregate(
        total=Count('id'),
        rojos=Count('id', filter=Q(nivel_urgencia='ROJO')),
        amarillos=Count('id', filter=Q(nivel_urgencia='AMARILLO')),
        verdes=Count('id', filter=Q(nivel_urgencia='VERDE'))
    )
    
    # Limpiar cache del dashboard para que se actualice
    cache.delete('dashboard_stats')
    
    return JsonResponse({
        'success': True,
        'rojos': estadisticas['rojos'],
        'amarillos': estadisticas['amarillos'],
        'verdes': estadisticas['verdes'],
        'total': estadisticas['total'],
        'timestamp': timezone.now().isoformat()
    })


def manifest(request):
    """
    📱 PWA Manifest - Configuración para app instalable.
    Permite instalar Triage Digital como app nativa.
    """
    return render(request, 'triage/manifest.json', content_type='application/manifest+json')


def service_worker(request):
    """
    🔧 Service Worker - Funcionalidad offline para emergencias.
    Permite usar el sistema sin conexión en situaciones críticas.
    """
    return render(request, 'triage/sw.js', content_type='application/javascript')
