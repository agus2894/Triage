"""Calculadora NEWS Score - Lógica central de triage médico."""

from typing import Dict, Tuple
from decimal import Decimal


class CalculadoraNEWS:
    """Calculadora NEWS Score optimizada para velocidad médica."""
    
    # Optimización: Tuplas ordenadas por prioridad médica (más rápido que dict)
    RANGOS_CLASIFICACION = (
        ('ROJO', 7, 20),      # Prioridad 1: Riesgo vital inmediato
        ('AMARILLO', 5, 6),   # Prioridad 2: Riesgo moderado
        ('VERDE', 0, 4),      # Prioridad 3: Sin riesgo vital
    )
    
    # Tiempos de atención críticos (protocolo médico argentino)
    TIEMPOS_ATENCION = {
        'ROJO': 0,        # CRÍTICO: Atención inmediata
        'AMARILLO': 30,   # URGENTE: 30 minutos máximo
        'VERDE': 60,      # RUTINARIO: 60 minutos máximo
    }
    
    @staticmethod
    def calcular_puntaje_frecuencia_respiratoria(frecuencia: int) -> int:
        """
        Calcula el puntaje para frecuencia respiratoria.
        
        Args:
            frecuencia: Respiraciones por minuto
            
        Returns:
            Puntaje NEWS (0-3)
        """
        if frecuencia <= 8:
            return 3
        elif 9 <= frecuencia <= 11:
            return 1
        elif 12 <= frecuencia <= 20:
            return 0
        elif 21 <= frecuencia <= 24:
            return 2
        else:  # >= 25
            return 3
    
    @staticmethod
    def calcular_puntaje_saturacion_oxigeno(saturacion: int) -> int:
        """
        Calcula el puntaje para saturación de oxígeno.
        
        Args:
            saturacion: Porcentaje de saturación de O2
            
        Returns:
            Puntaje NEWS (0-3)
        """
        if saturacion <= 91:
            return 3
        elif 92 <= saturacion <= 93:
            return 2
        elif 94 <= saturacion <= 95:
            return 1
        else:  # >= 96
            return 0
    
    @staticmethod
    def calcular_puntaje_presion_sistolica(presion: int) -> int:
        """
        Calcula el puntaje para tensión arterial sistólica.
        
        Args:
            presion: Tensión sistólica en mmHg
            
        Returns:
            Puntaje NEWS (0-3)
        """
        if presion <= 90:
            return 3
        elif 91 <= presion <= 100:
            return 2
        elif 101 <= presion <= 110:
            return 1
        elif 111 <= presion <= 219:
            return 0
        else:  # >= 220
            return 3
    
    @staticmethod
    def calcular_puntaje_frecuencia_cardiaca(frecuencia: int) -> int:
        """
        Calcula el puntaje para frecuencia cardíaca.
        
        Args:
            frecuencia: Latidos por minuto
            
        Returns:
            Puntaje NEWS (0-3)
        """
        if frecuencia <= 40:
            return 3
        elif 41 <= frecuencia <= 50:
            return 1
        elif 51 <= frecuencia <= 90:
            return 0
        elif 91 <= frecuencia <= 110:
            return 1
        elif 111 <= frecuencia <= 130:
            return 2
        else:  # >= 131
            return 3
    
    @staticmethod
    def calcular_puntaje_nivel_conciencia(nivel: str) -> int:
        """
        Calcula el puntaje para nivel de conciencia (AVPU).
        
        Args:
            nivel: Nivel de conciencia ('A', 'V', 'P', 'U')
            
        Returns:
            Puntaje NEWS (0-3)
        """
        if nivel == 'A':  # Alerta
            return 0
        else:  # V, P, U
            return 3
    
    @staticmethod
    def calcular_puntaje_temperatura(temperatura: Decimal) -> int:
        """
        Calcula el puntaje para temperatura corporal.
        
        Args:
            temperatura: Temperatura en grados Celsius
            
        Returns:
            Puntaje NEWS (0-3)
        """
        temp = float(temperatura)
        
        if temp <= 35.0:
            return 3
        elif 35.1 <= temp <= 36.0:
            return 1
        elif 36.1 <= temp <= 38.0:
            return 0
        elif 38.1 <= temp <= 39.0:
            return 2
        else:  # >= 39.1
            return 3
    
    @classmethod
    def calcular_puntaje_total(cls, signos_vitales: Dict) -> Dict:
        """
        Calcula el puntaje total NEWS y determina la clasificación.
        
        Args:
            signos_vitales: Diccionario con los signos vitales
            
        Returns:
            Diccionario con el resultado completo del cálculo
        """
        # Calcular puntajes individuales
        puntajes = {
            'frecuencia_respiratoria': cls.calcular_puntaje_frecuencia_respiratoria(
                signos_vitales['frecuencia_respiratoria']
            ),
            'saturacion_oxigeno': cls.calcular_puntaje_saturacion_oxigeno(
                signos_vitales['saturacion_oxigeno']
            ),
            'presion_sistolica': cls.calcular_puntaje_presion_sistolica(
                signos_vitales['tension_sistolica']
            ),
            'frecuencia_cardiaca': cls.calcular_puntaje_frecuencia_cardiaca(
                signos_vitales['frecuencia_cardiaca']
            ),
            'nivel_conciencia': cls.calcular_puntaje_nivel_conciencia(
                signos_vitales['nivel_conciencia']
            ),
            'temperatura': cls.calcular_puntaje_temperatura(
                signos_vitales['temperatura']
            ),
        }
        
        # Calcular puntaje total
        puntaje_total = sum(puntajes.values())
        
        # Determinar clasificación
        clasificacion = cls.obtener_clasificacion(puntaje_total)
        
        return {
            'puntajes_individuales': puntajes,
            'puntaje_total': puntaje_total,
            'clasificacion': clasificacion,
            'nivel_urgencia': clasificacion,
            'tiempo_atencion_maximo': cls.TIEMPOS_ATENCION[clasificacion],
            'codigo_color': cls.obtener_codigo_color(clasificacion),
        }
    
    @classmethod
    def obtener_clasificacion(cls, puntaje: int) -> str:
        """
        CRÍTICO: Clasificación médica optimizada para velocidad.
        Sistema puede salvar vidas - debe ser RÁPIDO.
        
        Args:
            puntaje: Puntaje total NEWS (0-20)
            
        Returns:
            Nivel de urgencia ('VERDE', 'AMARILLO', 'ROJO')
        """
        # Optimización: Evaluar casos críticos primero (salvar vidas)
        if puntaje >= 7:    # ROJO: Emergencia crítica
            return 'ROJO'
        elif puntaje >= 5:  # AMARILLO: Urgencia moderada  
            return 'AMARILLO'
        else:               # VERDE: Rutinario (0-4)
            return 'VERDE'
    
    @staticmethod
    def obtener_codigo_color(clasificacion: str) -> str:
        """
        Obtiene el código de color hexadecimal para la clasificación.
        
        Args:
            clasificacion: Nivel de urgencia
            
        Returns:
            Código de color hexadecimal
        """
        colores = {
            'VERDE': '#28a745',
            'AMARILLO': '#ffc107',
            'ROJO': '#dc3545'
        }
        return colores.get(clasificacion, '#6c757d')
    
    @classmethod
    def obtener_descripcion_clasificacion(cls, clasificacion: str) -> str:
        """
        Obtiene la descripción completa de la clasificación.
        
        Args:
            clasificacion: Nivel de urgencia
            
        Returns:
            Descripción detallada del nivel de urgencia
        """
        descripciones = {
            'VERDE': 'Verde - Sin riesgo vital (atención dentro de 60 minutos)',
            'AMARILLO': 'Amarillo - Riesgo moderado (atención dentro de 30 minutos)', 
            'ROJO': 'Rojo - Riesgo vital inmediato (atención inmediata)'
        }
        return descripciones.get(clasificacion, 'Clasificación desconocida')