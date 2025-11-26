"""
╔══════════════════════════════════════════════════════════════════╗
║   ENTRENAR SISTEMA DE RECOMENDACIÓN KNN                         ║
║   Prepara el sistema KNN con datos históricos                    ║
╚══════════════════════════════════════════════════════════════════╝

Este script:
1. Carga datos históricos (con oro y sentimiento si están disponibles)
2. Crea features técnicas
3. Entrena el sistema KNN
4. Evalúa su rendimiento
5. Guarda el modelo entrenado

Ejecutar DESPUÉS de extraer_datos.py y ANTES de prediccion_en_vivo.py
"""

import pandas as pd
import numpy as np
import os
import config
import sistema_knn
from datetime import datetime


def cargar_datos():
    """Carga los datos más completos disponibles"""
    print("\n" + "="*70)
    print("📂 CARGANDO DATOS HISTÓRICOS")
    print("="*70)
    
    # Prioridad 1: Datos con oro (más completo)
    if os.path.exists("datos/eurusd_con_oro.csv"):
        df = pd.read_csv("datos/eurusd_con_oro.csv")
        print(f"✅ Cargados {len(df)} registros CON ORO")
        tipo = "oro"
    # Prioridad 2: Datos con sentimiento
    elif os.path.exists("datos/eurusd_con_sentimiento.csv"):
        df = pd.read_csv("datos/eurusd_con_sentimiento.csv")
        print(f"✅ Cargados {len(df)} registros CON SENTIMIENTO")
        tipo = "sentimiento"
    # Prioridad 3: Datos básicos
    elif os.path.exists("datos/eurusd_datos.csv"):
        df = pd.read_csv("datos/eurusd_datos.csv")
        print(f"✅ Cargados {len(df)} registros BÁSICOS")
        tipo = "basico"
    else:
        print("❌ No hay datos disponibles")
        print("👉 Primero ejecuta: python extraer_datos.py")
        return None, None
    
    return df, tipo


def crear_features(df):
    """Crea features técnicas si no existen"""
    print("\n🔧 VERIFICANDO FEATURES...")
    
    features_necesarias = ['MA_10', 'MA_30', 'MA_50', 'RSI', 'Volatility', 
                          'HL_Range', 'Price_Change', 'Volume_MA']
    
    features_faltantes = [f for f in features_necesarias if f not in df.columns]
    
    if not features_faltantes:
        print("✅ Todas las features técnicas ya existen")
        return df
    
    print(f"🔨 Creando {len(features_faltantes)} features faltantes...")
    
    # Medias móviles
    if 'MA_10' not in df.columns:
        df['MA_10'] = df['close'].rolling(window=10).mean()
    if 'MA_30' not in df.columns:
        df['MA_30'] = df['close'].rolling(window=30).mean()
    if 'MA_50' not in df.columns:
        df['MA_50'] = df['close'].rolling(window=50).mean()
    
    # RSI
    if 'RSI' not in df.columns:
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
    
    # Volatilidad
    if 'Volatility' not in df.columns:
        df['Volatility'] = df['close'].rolling(window=20).std()
    
    # Rango Alto-Bajo
    if 'HL_Range' not in df.columns:
        df['HL_Range'] = df['high'] - df['low']
    
    # Cambio porcentual
    if 'Price_Change' not in df.columns:
        df['Price_Change'] = df['close'].pct_change()
    
    # Volumen medio
    if 'Volume_MA' not in df.columns:
        df['Volume_MA'] = df['tick_volume'].rolling(window=20).mean()
    
    # Eliminar NaN
    df = df.dropna()
    
    print(f"✅ Features creadas. Registros válidos: {len(df)}")
    
    return df


def main():
    """Función principal"""
    print("\n╔" + "═"*68 + "╗")
    print("║" + " "*15 + "ENTRENAR SISTEMA KNN" + " "*33 + "║")
    print("╚" + "═"*68 + "╝")
    
    print(f"\n📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Mostrar configuración
    print("\n⚙️  CONFIGURACIÓN:")
    print(f"   • K Vecinos: {config.K_VECINOS}")
    print(f"   • Horizonte: {config.HORIZONTE_KNN} velas")
    print(f"   • Timeframe: {config.TIMEFRAME}")
    
    # 1. Cargar datos
    df, tipo_datos = cargar_datos()
    if df is None:
        return
    
    # 2. Crear features
    df = crear_features(df)
    
    # 3. Inicializar sistema KNN
    print("\n" + "="*70)
    print("🎯 INICIALIZANDO SISTEMA KNN")
    print("="*70)
    
    sistema = sistema_knn.SistemaRecomendacionKNN(
        k_vecinos=config.K_VECINOS,
        min_datos=500
    )
    
    # 4. Preparar datos históricos
    print("\n📊 PREPARANDO DATOS HISTÓRICOS...")
    
    if not sistema.preparar_datos_historicos(df, horizonte_prediccion=config.HORIZONTE_KNN):
        print("\n❌ Error al preparar datos")
        return
    
    # 5. Guardar modelo
    print("\n" + "="*70)
    print("💾 GUARDANDO SISTEMA KNN")
    print("="*70)
    sistema.guardar_modelo("modelos/sistema_knn.pkl")
    
    # 6. Evaluar rendimiento
    print("\n" + "="*70)
    print("📈 EVALUANDO RENDIMIENTO")
    print("="*70)
    
    metricas = sistema.evaluar_rendimiento(ventana_test=200)
    
    # 7. Probar una recomendación de ejemplo
    print("\n" + "="*70)
    print("🔮 EJEMPLO DE RECOMENDACIÓN")
    print("="*70)
    
    recomendacion = sistema.obtener_recomendacion(df, explicar=True)
    
    if recomendacion:
        sistema.mostrar_recomendacion(recomendacion)
    
    # Resumen final
    print("\n" + "╔" + "═"*68 + "╗")
    print("║" + " "*20 + "ENTRENAMIENTO COMPLETADO" + " "*24 + "║")
    print("╚" + "═"*68 + "╝")
    
    print("\n📊 RESUMEN:")
    print(f"   • Datos utilizados: {tipo_datos.upper()}")
    print(f"   • Patrones históricos: {sistema.estadisticas['total_patrones']}")
    print(f"   • Features: {len(sistema.features_usadas)}")
    print(f"   • Accuracy en test: {metricas['accuracy']:.2f}%")
    print(f"   • Ganancia simulada: {metricas['ganancia_acumulada']:.3f}%")
    
    print("\n✅ SISTEMA KNN LISTO PARA USAR")
    print("\n📝 PRÓXIMOS PASOS:")
    print("   1. Ejecuta: python prediccion_en_vivo.py")
    print("      → El sistema ahora usará LSTM + KNN combinados")
    print("   2. Ejecuta: python generar_señales_iqoption.py")
    print("      → Para generar señales mejoradas con KNN")
    
    print("\n💡 NOTAS:")
    print("   • El sistema KNN se actualiza automáticamente con nuevos datos")
    print("   • Re-entrena el KNN semanalmente para mejores resultados")
    print("   • Combina análisis técnico + fundamental + sentimiento")
    
    # Guardar reporte
    guardar_reporte(sistema, metricas, tipo_datos)


def guardar_reporte(sistema, metricas, tipo_datos):
    """Guarda un reporte del entrenamiento"""
    os.makedirs("registros", exist_ok=True)
    
    reporte = f"""
╔══════════════════════════════════════════════════════════════════╗
║           REPORTE DE ENTRENAMIENTO - SISTEMA KNN                 ║
╚══════════════════════════════════════════════════════════════════╝

Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

CONFIGURACIÓN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• K Vecinos:        {config.K_VECINOS}
• Horizonte:        {config.HORIZONTE_KNN} velas
• Timeframe:        {config.TIMEFRAME}
• Tipo de datos:    {tipo_datos.upper()}

DATOS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Patrones totales:     {sistema.estadisticas['total_patrones']}
• Features utilizadas:  {len(sistema.features_usadas)}
• Patrones COMPRA:      {sistema.estadisticas['compras']} ({sistema.estadisticas['pct_compras']:.1f}%)
• Patrones VENTA:       {sistema.estadisticas['ventas']} ({sistema.estadisticas['pct_ventas']:.1f}%)
• Patrones ESPERA:      {sistema.estadisticas['esperas']} ({sistema.estadisticas['pct_esperas']:.1f}%)

RENDIMIENTO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Accuracy:             {metricas['accuracy']:.2f}%
• Predicciones correctas: {metricas['predicciones_correctas']} / {metricas['total_predicciones']}
• Ganancia acumulada:   {metricas['ganancia_acumulada']:.3f}%
• Retorno medio COMPRA: {sistema.estadisticas['retorno_medio_compras']*100:.3f}%
• Retorno medio VENTA:  {sistema.estadisticas['retorno_medio_ventas']*100:.3f}%

FEATURES UTILIZADAS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{chr(10).join(f"  {i+1:2d}. {feat}" for i, feat in enumerate(sistema.features_usadas))}

╔══════════════════════════════════════════════════════════════════╗
║                     ENTRENAMIENTO EXITOSO                        ║
╚══════════════════════════════════════════════════════════════════╝
"""
    
    filename = f"registros/reporte_knn_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(reporte)
    
    print(f"\n📄 Reporte guardado en: {filename}")


if __name__ == "__main__":
    main()
