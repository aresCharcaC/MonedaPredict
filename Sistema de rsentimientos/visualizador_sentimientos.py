"""
╔══════════════════════════════════════════════════════════════════╗
║      VISUALIZADOR DE RESULTADOS - SISTEMA SENTIMIENTOS           ║
╚══════════════════════════════════════════════════════════════════╝

Módulo para visualizar resultados y generar reportes del sistema
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import logging
import os
from typing import Optional

# Importar configuración
import config_sentimientos as cfg

# Configurar logging
logging.basicConfig(
    level=getattr(logging, cfg.NIVEL_LOG),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurar estilo de gráficos
try:
    plt.style.use(cfg.ESTILO_GRAFICOS)
except:
    plt.style.use('default')


class VisualizadorSentimientos:
    """
    Visualiza resultados del análisis de sentimientos
    """
    
    def __init__(self):
        """Inicializa el visualizador"""
        # Crear carpetas
        os.makedirs(cfg.CARPETA_REPORTES, exist_ok=True)
        
        if cfg.MODO_VERBOSE:
            logger.info("✅ Visualizador inicializado")
    
    
    def _cargar_datos(self) -> tuple:
        """
        Carga los datos de señales y noticias
        
        Returns:
            Tupla (df_señales, df_noticias)
        """
        df_señales = pd.DataFrame()
        df_noticias = pd.DataFrame()
        
        # Cargar señales
        if os.path.exists(cfg.ARCHIVO_SEÑALES):
            try:
                df_señales = pd.read_csv(cfg.ARCHIVO_SEÑALES)
                df_señales['timestamp'] = pd.to_datetime(df_señales['timestamp'], utc=True)
                logger.info(f"✅ Cargadas {len(df_señales)} señales")
            except Exception as e:
                logger.error(f"❌ Error cargando señales: {e}")
        
        # Cargar noticias analizadas
        if os.path.exists(cfg.ARCHIVO_NOTICIAS_ANALIZADAS):
            try:
                df_noticias = pd.read_csv(cfg.ARCHIVO_NOTICIAS_ANALIZADAS)
                df_noticias['fecha'] = pd.to_datetime(df_noticias['fecha'], utc=True)
                logger.info(f"✅ Cargadas {len(df_noticias)} noticias analizadas")
            except Exception as e:
                logger.error(f"❌ Error cargando noticias: {e}")
        
        return df_señales, df_noticias
    
    
    def graficar_evolucion_sentimiento(self, dias: int = 7):
        """
        Grafica la evolución del sentimiento en el tiempo
        
        Args:
            dias: Cantidad de días a visualizar
        """
        df_señales, _ = self._cargar_datos()
        
        if df_señales.empty:
            logger.warning("⚠️ No hay datos de señales para graficar")
            return
        
        # Filtrar por días
        fecha_limite = pd.Timestamp.now(tz='UTC') - timedelta(days=dias)
        df = df_señales[df_señales['timestamp'] >= fecha_limite].copy()
        
        if df.empty:
            logger.warning(f"⚠️ No hay datos de los últimos {dias} días")
            return
        
        # Crear figura
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=cfg.TAMAÑO_FIGURA, sharex=True)
        
        # Gráfico 1: Sentimiento General
        ax1.plot(df['timestamp'], df['sentimiento_general'], 
                marker='o', linewidth=2, markersize=4, label='Sentimiento')
        ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax1.fill_between(df['timestamp'], 0, df['sentimiento_general'],
                         where=(df['sentimiento_general'] >= 0),
                         color=cfg.COLOR_POSITIVO, alpha=0.3, label='Positivo')
        ax1.fill_between(df['timestamp'], 0, df['sentimiento_general'],
                         where=(df['sentimiento_general'] < 0),
                         color=cfg.COLOR_NEGATIVO, alpha=0.3, label='Negativo')
        ax1.set_ylabel('Sentimiento', fontsize=11, fontweight='bold')
        ax1.set_title(f'Evolución del Sentimiento EUR/USD - Últimos {dias} días', 
                     fontsize=14, fontweight='bold', pad=20)
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        
        # Gráfico 2: Confianza
        ax2.plot(df['timestamp'], df['confianza'], 
                marker='s', linewidth=2, markersize=4, color='orange', label='Confianza')
        ax2.axhline(y=cfg.CONFIANZA_MINIMA_COMPRA, color='red', 
                   linestyle='--', alpha=0.5, label=f'Umbral mínimo ({cfg.CONFIANZA_MINIMA_COMPRA}%)')
        ax2.fill_between(df['timestamp'], 0, df['confianza'],
                        alpha=0.3, color='orange')
        ax2.set_ylabel('Confianza (%)', fontsize=11, fontweight='bold')
        ax2.set_ylim(0, 100)
        ax2.legend(loc='best')
        ax2.grid(True, alpha=0.3)
        
        # Gráfico 3: Señales
        colores_señal = {
            'COMPRA': cfg.COLOR_POSITIVO,
            'VENTA': cfg.COLOR_NEGATIVO,
            'ESPERA': cfg.COLOR_NEUTRAL
        }
        
        # Convertir señales a valores numéricos
        señal_valores = df['señal'].map({'COMPRA': 1, 'VENTA': -1, 'ESPERA': 0})
        
        for señal, color in colores_señal.items():
            mask = df['señal'] == señal
            ax3.scatter(df.loc[mask, 'timestamp'], señal_valores[mask],
                       c=color, s=100, marker='o', label=señal, alpha=0.7)
        
        ax3.axhline(y=0, color='gray', linestyle='-', alpha=0.5)
        ax3.set_ylabel('Señal', fontsize=11, fontweight='bold')
        ax3.set_xlabel('Fecha', fontsize=11, fontweight='bold')
        ax3.set_yticks([-1, 0, 1])
        ax3.set_yticklabels(['VENTA', 'ESPERA', 'COMPRA'])
        ax3.legend(loc='best')
        ax3.grid(True, alpha=0.3)
        
        # Formatear eje X
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        
        # Guardar
        archivo = f"{cfg.CARPETA_REPORTES}/evolucion_sentimiento_{dias}d.png"
        plt.savefig(archivo, dpi=cfg.DPI, bbox_inches='tight')
        logger.info(f"💾 Gráfico guardado: {archivo}")
        
        plt.show()
    
    
    def graficar_distribucion_noticias(self, dias: int = 7):
        """
        Grafica la distribución de noticias por fuente y sentimiento
        
        Args:
            dias: Cantidad de días a visualizar
        """
        _, df_noticias = self._cargar_datos()
        
        if df_noticias.empty:
            logger.warning("⚠️ No hay datos de noticias para graficar")
            return
        
        # Filtrar por días
        fecha_limite = pd.Timestamp.now(tz='UTC') - timedelta(days=dias)
        df = df_noticias[df_noticias['fecha'] >= fecha_limite].copy()
        
        if df.empty:
            logger.warning(f"⚠️ No hay noticias de los últimos {dias} días")
            return
        
        # Crear figura
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Gráfico 1: Por fuente
        fuentes_count = df['fuente'].value_counts()
        ax1.pie(fuentes_count.values, labels=fuentes_count.index, autopct='%1.1f%%',
               startangle=90, colors=plt.cm.Set3.colors)
        ax1.set_title(f'Distribución por Fuente\n({len(df)} noticias)', 
                     fontsize=12, fontweight='bold')
        
        # Gráfico 2: Por dirección EUR
        direccion_count = df['direccion_eur'].value_counts()
        colores = [cfg.COLOR_POSITIVO if 'POSITIVO' in d else 
                   cfg.COLOR_NEGATIVO if 'NEGATIVO' in d else 
                   cfg.COLOR_NEUTRAL for d in direccion_count.index]
        
        ax2.pie(direccion_count.values, labels=direccion_count.index, autopct='%1.1f%%',
               startangle=90, colors=colores)
        ax2.set_title(f'Distribución por Sentimiento EUR\n({len(df)} noticias)', 
                     fontsize=12, fontweight='bold')
        
        plt.suptitle(f'Análisis de Noticias - Últimos {dias} días', 
                    fontsize=14, fontweight='bold', y=1.02)
        
        plt.tight_layout()
        
        # Guardar
        archivo = f"{cfg.CARPETA_REPORTES}/distribucion_noticias_{dias}d.png"
        plt.savefig(archivo, dpi=cfg.DPI, bbox_inches='tight')
        logger.info(f"💾 Gráfico guardado: {archivo}")
        
        plt.show()
    
    
    def generar_reporte_texto(self, dias: int = 7):
        """
        Genera un reporte en texto con estadísticas
        
        Args:
            dias: Cantidad de días a analizar
        """
        df_señales, df_noticias = self._cargar_datos()
        
        # Filtrar por días
        fecha_limite = pd.Timestamp.now(tz='UTC') - timedelta(days=dias)
        
        if not df_señales.empty:
            df_señales = df_señales[df_señales['timestamp'] >= fecha_limite]
        
        if not df_noticias.empty:
            df_noticias = df_noticias[df_noticias['fecha'] >= fecha_limite]
        
        # Generar reporte
        reporte = []
        reporte.append("═" * 70)
        reporte.append("📊 REPORTE DE ANÁLISIS DE SENTIMIENTOS EUR/USD")
        reporte.append("═" * 70)
        reporte.append(f"\n📅 Período: Últimos {dias} días")
        reporte.append(f"⏰ Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Estadísticas de señales
        if not df_señales.empty:
            reporte.append("\n\n" + "─" * 70)
            reporte.append("🎯 ESTADÍSTICAS DE SEÑALES")
            reporte.append("─" * 70)
            
            reporte.append(f"\nTotal señales generadas: {len(df_señales)}")
            
            # Distribución de señales
            for señal in ['COMPRA', 'VENTA', 'ESPERA']:
                count = len(df_señales[df_señales['señal'] == señal])
                pct = (count / len(df_señales)) * 100 if len(df_señales) > 0 else 0
                reporte.append(f"   {señal}: {count} ({pct:.1f}%)")
            
            # Confianza promedio
            conf_promedio = df_señales['confianza'].mean()
            reporte.append(f"\nConfianza promedio: {conf_promedio:.1f}%")
            
            # Sentimiento promedio
            sent_promedio = df_señales['sentimiento_general'].mean()
            reporte.append(f"Sentimiento promedio: {sent_promedio:.4f}")
            
            # Última señal
            ultima = df_señales.iloc[-1]
            reporte.append(f"\n📍 Última señal:")
            reporte.append(f"   Tipo:       {ultima['señal']}")
            reporte.append(f"   Confianza:  {ultima['confianza']:.1f}%")
            reporte.append(f"   Urgencia:   {ultima['urgencia']}")
            reporte.append(f"   Timestamp:  {ultima['timestamp']}")
        
        # Estadísticas de noticias
        if not df_noticias.empty:
            reporte.append("\n\n" + "─" * 70)
            reporte.append("📰 ESTADÍSTICAS DE NOTICIAS")
            reporte.append("─" * 70)
            
            reporte.append(f"\nTotal noticias analizadas: {len(df_noticias)}")
            
            # Por fuente
            reporte.append("\nDistribución por fuente:")
            for fuente, count in df_noticias['fuente'].value_counts().items():
                pct = (count / len(df_noticias)) * 100
                reporte.append(f"   {fuente}: {count} ({pct:.1f}%)")
            
            # Por sentimiento
            reporte.append("\nDistribución por sentimiento EUR:")
            for direccion, count in df_noticias['direccion_eur'].value_counts().items():
                pct = (count / len(df_noticias)) * 100
                reporte.append(f"   {direccion}: {count} ({pct:.1f}%)")
            
            # Top noticias por impacto
            reporte.append("\n🔝 Top 5 noticias por impacto:")
            top_noticias = df_noticias.nlargest(5, 'peso_final')
            
            for idx, row in top_noticias.iterrows():
                reporte.append(f"\n   [{row['fuente']}] {row['fecha'].strftime('%Y-%m-%d %H:%M')}")
                reporte.append(f"   {row['titulo'][:70]}...")
                reporte.append(f"   Sentimiento: {row['sentimiento_ajustado']:.3f} | " +
                             f"Peso: {row['peso_final']:.3f} | " +
                             f"Dirección: {row['direccion_eur']}")
        
        reporte.append("\n" + "═" * 70 + "\n")
        
        # Guardar reporte
        texto_reporte = "\n".join(reporte)
        
        archivo = f"{cfg.CARPETA_REPORTES}/reporte_{dias}d_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(texto_reporte)
        
        logger.info(f"💾 Reporte guardado: {archivo}")
        
        # Mostrar en consola
        print(texto_reporte)
    
    
    def dashboard_completo(self, dias: int = 7):
        """
        Genera un dashboard completo con todos los gráficos
        
        Args:
            dias: Cantidad de días a visualizar
        """
        logger.info("\n" + "═"*70)
        logger.info("📊 GENERANDO DASHBOARD COMPLETO")
        logger.info("═"*70 + "\n")
        
        # Generar gráficos
        self.graficar_evolucion_sentimiento(dias)
        self.graficar_distribucion_noticias(dias)
        
        # Generar reporte texto
        self.generar_reporte_texto(dias)
        
        logger.info("\n✅ Dashboard completado")


# ═══════════════════════════════════════════════════════════════
# 🎯 PUNTO DE ENTRADA
# ═══════════════════════════════════════════════════════════════

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Visualizador de Resultados - Sistema de Sentimientos',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--dias',
        type=int,
        default=7,
        help='Cantidad de días a visualizar (default: 7)'
    )
    
    parser.add_argument(
        '--tipo',
        choices=['evolucion', 'distribucion', 'reporte', 'todo'],
        default='todo',
        help='Tipo de visualización (default: todo)'
    )
    
    args = parser.parse_args()
    
    # Crear visualizador
    viz = VisualizadorSentimientos()
    
    # Generar visualizaciones
    if args.tipo == 'evolucion':
        viz.graficar_evolucion_sentimiento(args.dias)
    
    elif args.tipo == 'distribucion':
        viz.graficar_distribucion_noticias(args.dias)
    
    elif args.tipo == 'reporte':
        viz.generar_reporte_texto(args.dias)
    
    else:  # 'todo'
        viz.dashboard_completo(args.dias)


if __name__ == "__main__":
    main()
