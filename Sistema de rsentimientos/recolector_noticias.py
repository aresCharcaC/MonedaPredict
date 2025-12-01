"""
╔══════════════════════════════════════════════════════════════════╗
║           RECOLECTOR DE NOTICIAS - SISTEMA SENTIMIENTOS          ║
╚══════════════════════════════════════════════════════════════════╝

Módulo para recolectar noticias de múltiples fuentes relacionadas con EUR/USD
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import logging
import re
from typing import List, Dict, Optional
import os

# Importar configuración
import config_sentimientos as cfg

# Configurar logging
logging.basicConfig(
    level=getattr(logging, cfg.NIVEL_LOG),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RecolectorNoticias:
    """
    Recolecta noticias de múltiples fuentes RSS relacionadas con EUR/USD
    """
    
    def __init__(self):
        """Inicializa el recolector de noticias"""
        self.noticias = []
        self.fuentes_activas = self._obtener_fuentes_activas()
        
        # Crear carpetas si no existen
        os.makedirs(cfg.CARPETA_DATOS, exist_ok=True)
        os.makedirs(cfg.CARPETA_LOGS, exist_ok=True)
        
        if cfg.MODO_VERBOSE:
            logger.info("✅ Recolector de noticias inicializado")
            logger.info(f"📰 Fuentes activas: {len(self.fuentes_activas)}")
    
    
    def _obtener_fuentes_activas(self) -> Dict[str, str]:
        """Obtiene las fuentes activas según configuración"""
        fuentes = {}
        
        if cfg.USAR_GOOGLE_NEWS:
            fuentes['Google News'] = cfg.URLS['google_news']
        
        if cfg.USAR_INVESTING:
            fuentes['Investing.com'] = cfg.URLS['investing']
        
        if cfg.USAR_FXSTREET:
            fuentes['FXStreet'] = cfg.URLS['fxstreet']
        
        if cfg.USAR_FOREXLIVE:
            fuentes['ForexLive'] = cfg.URLS['forexlive']
        
        return fuentes
    
    
    def _es_relevante_eurusd(self, texto: str) -> bool:
        """
        Determina si una noticia es relevante para EUR/USD
        
        Args:
            texto: Título + descripción de la noticia
        
        Returns:
            True si es relevante, False si no
        """
        if not cfg.FILTRAR_RELEVANCIA:
            return True
        
        texto_lower = texto.lower()
        
        # Contar coincidencias con keywords
        coincidencias = 0
        total_keywords = len(cfg.KEYWORDS_EURUSD) + len(cfg.KEYWORDS_EVENTOS_IMPORTANTES)
        
        for keyword in cfg.KEYWORDS_EURUSD:
            if keyword.lower() in texto_lower:
                coincidencias += 1
        
        for keyword in cfg.KEYWORDS_EVENTOS_IMPORTANTES:
            if keyword.lower() in texto_lower:
                coincidencias += 1.5  # Eventos importantes tienen más peso
        
        # Calcular relevancia
        relevancia = coincidencias / total_keywords
        
        return relevancia >= cfg.RELEVANCIA_MINIMA
    
    
    def _obtener_noticias_google(self) -> List[Dict]:
        """Obtiene noticias de Google News"""
        noticias = []
        
        try:
            # Construir query para EUR/USD
            query = "EUR+USD+OR+EURUSD+OR+euro+dollar"
            url = f"{cfg.URLS['google_news']}/search?q={query}&hl=en-US&gl=US&ceid=US:en"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item', limit=cfg.NOTICIAS_POR_FUENTE)
            
            for item in items:
                try:
                    titulo = item.title.text if item.title else ""
                    descripcion = item.description.text if item.description else ""
                    link = item.link.text if item.link else ""
                    
                    # Obtener fecha
                    fecha_str = item.pubDate.text if item.pubDate else ""
                    fecha = pd.to_datetime(fecha_str, utc=True) if fecha_str else pd.Timestamp.now(tz='UTC')
                    
                    # Verificar relevancia
                    texto_completo = f"{titulo} {descripcion}"
                    if self._es_relevante_eurusd(texto_completo):
                        noticias.append({
                            'fuente': 'Google News',
                            'titulo': titulo,
                            'descripcion': descripcion,
                            'link': link,
                            'fecha': fecha,
                            'texto_completo': texto_completo
                        })
                
                except Exception as e:
                    logger.warning(f"Error procesando noticia de Google News: {e}")
                    continue
            
            logger.info(f"✅ Google News: {len(noticias)} noticias relevantes")
        
        except Exception as e:
            logger.error(f"❌ Error obteniendo noticias de Google News: {e}")
        
        return noticias
    
    
    def _obtener_noticias_investing(self) -> List[Dict]:
        """Obtiene noticias de Investing.com"""
        noticias = []
        
        try:
            response = requests.get(cfg.URLS['investing'], timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item', limit=cfg.NOTICIAS_POR_FUENTE * 2)  # Obtener más porque filtraremos
            
            for item in items:
                try:
                    titulo = item.title.text if item.title else ""
                    descripcion = item.description.text if item.description else ""
                    link = item.link.text if item.link else ""
                    
                    # Obtener fecha
                    fecha_str = item.pubDate.text if item.pubDate else ""
                    fecha = pd.to_datetime(fecha_str, utc=True) if fecha_str else pd.Timestamp.now(tz='UTC')
                    
                    # Verificar relevancia
                    texto_completo = f"{titulo} {descripcion}"
                    if self._es_relevante_eurusd(texto_completo):
                        noticias.append({
                            'fuente': 'Investing.com',
                            'titulo': titulo,
                            'descripcion': descripcion,
                            'link': link,
                            'fecha': fecha,
                            'texto_completo': texto_completo
                        })
                        
                        if len(noticias) >= cfg.NOTICIAS_POR_FUENTE:
                            break
                
                except Exception as e:
                    logger.warning(f"Error procesando noticia de Investing: {e}")
                    continue
            
            logger.info(f"✅ Investing.com: {len(noticias)} noticias relevantes")
        
        except Exception as e:
            logger.error(f"❌ Error obteniendo noticias de Investing: {e}")
        
        return noticias
    
    
    def _obtener_noticias_fxstreet(self) -> List[Dict]:
        """Obtiene noticias de FXStreet"""
        noticias = []
        
        try:
            response = requests.get(cfg.URLS['fxstreet'], timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item', limit=cfg.NOTICIAS_POR_FUENTE * 2)
            
            for item in items:
                try:
                    titulo = item.title.text if item.title else ""
                    descripcion = item.description.text if item.description else ""
                    link = item.link.text if item.link else ""
                    
                    # Obtener fecha
                    fecha_str = item.pubDate.text if item.pubDate else ""
                    fecha = pd.to_datetime(fecha_str, utc=True) if fecha_str else pd.Timestamp.now(tz='UTC')
                    
                    # Verificar relevancia
                    texto_completo = f"{titulo} {descripcion}"
                    if self._es_relevante_eurusd(texto_completo):
                        noticias.append({
                            'fuente': 'FXStreet',
                            'titulo': titulo,
                            'descripcion': descripcion,
                            'link': link,
                            'fecha': fecha,
                            'texto_completo': texto_completo
                        })
                        
                        if len(noticias) >= cfg.NOTICIAS_POR_FUENTE:
                            break
                
                except Exception as e:
                    logger.warning(f"Error procesando noticia de FXStreet: {e}")
                    continue
            
            logger.info(f"✅ FXStreet: {len(noticias)} noticias relevantes")
        
        except Exception as e:
            logger.error(f"❌ Error obteniendo noticias de FXStreet: {e}")
        
        return noticias
    
    
    def _obtener_noticias_forexlive(self) -> List[Dict]:
        """Obtiene noticias de ForexLive"""
        noticias = []
        
        try:
            response = requests.get(cfg.URLS['forexlive'], timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item', limit=cfg.NOTICIAS_POR_FUENTE * 2)
            
            for item in items:
                try:
                    titulo = item.title.text if item.title else ""
                    descripcion = item.description.text if item.description else ""
                    link = item.link.text if item.link else ""
                    
                    # Obtener fecha
                    fecha_str = item.pubDate.text if item.pubDate else ""
                    fecha = pd.to_datetime(fecha_str, utc=True) if fecha_str else pd.Timestamp.now(tz='UTC')
                    
                    # Verificar relevancia
                    texto_completo = f"{titulo} {descripcion}"
                    if self._es_relevante_eurusd(texto_completo):
                        noticias.append({
                            'fuente': 'ForexLive',
                            'titulo': titulo,
                            'descripcion': descripcion,
                            'link': link,
                            'fecha': fecha,
                            'texto_completo': texto_completo
                        })
                        
                        if len(noticias) >= cfg.NOTICIAS_POR_FUENTE:
                            break
                
                except Exception as e:
                    logger.warning(f"Error procesando noticia de ForexLive: {e}")
                    continue
            
            logger.info(f"✅ ForexLive: {len(noticias)} noticias relevantes")
        
        except Exception as e:
            logger.error(f"❌ Error obteniendo noticias de ForexLive: {e}")
        
        return noticias
    
    
    def _deduplicar_noticias(self, noticias: List[Dict]) -> List[Dict]:
        """
        Elimina noticias duplicadas basándose en el título
        
        Args:
            noticias: Lista de noticias
        
        Returns:
            Lista de noticias sin duplicados
        """
        titulos_vistos = set()
        noticias_unicas = []
        
        for noticia in noticias:
            # Normalizar título
            titulo_norm = re.sub(r'\s+', ' ', noticia['titulo'].lower().strip())
            
            if titulo_norm not in titulos_vistos:
                titulos_vistos.add(titulo_norm)
                noticias_unicas.append(noticia)
        
        duplicados = len(noticias) - len(noticias_unicas)
        if duplicados > 0:
            logger.info(f"🔄 Eliminados {duplicados} duplicados")
        
        return noticias_unicas
    
    
    def recolectar_noticias(self) -> pd.DataFrame:
        """
        Recolecta noticias de todas las fuentes activas
        
        Returns:
            DataFrame con las noticias recolectadas
        """
        logger.info("\n" + "="*70)
        logger.info("📰 INICIANDO RECOLECCIÓN DE NOTICIAS")
        logger.info("="*70)
        
        todas_noticias = []
        
        # Obtener de cada fuente
        if cfg.USAR_GOOGLE_NEWS:
            todas_noticias.extend(self._obtener_noticias_google())
            time.sleep(1)  # Pausa entre fuentes
        
        if cfg.USAR_INVESTING:
            todas_noticias.extend(self._obtener_noticias_investing())
            time.sleep(1)
        
        if cfg.USAR_FXSTREET:
            todas_noticias.extend(self._obtener_noticias_fxstreet())
            time.sleep(1)
        
        if cfg.USAR_FOREXLIVE:
            todas_noticias.extend(self._obtener_noticias_forexlive())
        
        # Deduplicar
        todas_noticias = self._deduplicar_noticias(todas_noticias)
        
        # Limitar cantidad total
        if len(todas_noticias) > cfg.MAX_NOTICIAS_TOTALES:
            # Ordenar por fecha (más recientes primero)
            todas_noticias.sort(key=lambda x: x['fecha'], reverse=True)
            todas_noticias = todas_noticias[:cfg.MAX_NOTICIAS_TOTALES]
            logger.info(f"⚠️ Limitado a {cfg.MAX_NOTICIAS_TOTALES} noticias más recientes")
        
        # Convertir a DataFrame
        if todas_noticias:
            df = pd.DataFrame(todas_noticias)
            df = df.sort_values('fecha', ascending=False).reset_index(drop=True)
            
            logger.info(f"\n✅ RECOLECCIÓN COMPLETADA: {len(df)} noticias únicas")
            logger.info("="*70 + "\n")
            
            # Guardar noticias raw
            if cfg.GUARDAR_HISTORICO:
                self._guardar_noticias_raw(df)
            
            return df
        else:
            logger.warning("⚠️ No se recolectaron noticias")
            return pd.DataFrame()
    
    
    def _guardar_noticias_raw(self, df: pd.DataFrame):
        """Guarda las noticias sin procesar"""
        try:
            # Agregar timestamp de recolección
            df['timestamp_recoleccion'] = pd.Timestamp.now(tz='UTC')
            
            # Guardar
            df.to_csv(cfg.ARCHIVO_NOTICIAS_RAW, index=False)
            logger.info(f"💾 Noticias guardadas en {cfg.ARCHIVO_NOTICIAS_RAW}")
        
        except Exception as e:
            logger.error(f"❌ Error guardando noticias: {e}")
    
    
    def obtener_noticias_recientes(self, horas: int = 24) -> pd.DataFrame:
        """
        Obtiene solo las noticias de las últimas X horas
        
        Args:
            horas: Cantidad de horas hacia atrás
        
        Returns:
            DataFrame con noticias recientes
        """
        df = self.recolectar_noticias()
        
        if df.empty:
            return df
        
        # Filtrar por fecha
        fecha_limite = pd.Timestamp.now(tz='UTC') - timedelta(hours=horas)
        df_recientes = df[df['fecha'] >= fecha_limite].copy()
        
        logger.info(f"📅 Noticias últimas {horas} horas: {len(df_recientes)}")
        
        return df_recientes
    
    
    def mostrar_resumen(self, df: pd.DataFrame):
        """Muestra un resumen de las noticias recolectadas"""
        if df.empty:
            print("❌ No hay noticias para mostrar")
            return
        
        print("\n" + "="*70)
        print("📊 RESUMEN DE NOTICIAS RECOLECTADAS")
        print("="*70)
        
        # Por fuente
        print("\n📰 Por fuente:")
        for fuente, count in df['fuente'].value_counts().items():
            print(f"   • {fuente}: {count} noticias")
        
        # Noticias más recientes
        print(f"\n⏰ Noticia más reciente: {df.iloc[0]['fecha']}")
        print(f"⏰ Noticia más antigua: {df.iloc[-1]['fecha']}")
        
        # Ejemplos
        print("\n📄 Últimas 5 noticias:")
        for i, row in df.head(5).iterrows():
            print(f"\n   [{row['fuente']}] {row['fecha']}")
            print(f"   {row['titulo'][:100]}...")
        
        print("\n" + "="*70 + "\n")


# ═══════════════════════════════════════════════════════════════
# 🧪 MODO DE PRUEBA
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 MODO DE PRUEBA - RECOLECTOR DE NOTICIAS")
    print("="*70 + "\n")
    
    # Crear recolector
    recolector = RecolectorNoticias()
    
    # Recolectar noticias
    df_noticias = recolector.recolectar_noticias()
    
    # Mostrar resumen
    recolector.mostrar_resumen(df_noticias)
    
    print("✅ Prueba completada")
