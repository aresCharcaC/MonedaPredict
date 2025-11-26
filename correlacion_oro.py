"""
CORRELACIÓN EUR/USD CON ORO (XAU/USD)
======================================
Este módulo maneja la correlación del EUR/USD con el oro, que históricamente 
tienen una correlación positiva significativa.

El oro es un activo refugio que generalmente se correlaciona con el EUR,
especialmente en momentos de incertidumbre económica.
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import seaborn as sns


def calcular_correlacion(df_eurusd, df_oro, ventana=100):
    """
    Calcula la correlación entre EUR/USD y XAU/USD
    
    Parámetros:
    - df_eurusd: DataFrame con datos de EUR/USD
    - df_oro: DataFrame con datos de XAU/USD
    - ventana: ventana de tiempo para correlación móvil
    
    Retorna:
    - DataFrame con columnas de correlación
    """
    
    print(f"\n📊 Calculando correlación con ventana de {ventana} periodos...")
    
    # Asegurar que ambos DataFrames tienen la misma longitud y están alineados
    df_eurusd = df_eurusd.copy()
    df_oro = df_oro.copy()
    
    # Asegurar que tienen el mismo índice temporal
    df_eurusd['time'] = pd.to_datetime(df_eurusd['time'])
    df_oro['time'] = pd.to_datetime(df_oro['time'])
    
    # Merge por tiempo
    df_merged = pd.merge(
        df_eurusd[['time', 'close']],
        df_oro[['time', 'close']],
        on='time',
        suffixes=('_eur', '_oro')
    )
    
    # Calcular retornos
    df_merged['retorno_eur'] = df_merged['close_eur'].pct_change()
    df_merged['retorno_oro'] = df_merged['close_oro'].pct_change()
    
    # Correlación móvil
    correlaciones = []
    for i in range(len(df_merged)):
        if i < ventana:
            correlaciones.append(np.nan)
        else:
            ventana_eur = df_merged['retorno_eur'].iloc[i-ventana:i]
            ventana_oro = df_merged['retorno_oro'].iloc[i-ventana:i]
            
            # Eliminar NaN
            mask = ~(ventana_eur.isna() | ventana_oro.isna())
            ventana_eur_clean = ventana_eur[mask]
            ventana_oro_clean = ventana_oro[mask]
            
            if len(ventana_eur_clean) > 10:
                corr, _ = pearsonr(ventana_eur_clean, ventana_oro_clean)
                correlaciones.append(corr)
            else:
                correlaciones.append(np.nan)
    
    df_merged['correlacion'] = correlaciones
    
    # Correlación general
    mask = ~(df_merged['retorno_eur'].isna() | df_merged['retorno_oro'].isna())
    corr_general, p_value = pearsonr(
        df_merged['retorno_eur'][mask],
        df_merged['retorno_oro'][mask]
    )
    
    print(f"✅ Correlación general: {corr_general:.4f} (p-value: {p_value:.4f})")
    print(f"   {'Fuerte correlación positiva' if corr_general > 0.5 else 'Correlación moderada' if corr_general > 0.3 else 'Correlación débil'}")
    
    return df_merged, corr_general


def crear_features_oro(df_merged):
    """
    Crea features basadas en la relación EUR/USD - ORO
    
    Parámetros:
    - df_merged: DataFrame con datos combinados
    
    Retorna:
    - DataFrame con nuevas features
    """
    
    print("\n🔧 Creando features de correlación con oro...")
    
    df = df_merged.copy()
    
    # 1. Ratio EUR/USD vs ORO
    df['ratio_eur_oro'] = df['close_eur'] / df['close_oro']
    df['ratio_eur_oro_ma'] = df['ratio_eur_oro'].rolling(window=20).mean()
    df['ratio_eur_oro_std'] = df['ratio_eur_oro'].rolling(window=20).std()
    
    # 2. Desviación del ratio respecto a la media
    df['ratio_desviacion'] = (df['ratio_eur_oro'] - df['ratio_eur_oro_ma']) / df['ratio_eur_oro_std']
    
    # 3. Diferencia de retornos (divergencia)
    df['divergencia_retornos'] = df['retorno_eur'] - df['retorno_oro']
    df['divergencia_ma'] = df['divergencia_retornos'].rolling(window=10).mean()
    
    # 4. Tendencia del oro (puede influir en EUR)
    df['oro_ma_rapida'] = df['close_oro'].rolling(window=10).mean()
    df['oro_ma_lenta'] = df['close_oro'].rolling(window=30).mean()
    df['oro_tendencia'] = (df['oro_ma_rapida'] - df['oro_ma_lenta']) / df['oro_ma_lenta']
    
    # 5. Volatilidad relativa
    df['vol_eur'] = df['retorno_eur'].rolling(window=20).std()
    df['vol_oro'] = df['retorno_oro'].rolling(window=20).std()
    df['ratio_volatilidad'] = df['vol_eur'] / df['vol_oro']
    
    # 6. Correlación como feature
    df['correlacion_ma'] = df['correlacion'].rolling(window=20).mean()
    
    # 7. Cambio en correlación (indica cambios de régimen)
    df['correlacion_cambio'] = df['correlacion'].diff()
    
    # 8. Precio del oro normalizado
    df['oro_cambio_pct'] = df['close_oro'].pct_change()
    df['oro_momentum'] = df['close_oro'].pct_change(periods=5)
    
    print(f"✅ Features creadas:")
    print(f"   • ratio_eur_oro: Ratio de precios EUR/USD vs ORO")
    print(f"   • ratio_desviacion: Desviación del ratio")
    print(f"   • divergencia_retornos: Diferencia en retornos")
    print(f"   • oro_tendencia: Tendencia del oro")
    print(f"   • ratio_volatilidad: Volatilidad relativa")
    print(f"   • correlacion_ma: Media móvil de correlación")
    print(f"   • oro_momentum: Momentum del oro")
    
    return df


def integrar_oro_a_eurusd(df_eurusd, df_oro):
    """
    Integra las features de oro al DataFrame de EUR/USD
    
    Parámetros:
    - df_eurusd: DataFrame original de EUR/USD
    - df_oro: DataFrame de oro
    
    Retorna:
    - DataFrame de EUR/USD enriquecido con features de oro
    """
    
    print("\n🔗 Integrando datos de oro a EUR/USD...")
    
    # Calcular correlación
    df_merged, corr_general = calcular_correlacion(df_eurusd, df_oro)
    
    # Crear features
    df_merged = crear_features_oro(df_merged)
    
    # Preparar DataFrame final
    # Mantener todas las columnas de EUR/USD originales
    df_final = df_eurusd.copy()
    df_final['time'] = pd.to_datetime(df_final['time'])
    
    # Agregar features de oro
    oro_features = [
        'close_oro', 'ratio_eur_oro', 'ratio_desviacion',
        'divergencia_retornos', 'oro_tendencia', 'ratio_volatilidad',
        'correlacion', 'correlacion_ma', 'oro_momentum'
    ]
    
    for feature in oro_features:
        if feature in df_merged.columns:
            df_final = df_final.merge(
                df_merged[['time', feature]],
                on='time',
                how='left'
            )
    
    # Eliminar filas con NaN
    registros_antes = len(df_final)
    df_final = df_final.dropna()
    registros_despues = len(df_final)
    
    print(f"✅ Integración completada!")
    print(f"   Registros antes: {registros_antes}")
    print(f"   Registros después: {registros_despues}")
    print(f"   Registros eliminados: {registros_antes - registros_despues}")
    
    return df_final, corr_general


def visualizar_correlacion(df_merged, guardar=True):
    """
    Crea visualizaciones de la correlación EUR/USD - ORO
    
    Parámetros:
    - df_merged: DataFrame con datos combinados
    - guardar: Si guardar las imágenes
    """
    
    print("\n📊 Generando visualizaciones...")
    
    # Crear figura con subplots
    fig, axes = plt.subplots(3, 2, figsize=(16, 12))
    fig.suptitle('Análisis de Correlación EUR/USD vs ORO (XAU/USD)', 
                 fontsize=16, fontweight='bold', y=1.00)
    
    # 1. Precios normalizados
    ax = axes[0, 0]
    eur_norm = (df_merged['close_eur'] / df_merged['close_eur'].iloc[0]) * 100
    oro_norm = (df_merged['close_oro'] / df_merged['close_oro'].iloc[0]) * 100
    ax.plot(df_merged.index, eur_norm, label='EUR/USD', linewidth=2, color='blue')
    ax.plot(df_merged.index, oro_norm, label='XAU/USD (Oro)', linewidth=2, color='gold')
    ax.set_title('Precios Normalizados (Base 100)', fontweight='bold')
    ax.set_ylabel('Índice')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. Correlación móvil
    ax = axes[0, 1]
    ax.plot(df_merged.index, df_merged['correlacion'], linewidth=2, color='purple')
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    ax.axhline(y=0.5, color='green', linestyle='--', alpha=0.3, label='Corr. Fuerte')
    ax.axhline(y=-0.5, color='red', linestyle='--', alpha=0.3, label='Corr. Inversa')
    ax.set_title('Correlación Móvil (100 periodos)', fontweight='bold')
    ax.set_ylabel('Correlación')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 3. Scatter plot de retornos
    ax = axes[1, 0]
    mask = ~(df_merged['retorno_eur'].isna() | df_merged['retorno_oro'].isna())
    ax.scatter(df_merged['retorno_oro'][mask], df_merged['retorno_eur'][mask], 
               alpha=0.5, s=10, color='darkblue')
    
    # Línea de regresión
    z = np.polyfit(df_merged['retorno_oro'][mask], df_merged['retorno_eur'][mask], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df_merged['retorno_oro'][mask].min(), 
                        df_merged['retorno_oro'][mask].max(), 100)
    ax.plot(x_line, p(x_line), "r--", linewidth=2, label=f'Regresión: y={z[0]:.2f}x+{z[1]:.4f}')
    
    ax.set_title('Dispersión de Retornos', fontweight='bold')
    ax.set_xlabel('Retorno ORO (%)')
    ax.set_ylabel('Retorno EUR/USD (%)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 4. Ratio EUR/ORO
    ax = axes[1, 1]
    ax.plot(df_merged.index, df_merged['ratio_eur_oro'], linewidth=1.5, color='teal')
    if 'ratio_eur_oro_ma' in df_merged.columns:
        ax.plot(df_merged.index, df_merged['ratio_eur_oro_ma'], 
                linewidth=2, color='orange', label='MA 20')
    ax.set_title('Ratio EUR/USD vs ORO', fontweight='bold')
    ax.set_ylabel('Ratio')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 5. Divergencia de retornos
    ax = axes[2, 0]
    if 'divergencia_retornos' in df_merged.columns:
        ax.plot(df_merged.index, df_merged['divergencia_retornos'], 
                linewidth=1, color='green', alpha=0.7)
        if 'divergencia_ma' in df_merged.columns:
            ax.plot(df_merged.index, df_merged['divergencia_ma'], 
                    linewidth=2, color='darkgreen', label='MA 10')
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax.set_title('Divergencia de Retornos (EUR - ORO)', fontweight='bold')
        ax.set_ylabel('Divergencia')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # 6. Distribución de correlación
    ax = axes[2, 1]
    if 'correlacion' in df_merged.columns:
        hist_data = df_merged['correlacion'].dropna()
        
        if len(hist_data) > 5:  # Solo crear histograma si hay suficientes datos
            # Calcular bins de forma segura
            n_unique = len(np.unique(hist_data))
            bins = min(20, max(5, n_unique // 2))  # Entre 5 y 20 bins
            
            try:
                ax.hist(hist_data, bins=bins, color='skyblue', edgecolor='black', alpha=0.7)
                ax.axvline(x=hist_data.mean(), color='red', linestyle='--', 
                           linewidth=2, label=f'Media: {hist_data.mean():.3f}')
                ax.legend()
            except ValueError:
                # Si aún falla, usar 'auto' para que numpy decida
                ax.hist(hist_data, bins='auto', color='skyblue', edgecolor='black', alpha=0.7)
                ax.axvline(x=hist_data.mean(), color='red', linestyle='--', 
                           linewidth=2, label=f'Media: {hist_data.mean():.3f}')
                ax.legend()
            
            ax.set_title('Distribución de Correlación', fontweight='bold')
            ax.set_xlabel('Correlación')
            ax.set_ylabel('Frecuencia')
            ax.grid(True, alpha=0.3)
        else:
            ax.text(0.5, 0.5, 'Datos insuficientes\npara histograma', 
                   ha='center', va='center', transform=ax.transAxes,
                   fontsize=12)
            ax.set_title('Distribución de Correlación', fontweight='bold')
    
    plt.tight_layout()
    
    if guardar:
        import os
        os.makedirs('datos', exist_ok=True)
        plt.savefig('datos/correlacion_oro.png', dpi=300, bbox_inches='tight')
        print("✅ Gráfico guardado: datos/correlacion_oro.png")
    
    plt.close()


def obtener_features_oro():
    """
    Retorna la lista de features de oro que se usarán en el modelo
    """
    return [
        'close_oro',
        'ratio_eur_oro',
        'ratio_desviacion',
        'divergencia_retornos',
        'oro_tendencia',
        'ratio_volatilidad',
        'correlacion',
        'correlacion_ma',
        'oro_momentum'
    ]


def resumen_correlacion(df_merged):
    """
    Muestra un resumen estadístico de la correlación
    """
    
    print("\n" + "="*70)
    print("📊 RESUMEN DE CORRELACIÓN EUR/USD - ORO")
    print("="*70)
    
    if 'correlacion' in df_merged.columns:
        corr_data = df_merged['correlacion'].dropna()
        
        print(f"Correlación promedio:     {corr_data.mean():.4f}")
        print(f"Correlación mediana:      {corr_data.median():.4f}")
        print(f"Correlación mínima:       {corr_data.min():.4f}")
        print(f"Correlación máxima:       {corr_data.max():.4f}")
        print(f"Desviación estándar:      {corr_data.std():.4f}")
        
        # Porcentaje de tiempo en correlación positiva
        pct_positivo = (corr_data > 0).sum() / len(corr_data) * 100
        pct_fuerte = (corr_data > 0.5).sum() / len(corr_data) * 100
        
        print(f"\nPorcentaje correlación positiva: {pct_positivo:.1f}%")
        print(f"Porcentaje correlación fuerte:   {pct_fuerte:.1f}%")
        
        # Interpretación
        print("\n💡 INTERPRETACIÓN:")
        if corr_data.mean() > 0.5:
            print("   ✅ Fuerte correlación positiva entre EUR/USD y ORO")
            print("   → Cuando el oro sube, EUR/USD tiende a subir")
        elif corr_data.mean() > 0.3:
            print("   📊 Correlación positiva moderada")
            print("   → Existe relación positiva pero con variabilidad")
        elif corr_data.mean() > 0:
            print("   📉 Correlación positiva débil")
            print("   → Relación limitada entre ambos activos")
        else:
            print("   ⚠️ Correlación negativa o nula")
            print("   → Los activos se mueven independientemente")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🥇 MÓDULO DE CORRELACIÓN CON ORO")
    print("="*70)
    print("\n💡 Este módulo se usa automáticamente en:")
    print("   • extraer_datos.py (descarga datos de oro)")
    print("   • entrenar_modelo.py (integra features de oro)")
    print("   • prediccion_en_vivo.py (usa oro en predicciones)")
    print("\n👉 No necesitas ejecutar este archivo directamente")
    print("="*70 + "\n")
