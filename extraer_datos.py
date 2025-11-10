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

def conectar_mt5():
    """Conecta con MetaTrader 5"""
    print("🔌 Conectando con MetaTrader5...")
    
    # Inicializar MT5
    if not mt5.initialize():
        print("❌ Error: No se pudo inicializar MT5")
        print("👉 Asegúrate de que MetaTrader5 esté ABIERTO")
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
    
    # 2. Descargar datos (usando configuración de config.py)
    df = descargar_datos(
        symbol=config.PAR_DIVISAS,
        timeframe=config.get_timeframe_mt5(),
        num_velas=config.CANTIDAD_DATOS
    )
    
    if df is not None:
        # 3. Guardar datos
        guardar_datos(df)
        
        print("\n" + "="*60)
        print("✅ PROCESO COMPLETADO!")
        print("="*60)
        print("👉 Ahora ejecuta: entrenar_modelo.py")
    
    # 4. Cerrar conexión
    mt5.shutdown()
    print("\n🔌 Conexión cerrada")

if __name__ == "__main__":
    main()