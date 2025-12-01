"""
╔══════════════════════════════════════════════════════════════════╗
║         ANALIZADOR DE SENTIMIENTOS - SISTEMA SENTIMIENTOS       ║
╚══════════════════════════════════════════════════════════════════╝

Módulo para analizar el sentimiento de noticias usando VADER y NLP
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import re
from typing import Dict, List, Tuple
import os

# Importar configuración
import config_sentimientos as cfg

# Configurar logging
logging.basicConfig(
    level=getattr(logging, cfg.NIVEL_LOG),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AnalizadorSentimientos:
    """
    Analiza el sentimiento de noticias financieras relacionadas con EUR/USD
    """
    
    def __init__(self):
        """Inicializa el analizador de sentimientos"""
        self.analyzer = SentimentIntensityAnalyzer()
        
        # Diccionario de términos financieros específicos
        self._agregar_lexico_financiero()
        
        if cfg.MODO_VERBOSE:
            logger.info("✅ Analizador de sentimientos inicializado")
    
    
    def _agregar_lexico_financiero(self):
        """Agrega términos financieros específicos al lexicón de VADER"""
        
        # Términos positivos para EUR
        terminos_positivos = {
            'strengthen': 2.5,
            'surge': 3.0,
            'rally': 2.8,
            'gain': 2.0,
            'rise': 2.0,
            'bullish': 2.5,
            'upside': 2.0,
            'support': 1.5,
            'recovery': 2.0,
            'growth': 2.0,
            'expansion': 2.0,
            'optimism': 2.5,
            'confidence': 2.0
        }
        
        # Términos negativos para EUR
        terminos_negativos = {
            'weaken': -2.5,
            'plunge': -3.0,
            'crash': -3.5,
            'fall': -2.0,
            'drop': -2.0,
            'bearish': -2.5,
            'downside': -2.0,
            'resistance': -1.5,
            'recession': -3.0,
            'contraction': -2.5,
            'concern': -2.0,
            'fear': -2.5,
            'risk': -1.5
        }
        
        # Actualizar lexicón de VADER
        self.analyzer.lexicon.update(terminos_positivos)
        self.analyzer.lexicon.update(terminos_negativos)
    
    
    def _detectar_entidades(self, texto: str) -> Dict[str, bool]:
        """
        Detecta entidades importantes en el texto
        
        Args:
            texto: Texto a analizar
        
        Returns:
            Diccionario con entidades detectadas
        """
        texto_lower = texto.lower()
        
        return {
            'menciona_ecb': any(word in texto_lower for word in ['ecb', 'european central bank', 'lagarde']),
            'menciona_fed': any(word in texto_lower for word in ['fed', 'federal reserve', 'powell', 'fomc']),
            'menciona_eur': any(word in texto_lower for word in ['eur', 'euro', 'eurozone', 'europe']),
            'menciona_usd': any(word in texto_lower for word in ['usd', 'dollar', 'us economy', 'united states']),
            'dato_economico': any(word in texto_lower for word in ['gdp', 'pib', 'inflation', 'cpi', 'pce', 'nfp', 'employment']),
            'decision_tasas': any(word in texto_lower for word in ['interest rate', 'tasa', 'monetary policy'])
        }
    
    
    def _calcular_multiplicador_evento(self, entidades: Dict[str, bool]) -> float:
        """
        Calcula el multiplicador basado en el tipo de evento detectado
        
        Args:
            entidades: Diccionario de entidades detectadas
        
        Returns:
            Multiplicador a aplicar al sentimiento
        """
        multiplicador = 1.0
        
        # Eventos del ECB tienen prioridad máxima
        if entidades['menciona_ecb']:
            multiplicador = max(multiplicador, cfg.MULTIPLICADOR_EVENTO_ECB)
        
        # Eventos de la Fed
        if entidades['menciona_fed']:
            multiplicador = max(multiplicador, cfg.MULTIPLICADOR_EVENTO_FED)
        
        # Datos económicos importantes
        if entidades['dato_economico']:
            multiplicador = max(multiplicador, cfg.MULTIPLICADOR_DATO_ECONOMICO)
        
        # Decisiones de tasas
        if entidades['decision_tasas']:
            multiplicador = max(multiplicador, cfg.MULTIPLICADOR_EVENTO_ECB)
        
        return multiplicador
    
    
    def _calcular_peso_temporal(self, fecha: pd.Timestamp) -> float:
        """
        Calcula el peso de una noticia según su antigüedad
        
        Args:
            fecha: Fecha de la noticia
        
        Returns:
            Peso a aplicar (0.0 - 1.0)
        """
        ahora = pd.Timestamp.now(tz='UTC')
        diferencia = ahora - fecha
        horas = diferencia.total_seconds() / 3600
        
        if horas <= 2:
            return cfg.PESO_ULTIMAS_2H
        elif horas <= 12:
            return cfg.PESO_ULTIMAS_12H
        elif horas <= 24:
            return cfg.PESO_ULTIMAS_24H
        else:
            return cfg.PESO_MAS_24H
    
    
    def _determinar_direccion_eur(self, texto: str, sentimiento_compuesto: float) -> str:
        """
        Determina si el sentimiento es positivo o negativo para el EUR
        
        Args:
            texto: Texto de la noticia
            sentimiento_compuesto: Score de sentimiento (-1 a 1)
        
        Returns:
            'POSITIVO_EUR', 'NEGATIVO_EUR', o 'NEUTRAL'
        """
        texto_lower = texto.lower()
        
        # Detectar si habla principalmente del EUR o USD
        menciones_eur = sum([1 for word in ['eur', 'euro', 'eurozone', 'europe'] if word in texto_lower])
        menciones_usd = sum([1 for word in ['usd', 'dollar', 'us economy', 'united states'] if word in texto_lower])
        
        # Si el sentimiento es neutral
        if abs(sentimiento_compuesto) < 0.05:
            return 'NEUTRAL'
        
        # Si habla más del EUR
        if menciones_eur >= menciones_usd:
            # Sentimiento positivo = EUR sube = POSITIVO_EUR
            return 'POSITIVO_EUR' if sentimiento_compuesto > 0 else 'NEGATIVO_EUR'
        
        # Si habla más del USD
        elif menciones_usd > menciones_eur:
            # Sentimiento positivo del USD = EUR baja = NEGATIVO_EUR
            return 'NEGATIVO_EUR' if sentimiento_compuesto > 0 else 'POSITIVO_EUR'
        
        # Si no está claro, usar el sentimiento directo
        else:
            return 'POSITIVO_EUR' if sentimiento_compuesto > 0 else 'NEGATIVO_EUR'
    
    
    def analizar_noticia(self, noticia: Dict) -> Dict:
        """
        Analiza el sentimiento de una noticia individual
        
        Args:
            noticia: Diccionario con datos de la noticia
        
        Returns:
            Diccionario con análisis completo
        """
        texto = noticia.get('texto_completo', '')
        
        # Análisis VADER
        scores = self.analyzer.polarity_scores(texto)
        
        # Detectar entidades
        entidades = self._detectar_entidades(texto)
        
        # Calcular multiplicadores
        mult_evento = self._calcular_multiplicador_evento(entidades)
        peso_temporal = self._calcular_peso_temporal(noticia['fecha'])
        peso_fuente = cfg.PESO_FUENTES.get(noticia['fuente'], 0.8)
        
        # Sentimiento ajustado
        sentimiento_base = scores['compound']
        sentimiento_ajustado = sentimiento_base * mult_evento
        
        # Determinar dirección para EUR
        direccion = self._determinar_direccion_eur(texto, sentimiento_base)
        
        # Peso final
        peso_final = peso_temporal * peso_fuente * mult_evento
        
        return {
            **noticia,
            'sentimiento_positivo': scores['pos'],
            'sentimiento_negativo': scores['neg'],
            'sentimiento_neutral': scores['neu'],
            'sentimiento_compuesto': sentimiento_base,
            'sentimiento_ajustado': sentimiento_ajustado,
            'direccion_eur': direccion,
            'peso_temporal': peso_temporal,
            'peso_fuente': peso_fuente,
            'multiplicador_evento': mult_evento,
            'peso_final': peso_final,
            **entidades
        }
    
    
    def analizar_lote_noticias(self, df_noticias: pd.DataFrame) -> pd.DataFrame:
        """
        Analiza un lote de noticias
        
        Args:
            df_noticias: DataFrame con noticias
        
        Returns:
            DataFrame con análisis de sentimientos
        """
        if df_noticias.empty:
            logger.warning("⚠️ No hay noticias para analizar")
            return pd.DataFrame()
        
        logger.info("\n" + "="*70)
        logger.info("🧠 INICIANDO ANÁLISIS DE SENTIMIENTOS")
        logger.info("="*70)
        
        # Analizar cada noticia
        noticias_analizadas = []
        
        for idx, row in df_noticias.iterrows():
            try:
                noticia_dict = row.to_dict()
                analisis = self.analizar_noticia(noticia_dict)
                noticias_analizadas.append(analisis)
            
            except Exception as e:
                logger.error(f"❌ Error analizando noticia {idx}: {e}")
                continue
        
        # Convertir a DataFrame
        df_analizado = pd.DataFrame(noticias_analizadas)
        
        logger.info(f"✅ ANÁLISIS COMPLETADO: {len(df_analizado)} noticias analizadas")
        logger.info("="*70 + "\n")
        
        # Guardar resultados
        if cfg.GUARDAR_HISTORICO:
            self._guardar_analisis(df_analizado)
        
        return df_analizado
    
    
    def _guardar_analisis(self, df: pd.DataFrame):
        """Guarda el análisis de sentimientos"""
        try:
            df.to_csv(cfg.ARCHIVO_NOTICIAS_ANALIZADAS, index=False)
            logger.info(f"💾 Análisis guardado en {cfg.ARCHIVO_NOTICIAS_ANALIZADAS}")
        except Exception as e:
            logger.error(f"❌ Error guardando análisis: {e}")
    
    
    def calcular_sentimiento_agregado(self, df_analizado: pd.DataFrame) -> Dict:
        """
        Calcula el sentimiento agregado ponderado
        
        Args:
            df_analizado: DataFrame con noticias analizadas
        
        Returns:
            Diccionario con métricas agregadas
        """
        if df_analizado.empty:
            return {
                'sentimiento_promedio': 0.0,
                'sentimiento_ponderado': 0.0,
                'balance_direccion': 0.0,
                'total_noticias': 0,
                'noticias_positivas': 0,
                'noticias_negativas': 0,
                'noticias_neutrales': 0,
                'confianza': 0
            }
        
        # Sentimiento promedio simple
        sentimiento_promedio = df_analizado['sentimiento_compuesto'].mean()
        
        # Sentimiento ponderado (considerando pesos)
        sentimiento_ponderado = np.average(
            df_analizado['sentimiento_ajustado'],
            weights=df_analizado['peso_final']
        )
        
        # Balance de direcciones
        positivas = len(df_analizado[df_analizado['direccion_eur'] == 'POSITIVO_EUR'])
        negativas = len(df_analizado[df_analizado['direccion_eur'] == 'NEGATIVO_EUR'])
        neutrales = len(df_analizado[df_analizado['direccion_eur'] == 'NEUTRAL'])
        
        total = len(df_analizado)
        balance = (positivas - negativas) / total if total > 0 else 0
        
        # Confianza (basada en consenso)
        if total > 0:
            max_direccion = max(positivas, negativas, neutrales)
            confianza = (max_direccion / total) * 100
        else:
            confianza = 0
        
        return {
            'sentimiento_promedio': round(sentimiento_promedio, 4),
            'sentimiento_ponderado': round(sentimiento_ponderado, 4),
            'balance_direccion': round(balance, 4),
            'total_noticias': total,
            'noticias_positivas': positivas,
            'noticias_negativas': negativas,
            'noticias_neutrales': neutrales,
            'confianza': round(confianza, 2)
        }
    
    
    def mostrar_resumen_sentimientos(self, df_analizado: pd.DataFrame):
        """Muestra un resumen del análisis de sentimientos"""
        if df_analizado.empty:
            print("❌ No hay datos de sentimiento para mostrar")
            return
        
        metricas = self.calcular_sentimiento_agregado(df_analizado)
        
        print("\n" + "="*70)
        print("📊 RESUMEN DE ANÁLISIS DE SENTIMIENTOS")
        print("="*70)
        
        print(f"\n📈 Métricas globales:")
        print(f"   Total noticias:          {metricas['total_noticias']}")
        print(f"   Sentimiento promedio:    {metricas['sentimiento_promedio']:.4f}")
        print(f"   Sentimiento ponderado:   {metricas['sentimiento_ponderado']:.4f}")
        print(f"   Balance EUR:             {metricas['balance_direccion']:.4f}")
        print(f"   Confianza:               {metricas['confianza']:.1f}%")
        
        print(f"\n📊 Distribución:")
        print(f"   Positivas EUR: {metricas['noticias_positivas']} ({metricas['noticias_positivas']/metricas['total_noticias']*100:.1f}%)")
        print(f"   Negativas EUR: {metricas['noticias_negativas']} ({metricas['noticias_negativas']/metricas['total_noticias']*100:.1f}%)")
        print(f"   Neutrales:     {metricas['noticias_neutrales']} ({metricas['noticias_neutrales']/metricas['total_noticias']*100:.1f}%)")
        
        # Top noticias por impacto
        print("\n🔝 Top 5 noticias por impacto:")
        top_impacto = df_analizado.nlargest(5, 'peso_final')
        
        for idx, row in top_impacto.iterrows():
            print(f"\n   [{row['fuente']}] {row['direccion_eur']}")
            print(f"   {row['titulo'][:80]}...")
            print(f"   Sentimiento: {row['sentimiento_ajustado']:.3f} | Peso: {row['peso_final']:.3f}")
        
        print("\n" + "="*70 + "\n")


# ═══════════════════════════════════════════════════════════════
# 🧪 MODO DE PRUEBA
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 MODO DE PRUEBA - ANALIZADOR DE SENTIMIENTOS")
    print("="*70 + "\n")
    
    # Crear analizador
    analizador = AnalizadorSentimientos()
    
    # Noticias de ejemplo
    noticias_ejemplo = pd.DataFrame([
        {
            'fuente': 'FXStreet',
            'titulo': 'EUR/USD rallies on ECB hawkish comments',
            'descripcion': 'The euro strengthens against the dollar after ECB signals further rate hikes',
            'texto_completo': 'EUR/USD rallies on ECB hawkish comments. The euro strengthens against the dollar after ECB signals further rate hikes',
            'fecha': pd.Timestamp.now(tz='UTC') - timedelta(hours=1)
        },
        {
            'fuente': 'ForexLive',
            'titulo': 'US dollar gains on strong NFP data',
            'descripcion': 'Dollar surges as jobs report beats expectations',
            'texto_completo': 'US dollar gains on strong NFP data. Dollar surges as jobs report beats expectations',
            'fecha': pd.Timestamp.now(tz='UTC') - timedelta(hours=3)
        },
        {
            'fuente': 'Investing.com',
            'titulo': 'EUR/USD remains neutral ahead of Fed decision',
            'descripcion': 'Traders await FOMC meeting results',
            'texto_completo': 'EUR/USD remains neutral ahead of Fed decision. Traders await FOMC meeting results',
            'fecha': pd.Timestamp.now(tz='UTC') - timedelta(hours=12)
        }
    ])
    
    # Analizar
    df_analizado = analizador.analizar_lote_noticias(noticias_ejemplo)
    
    # Mostrar resumen
    analizador.mostrar_resumen_sentimientos(df_analizado)
    
    print("✅ Prueba completada")
