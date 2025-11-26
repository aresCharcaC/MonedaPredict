"""
ARCHIVO 1: EXTRAER DATOS DE METATRADER 5
========================================
Este script conecta con MetaTrader5 y descarga datos históricos de EUR/USD
"""

import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import os
import config  # Importar configuración
import correlacion_oro  # Módulo de correlación con oro

def conectar_mt5():
    """Conecta con MetaTrader 5"""
    print("🔌 Conectando con MetaTrader5...")
    
    # Inicializar MT5
    if not mt5.initialize():
        print("Error: No se pudo inicializar MT5")
        print("Asegúrate de que MetaTrader5 esté ABIERTO")
        return False
    
    print("✅ Conectado exitosamente!")
    print(f"📊 Versión MT5: {mt5.version()}")
    
    # Mostrar info de la cuenta
    account_info = mt5.account_info()
    if account_info:
        print(f"💰 Balance: ${account_info.balance}")
        print(f"🌐 Servidor: {account_info.server}")
    
    return True

def descargar_datos(symbol="EURUSD", timeframe=mt5.TIMEFRAME_M15, num_velas=10000):
    """
    Descarga datos históricos
    
    Parámetros:
    - symbol: Par de divisas (default: EURUSD)
    - timeframe: Periodo de tiempo
        mt5.TIMEFRAME_M5  = 5 minutos
        mt5.TIMEFRAME_M15 = 15 minutos
        mt5.TIMEFRAME_H1  = 1 hora
    - num_velas: Cantidad de velas a descargar (default: 10000)
    """
    
    print(f"\n📥 Descargando {num_velas} velas de {symbol}...")
    
    # Obtener datos
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_velas)
    
    if rates is None:
        print(f"❌ Error al descargar datos. Código: {mt5.last_error()}")
        return None
    
    # Convertir a DataFrame
    df = pd.DataFrame(rates)
    
    # Convertir timestamp a fecha legible
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    # Mostrar info
    print(f"✅ Datos descargados exitosamente!")
    print(f"📅 Desde: {df['time'].min()}")
    print(f"📅 Hasta: {df['time'].max()}")
    print(f"📊 Total de registros: {len(df)}")
    
    return df

def guardar_datos(df, filename="datos/eurusd_datos.csv"):
    """Guarda los datos en un archivo CSV"""
    
    # Crear carpeta si no existe
    os.makedirs("datos", exist_ok=True)
    
    # Guardar CSV
    df.to_csv(filename, index=False)
    print(f"\n💾 Datos guardados en: {filename}")
    
    # Mostrar primeras filas
    print("\n📋 Vista previa de los datos:")
    print(df.head())
    print(f"\n📊 Columnas disponibles: {list(df.columns)}")

def main():
    """Función principal"""
    
    print("="*60)
    print("🚀 EXTRACTOR DE DATOS DE METATRADER 5")
    print("="*60)
    
    # 1. Conectar con MT5
    if not conectar_mt5():
        return
    
    # 2. Descargar datos de EUR/USD (usando configuración de config.py)
    print("\n📊 PASO 1: Descargando EUR/USD...")
    df_eurusd = descargar_datos(
        symbol=config.PAR_DIVISAS,
        timeframe=config.get_timeframe_mt5(),
        num_velas=config.CANTIDAD_DATOS
    )
    
    if df_eurusd is None:
        mt5.shutdown()
        return
    
    # 3. Descargar datos de ORO (XAU/USD)
    print("\n📊 PASO 2: Descargando datos de ORO (XAU/USD)...")
    df_oro = descargar_datos(
        symbol="XAUUSD",  # Símbolo del oro
        timeframe=config.get_timeframe_mt5(),
        num_velas=config.CANTIDAD_DATOS
    )
    
    if df_oro is None:
        print("⚠️ Advertencia: No se pudieron descargar datos del oro")
        print("   Continuando solo con EUR/USD...")
        # Guardar solo EUR/USD
        guardar_datos(df_eurusd)
    else:
        # 4. Calcular correlación
        print("\n📊 PASO 3: Calculando correlación con ORO...")
        df_merged, correlacion_general = correlacion_oro.calcular_correlacion(df_eurusd, df_oro)
        
        # 5. Crear features de oro
        print("\n📊 PASO 4: Creando features de oro...")
        df_merged_features = correlacion_oro.crear_features_oro(df_merged)
        
        # 6. Mostrar resumen de correlación
        correlacion_oro.resumen_correlacion(df_merged_features)
        
        # 7. Crear visualización
        correlacion_oro.visualizar_correlacion(df_merged_features, guardar=True)
        
        # 8. Integrar datos de oro con EUR/USD
        print("\n📊 PASO 5: Integrando datos finales...")
        df_final, _ = correlacion_oro.integrar_oro_a_eurusd(df_eurusd, df_oro)
        
        # 9. Guardar datos integrados
        print("\n📊 PASO 6: Guardando datos...")
        guardar_datos(df_final, filename="datos/eurusd_con_oro.csv")
        
        # También guardar datos individuales por si acaso
        guardar_datos(df_eurusd, filename="datos/eurusd_datos.csv")
        guardar_datos(df_oro, filename="datos/oro_datos.csv")
        
        print("\n" + "="*60)
        print("✅ PROCESO COMPLETADO CON ÉXITO!")
        print("="*60)
        print(f"\n📈 Correlación EUR/USD - ORO: {correlacion_general:.4f}")
        print("\n💾 Archivos guardados:")
        print("   • datos/eurusd_con_oro.csv (con features de oro)")
        print("   • datos/eurusd_datos.csv (solo EUR/USD)")
        print("   • datos/oro_datos.csv (solo ORO)")
        print("   • datos/correlacion_oro.png (visualización)")
        print("\n👉 Ahora ejecuta: entrenar_modelo.py")
    
    # 8. Cerrar conexión
    mt5.shutdown()
    print("\n🔌 Conexión cerrada")

if __name__ == "__main__":
    main()