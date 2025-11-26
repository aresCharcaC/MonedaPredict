"""
EJEMPLO: ANÁLISIS DE CORRELACIÓN EUR/USD - ORO
==============================================
Este script demuestra cómo usar el módulo de correlación con oro
"""

import pandas as pd
import os
import correlacion_oro

def ejemplo_analisis_correlacion():
    """
    Ejemplo completo de análisis de correlación
    """
    
    print("="*70)
    print("🥇 EJEMPLO: ANÁLISIS DE CORRELACIÓN EUR/USD - ORO")
    print("="*70)
    
    # 1. Verificar que existen los datos
    print("\n📊 PASO 1: Verificando datos...")
    
    if not os.path.exists('datos/eurusd_datos.csv'):
        print("❌ Error: No se encuentran datos de EUR/USD")
        print("👉 Ejecuta primero: python extraer_datos.py")
        return
    
    if not os.path.exists('datos/oro_datos.csv'):
        print("❌ Error: No se encuentran datos de ORO")
        print("👉 Ejecuta primero: python extraer_datos.py")
        return
    
    print("✅ Datos encontrados!")
    
    # 2. Cargar datos
    print("\n📊 PASO 2: Cargando datos...")
    df_eurusd = pd.read_csv('datos/eurusd_datos.csv')
    df_oro = pd.read_csv('datos/oro_datos.csv')
    
    print(f"   EUR/USD: {len(df_eurusd)} registros")
    print(f"   ORO:     {len(df_oro)} registros")
    
    # 3. Calcular correlación
    print("\n📊 PASO 3: Calculando correlación...")
    df_merged, corr_general = correlacion_oro.calcular_correlacion(
        df_eurusd, 
        df_oro, 
        ventana=100
    )
    
    # 4. Mostrar resumen estadístico
    print("\n📊 PASO 4: Análisis estadístico...")
    correlacion_oro.resumen_correlacion(df_merged)
    
    # 5. Crear features
    print("\n📊 PASO 5: Creando features de oro...")
    df_features = correlacion_oro.crear_features_oro(df_merged)
    
    print(f"\n📋 Features creadas: {len(correlacion_oro.obtener_features_oro())}")
    for i, feat in enumerate(correlacion_oro.obtener_features_oro(), 1):
        print(f"   {i}. {feat}")
    
    # 6. Visualizar
    print("\n📊 PASO 6: Generando visualizaciones...")
    correlacion_oro.visualizar_correlacion(df_merged, guardar=True)
    
    # 7. Integrar todo
    print("\n📊 PASO 7: Integrando datos completos...")
    df_final, _ = correlacion_oro.integrar_oro_a_eurusd(df_eurusd, df_oro)
    
    print(f"\n✅ DataFrame final: {len(df_final)} registros")
    print(f"   Columnas totales: {len(df_final.columns)}")
    
    # 8. Guardar ejemplo
    print("\n📊 PASO 8: Guardando datos de ejemplo...")
    df_final.to_csv('datos/ejemplo_correlacion.csv', index=False)
    print("✅ Guardado en: datos/ejemplo_correlacion.csv")
    
    # 9. Mostrar muestra de datos
    print("\n📊 PASO 9: Vista previa de datos con oro...")
    print("\nÚltimas 5 filas con features de oro:")
    
    oro_cols = ['time', 'close'] + correlacion_oro.obtener_features_oro()
    oro_cols = [col for col in oro_cols if col in df_final.columns]
    
    print(df_final[oro_cols].tail().to_string())
    
    # 10. Análisis de ejemplo
    print("\n" + "="*70)
    print("💡 ANÁLISIS DE EJEMPLO")
    print("="*70)
    
    ultima_fila = df_final.iloc[-1]
    
    print(f"\n📅 Última fecha: {ultima_fila['time']}")
    print(f"💵 EUR/USD: {ultima_fila['close']:.5f}")
    
    if 'close_oro' in df_final.columns:
        print(f"🥇 Oro: {ultima_fila['close_oro']:.2f}")
    
    if 'correlacion' in df_final.columns:
        corr_actual = ultima_fila['correlacion']
        print(f"📊 Correlación actual: {corr_actual:.4f}")
        
        if corr_actual > 0.7:
            print("   → 🔥 Correlación MUY FUERTE positiva")
            print("   → Si oro sube, EUR/USD muy probablemente suba")
        elif corr_actual > 0.5:
            print("   → ✅ Correlación FUERTE positiva")
            print("   → Movimientos del oro son buenos indicadores")
        elif corr_actual > 0.3:
            print("   → 📊 Correlación MODERADA positiva")
            print("   → Oro tiene influencia pero no definitiva")
        elif corr_actual > 0:
            print("   → 📉 Correlación DÉBIL positiva")
            print("   → Poca relación entre ambos activos")
        else:
            print("   → ⚠️ Correlación NEGATIVA o NULA")
            print("   → Los activos se mueven independientemente")
    
    if 'oro_tendencia' in df_final.columns:
        tendencia_oro = ultima_fila['oro_tendencia']
        print(f"\n📈 Tendencia del oro: {tendencia_oro:.6f}")
        
        if tendencia_oro > 0.001:
            print("   → 🟢 Oro en tendencia ALCISTA")
        elif tendencia_oro < -0.001:
            print("   → 🔴 Oro en tendencia BAJISTA")
        else:
            print("   → ⚪ Oro LATERAL")
    
    if 'ratio_desviacion' in df_final.columns:
        desviacion = ultima_fila['ratio_desviacion']
        print(f"\n📊 Desviación ratio EUR/ORO: {desviacion:.2f}")
        
        if abs(desviacion) > 2:
            print("   → ⚠️ EXTREMO: Posible reversión a la media")
        elif abs(desviacion) > 1:
            print("   → 📊 ELEVADO: Alejado de la media")
        else:
            print("   → ✅ NORMAL: Cerca de la media")
    
    print("\n" + "="*70)
    print("✅ ANÁLISIS COMPLETADO")
    print("="*70)
    print("\n📁 Archivos generados:")
    print("   • datos/ejemplo_correlacion.csv")
    print("   • datos/correlacion_oro.png")
    print("\n💡 Ahora puedes:")
    print("   • Entrenar el modelo: python entrenar_modelo.py")
    print("   • Ver predicciones: python prediccion_en_vivo.py")
    print("   • Revisar gráficos: datos/correlacion_oro.png")


def ejemplo_prediccion_simple():
    """
    Ejemplo simple de cómo el oro afecta una predicción
    """
    
    print("\n\n" + "="*70)
    print("🔮 EJEMPLO: PREDICCIÓN SIMPLE CON ORO")
    print("="*70)
    
    if not os.path.exists('datos/ejemplo_correlacion.csv'):
        print("❌ Error: Primero ejecuta el análisis de correlación")
        return
    
    df = pd.read_csv('datos/ejemplo_correlacion.csv')
    
    if 'correlacion' not in df.columns:
        print("❌ Error: No hay datos de correlación")
        return
    
    # Simulación simple
    print("\n💭 Simulación de señal de trading:")
    print("\nSituación actual:")
    
    ultima = df.iloc[-1]
    anterior = df.iloc[-2]
    
    eur_cambio = ((ultima['close'] - anterior['close']) / anterior['close']) * 100
    
    print(f"   EUR/USD: {ultima['close']:.5f}")
    print(f"   Cambio: {eur_cambio:+.3f}%")
    
    if 'close_oro' in df.columns:
        oro_cambio = ((ultima['close_oro'] - anterior['close_oro']) / anterior['close_oro']) * 100
        print(f"   Oro: {ultima['close_oro']:.2f}")
        print(f"   Cambio oro: {oro_cambio:+.3f}%")
        
        print(f"\n   Correlación: {ultima['correlacion']:.3f}")
        
        # Lógica simple
        print("\n🤔 Interpretación:")
        
        if ultima['correlacion'] > 0.5:
            print("   ✅ Correlación fuerte detectada")
            
            if oro_cambio > 0.1 and eur_cambio > 0:
                print("   → 🟢 ORO SUBE + EUR SUBE = SEÑAL ALCISTA FUERTE")
                print("   → Recomendación: COMPRAR con alta confianza")
            elif oro_cambio > 0.1 and eur_cambio < 0:
                print("   → ⚠️ ORO SUBE pero EUR BAJA = DIVERGENCIA")
                print("   → Recomendación: ESPERAR (señal contradictoria)")
            elif oro_cambio < -0.1 and eur_cambio < 0:
                print("   → 🔴 ORO BAJA + EUR BAJA = SEÑAL BAJISTA FUERTE")
                print("   → Recomendación: VENDER con alta confianza")
            elif oro_cambio < -0.1 and eur_cambio > 0:
                print("   → ⚠️ ORO BAJA pero EUR SUBE = DIVERGENCIA")
                print("   → Recomendación: ESPERAR (señal contradictoria)")
            else:
                print("   → ⚪ Movimientos menores")
                print("   → Recomendación: ESPERAR")
        else:
            print("   ⚠️ Correlación débil - oro no es buen indicador ahora")
            print("   → Usar otros indicadores técnicos")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 INICIANDO EJEMPLOS DE CORRELACIÓN")
    print("="*70)
    
    try:
        # Ejemplo 1: Análisis completo
        ejemplo_analisis_correlacion()
        
        # Ejemplo 2: Predicción simple
        ejemplo_prediccion_simple()
        
        print("\n\n" + "="*70)
        print("✅ TODOS LOS EJEMPLOS COMPLETADOS")
        print("="*70)
        print("\n💡 Próximos pasos:")
        print("   1. Revisa datos/correlacion_oro.png")
        print("   2. Analiza datos/ejemplo_correlacion.csv")
        print("   3. Entrena el modelo: python entrenar_modelo.py")
        print("   4. Lee CORRELACION_ORO_README.md para más info")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n👉 Asegúrate de haber ejecutado: python extraer_datos.py")
