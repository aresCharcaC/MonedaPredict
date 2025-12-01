"""
╔══════════════════════════════════════════════════════════════════╗
║       GENERADOR DE SEÑALES - SISTEMA SENTIMIENTOS EUR/USD        ║
╚══════════════════════════════════════════════════════════════════╝

Módulo para generar señales de trading basadas en análisis de sentimiento
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, Optional, Tuple
import os

# Importar módulos del sistema
import config_sentimientos as cfg
from recolector_noticias import RecolectorNoticias
from analizador_sentimientos import AnalizadorSentimientos

# Configurar logging
logging.basicConfig(
    level=getattr(logging, cfg.NIVEL_LOG),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GeneradorSeñalesSentimiento:
    """
    Genera señales de trading basadas en el análisis de sentimiento de noticias
    """
    
    def __init__(self):
        """Inicializa el generador de señales"""
        self.recolector = RecolectorNoticias()
        self.analizador = AnalizadorSentimientos()
        
        # Crear carpetas
        os.makedirs(cfg.CARPETA_DATOS, exist_ok=True)
        os.makedirs(cfg.CARPETA_REPORTES, exist_ok=True)
        
        if cfg.MODO_VERBOSE:
            logger.info("✅ Generador de señales inicializado")
    
    
    def _calcular_niveles_temporales(self, df_analizado: pd.DataFrame) -> Dict[str, Dict]:
        """
        Calcula sentimiento para diferentes horizontes temporales
        
        Args:
            df_analizado: DataFrame con noticias analizadas
        
        Returns:
            Diccionario con métricas por horizonte temporal
        """
        ahora = pd.Timestamp.now(tz='UTC')
        
        niveles = {}
        
        # Corto plazo (últimas 4 horas)
        df_corto = df_analizado[
            df_analizado['fecha'] >= (ahora - timedelta(hours=cfg.HORIZONTE_CORTO_PLAZO))
        ]
        niveles['corto_plazo'] = self.analizador.calcular_sentimiento_agregado(df_corto)
        niveles['corto_plazo']['horizonte'] = cfg.HORIZONTE_CORTO_PLAZO
        
        # Medio plazo (últimas 12 horas)
        df_medio = df_analizado[
            df_analizado['fecha'] >= (ahora - timedelta(hours=cfg.HORIZONTE_MEDIO_PLAZO))
        ]
        niveles['medio_plazo'] = self.analizador.calcular_sentimiento_agregado(df_medio)
        niveles['medio_plazo']['horizonte'] = cfg.HORIZONTE_MEDIO_PLAZO
        
        # Largo plazo (últimas 24 horas)
        df_largo = df_analizado[
            df_analizado['fecha'] >= (ahora - timedelta(hours=cfg.HORIZONTE_LARGO_PLAZO))
        ]
        niveles['largo_plazo'] = self.analizador.calcular_sentimiento_agregado(df_largo)
        niveles['largo_plazo']['horizonte'] = cfg.HORIZONTE_LARGO_PLAZO
        
        return niveles
    
    
    def _determinar_señal_base(self, metricas: Dict) -> Tuple[str, float]:
        """
        Determina la señal base según las métricas de sentimiento
        
        Args:
            metricas: Diccionario con métricas de sentimiento
        
        Returns:
            Tupla (señal, confianza)
        """
        # Verificar cantidad mínima de noticias
        if metricas['total_noticias'] < cfg.NOTICIAS_MINIMAS:
            return 'ESPERA', 0
        
        sentimiento = metricas['sentimiento_ponderado']
        balance = metricas['balance_direccion']
        confianza_base = metricas['confianza']
        
        # Determinar señal según balance y sentimiento
        if balance >= cfg.BALANCE_MINIMO_FUERTE:
            # Mayoría de noticias positivas para EUR
            if sentimiento > cfg.UMBRAL_POSITIVO:
                señal = 'COMPRA'  # Comprar EUR/USD
            else:
                señal = 'ESPERA'
        
        elif balance <= -cfg.BALANCE_MINIMO_FUERTE:
            # Mayoría de noticias negativas para EUR
            if sentimiento < cfg.UMBRAL_NEGATIVO:
                señal = 'VENTA'  # Vender EUR/USD
            else:
                señal = 'ESPERA'
        
        else:
            # No hay consenso claro
            señal = 'ESPERA'
        
        # Ajustar confianza según umbrales
        if señal == 'COMPRA' and confianza_base < cfg.CONFIANZA_MINIMA_COMPRA:
            señal = 'ESPERA'
            confianza_base = confianza_base * 0.5
        
        elif señal == 'VENTA' and confianza_base < cfg.CONFIANZA_MINIMA_VENTA:
            señal = 'ESPERA'
            confianza_base = confianza_base * 0.5
        
        return señal, confianza_base
    
    
    def _determinar_urgencia(self, niveles: Dict) -> str:
        """
        Determina el nivel de urgencia de la señal
        
        Args:
            niveles: Diccionario con señales por horizonte
        
        Returns:
            'ALTA', 'MEDIA', o 'BAJA'
        """
        # Obtener señales por horizonte
        señal_corto = niveles['corto_plazo'].get('señal', 'ESPERA')
        señal_medio = niveles['medio_plazo'].get('señal', 'ESPERA')
        señal_largo = niveles['largo_plazo'].get('señal', 'ESPERA')
        
        # Si todos los horizontes coinciden -> ALTA urgencia
        if señal_corto == señal_medio == señal_largo and señal_corto != 'ESPERA':
            return 'ALTA'
        
        # Si 2 de 3 coinciden -> MEDIA urgencia
        elif (señal_corto == señal_medio) or (señal_corto == señal_largo) or (señal_medio == señal_largo):
            if señal_corto != 'ESPERA' or señal_medio != 'ESPERA':
                return 'MEDIA'
        
        # Otros casos -> BAJA urgencia
        return 'BAJA'
    
    
    def generar_señal_completa(self) -> Dict:
        """
        Genera una señal completa con todos los análisis
        
        Returns:
            Diccionario con señal y métricas
        """
        logger.info("\n" + "═"*70)
        logger.info("🎯 GENERANDO SEÑAL DE TRADING - SISTEMA DE SENTIMIENTOS")
        logger.info("═"*70)
        
        # 1. Recolectar noticias
        df_noticias = self.recolector.recolectar_noticias()
        
        if df_noticias.empty:
            logger.warning("⚠️ No hay noticias disponibles")
            return self._señal_vacia()
        
        # 2. Analizar sentimientos
        df_analizado = self.analizador.analizar_lote_noticias(df_noticias)
        
        if df_analizado.empty:
            logger.warning("⚠️ No se pudo analizar las noticias")
            return self._señal_vacia()
        
        # 3. Calcular niveles temporales
        niveles = self._calcular_niveles_temporales(df_analizado)
        
        # 4. Generar señales por horizonte
        for plazo in ['corto_plazo', 'medio_plazo', 'largo_plazo']:
            señal, confianza = self._determinar_señal_base(niveles[plazo])
            niveles[plazo]['señal'] = señal
            niveles[plazo]['confianza_señal'] = confianza
        
        # 5. Determinar señal principal (medio plazo)
        señal_principal = niveles['medio_plazo']['señal']
        confianza_principal = niveles['medio_plazo']['confianza_señal']
        
        # 6. Determinar urgencia
        urgencia = self._determinar_urgencia(niveles)
        
        # 7. Compilar resultado
        resultado = {
            'timestamp': pd.Timestamp.now(tz='UTC'),
            'señal': señal_principal,
            'confianza': round(confianza_principal, 2),
            'urgencia': urgencia,
            'total_noticias': len(df_analizado),
            'sentimiento_general': round(niveles['medio_plazo']['sentimiento_ponderado'], 4),
            'balance_eur': round(niveles['medio_plazo']['balance_direccion'], 4),
            
            # Por horizonte
            'señal_corto_plazo': niveles['corto_plazo']['señal'],
            'confianza_corto_plazo': round(niveles['corto_plazo']['confianza_señal'], 2),
            'noticias_corto_plazo': niveles['corto_plazo']['total_noticias'],
            
            'señal_medio_plazo': niveles['medio_plazo']['señal'],
            'confianza_medio_plazo': round(niveles['medio_plazo']['confianza_señal'], 2),
            'noticias_medio_plazo': niveles['medio_plazo']['total_noticias'],
            
            'señal_largo_plazo': niveles['largo_plazo']['señal'],
            'confianza_largo_plazo': round(niveles['largo_plazo']['confianza_señal'], 2),
            'noticias_largo_plazo': niveles['largo_plazo']['total_noticias'],
        }
        
        # 8. Guardar señal
        self._guardar_señal(resultado)
        
        logger.info(f"\n✅ SEÑAL GENERADA: {señal_principal} (Confianza: {confianza_principal:.1f}%, Urgencia: {urgencia})")
        logger.info("═"*70 + "\n")
        
        return resultado
    
    
    def _señal_vacia(self) -> Dict:
        """Retorna una señal vacía/neutra"""
        return {
            'timestamp': pd.Timestamp.now(tz='UTC'),
            'señal': 'ESPERA',
            'confianza': 0,
            'urgencia': 'BAJA',
            'total_noticias': 0,
            'sentimiento_general': 0,
            'balance_eur': 0,
            'señal_corto_plazo': 'ESPERA',
            'confianza_corto_plazo': 0,
            'noticias_corto_plazo': 0,
            'señal_medio_plazo': 'ESPERA',
            'confianza_medio_plazo': 0,
            'noticias_medio_plazo': 0,
            'señal_largo_plazo': 'ESPERA',
            'confianza_largo_plazo': 0,
            'noticias_largo_plazo': 0
        }
    
    
    def _guardar_señal(self, señal: Dict):
        """Guarda la señal generada en archivo CSV"""
        try:
            # Convertir a DataFrame
            df_señal = pd.DataFrame([señal])
            
            # Agregar o actualizar archivo
            if os.path.exists(cfg.ARCHIVO_SEÑALES):
                df_existente = pd.read_csv(cfg.ARCHIVO_SEÑALES)
                df_existente['timestamp'] = pd.to_datetime(df_existente['timestamp'], utc=True)
                df_completo = pd.concat([df_existente, df_señal], ignore_index=True)
            else:
                df_completo = df_señal
            
            # Guardar
            df_completo.to_csv(cfg.ARCHIVO_SEÑALES, index=False)
            logger.info(f"💾 Señal guardada en {cfg.ARCHIVO_SEÑALES}")
            
            # Guardar histórico
            if cfg.GUARDAR_HISTORICO:
                self._actualizar_historico(df_completo)
        
        except Exception as e:
            logger.error(f"❌ Error guardando señal: {e}")
    
    
    def _actualizar_historico(self, df_señales: pd.DataFrame):
        """Mantiene histórico de señales con límite de días"""
        try:
            # Filtrar por días de histórico
            limite_fecha = pd.Timestamp.now(tz='UTC') - timedelta(days=cfg.DIAS_HISTORICO)
            df_filtrado = df_señales[df_señales['timestamp'] >= limite_fecha]
            
            # Guardar histórico
            df_filtrado.to_csv(cfg.ARCHIVO_HISTORICO, index=False)
            
        except Exception as e:
            logger.error(f"❌ Error actualizando histórico: {e}")
    
    
    def obtener_ultima_señal(self) -> Optional[Dict]:
        """Obtiene la última señal generada"""
        try:
            if os.path.exists(cfg.ARCHIVO_SEÑALES):
                df = pd.read_csv(cfg.ARCHIVO_SEÑALES)
                if not df.empty:
                    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
                    ultima = df.iloc[-1].to_dict()
                    return ultima
        except Exception as e:
            logger.error(f"❌ Error obteniendo última señal: {e}")
        
        return None
    
    
    def mostrar_señal(self, señal: Dict):
        """Muestra la señal de forma visual"""
        
        # Símbolos por señal
        simbolos = {
            'COMPRA': '📈 🟢',
            'VENTA': '📉 🔴',
            'ESPERA': '⏸️  ⚪'
        }
        
        # Colores por urgencia
        urgencia_simbolos = {
            'ALTA': '🔴',
            'MEDIA': '🟡',
            'BAJA': '🟢'
        }
        
        print("\n" + "═"*70)
        print("🎯 SEÑAL DE TRADING - SISTEMA DE SENTIMIENTOS EUR/USD")
        print("═"*70)
        
        print(f"\n{simbolos.get(señal['señal'], '⚪')} SEÑAL PRINCIPAL: {señal['señal']}")
        print(f"   Confianza:   {señal['confianza']:.1f}%")
        print(f"   Urgencia:    {urgencia_simbolos[señal['urgencia']]} {señal['urgencia']}")
        print(f"   Timestamp:   {señal['timestamp']}")
        
        print(f"\n📊 Análisis General:")
        print(f"   Total noticias:      {señal['total_noticias']}")
        print(f"   Sentimiento EUR:     {señal['sentimiento_general']:.4f}")
        print(f"   Balance EUR:         {señal['balance_eur']:.4f}")
        
        print(f"\n⏰ Por Horizonte Temporal:")
        
        # Corto plazo
        print(f"\n   📅 Corto Plazo (4h):")
        print(f"      Señal:      {simbolos.get(señal['señal_corto_plazo'], '⚪')} {señal['señal_corto_plazo']}")
        print(f"      Confianza:  {señal['confianza_corto_plazo']:.1f}%")
        print(f"      Noticias:   {señal['noticias_corto_plazo']}")
        
        # Medio plazo
        print(f"\n   📅 Medio Plazo (12h):")
        print(f"      Señal:      {simbolos.get(señal['señal_medio_plazo'], '⚪')} {señal['señal_medio_plazo']}")
        print(f"      Confianza:  {señal['confianza_medio_plazo']:.1f}%")
        print(f"      Noticias:   {señal['noticias_medio_plazo']}")
        
        # Largo plazo
        print(f"\n   📅 Largo Plazo (24h):")
        print(f"      Señal:      {simbolos.get(señal['señal_largo_plazo'], '⚪')} {señal['señal_largo_plazo']}")
        print(f"      Confianza:  {señal['confianza_largo_plazo']:.1f}%")
        print(f"      Noticias:   {señal['noticias_largo_plazo']}")
        
        print("\n" + "═"*70)
        
        # Interpretación
        self._mostrar_interpretacion(señal)
    
    
    def _mostrar_interpretacion(self, señal: Dict):
        """Muestra interpretación de la señal"""
        print("\n💡 INTERPRETACIÓN:")
        
        if señal['señal'] == 'COMPRA':
            print("   El análisis de sentimiento sugiere comprar EUR/USD.")
            print("   Las noticias recientes son mayormente positivas para el euro.")
            
            if señal['urgencia'] == 'ALTA':
                print("   ⚠️ Urgencia ALTA: Los tres horizontes temporales coinciden.")
            elif señal['urgencia'] == 'MEDIA':
                print("   ⚠️ Urgencia MEDIA: Hay consenso en 2 de 3 horizontes.")
        
        elif señal['señal'] == 'VENTA':
            print("   El análisis de sentimiento sugiere vender EUR/USD.")
            print("   Las noticias recientes son mayormente negativas para el euro.")
            
            if señal['urgencia'] == 'ALTA':
                print("   ⚠️ Urgencia ALTA: Los tres horizontes temporales coinciden.")
            elif señal['urgencia'] == 'MEDIA':
                print("   ⚠️ Urgencia MEDIA: Hay consenso en 2 de 3 horizontes.")
        
        else:  # ESPERA
            print("   No hay una señal clara. Se recomienda esperar.")
            
            if señal['total_noticias'] < cfg.NOTICIAS_MINIMAS:
                print(f"   ℹ️ Información insuficiente (mínimo {cfg.NOTICIAS_MINIMAS} noticias)")
            elif señal['confianza'] < 50:
                print("   ℹ️ Baja confianza en la señal. Sentimiento mixto.")
        
        print("═"*70 + "\n")


# ═══════════════════════════════════════════════════════════════
# 🧪 MODO DE PRUEBA
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 MODO DE PRUEBA - GENERADOR DE SEÑALES")
    print("="*70 + "\n")
    
    # Crear generador
    generador = GeneradorSeñalesSentimiento()
    
    # Generar señal
    señal = generador.generar_señal_completa()
    
    # Mostrar señal
    generador.mostrar_señal(señal)
    
    print("✅ Prueba completada")
