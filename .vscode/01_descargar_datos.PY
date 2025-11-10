import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta, timezone

# Inicializar conexión
if not mt5.initialize():
    print("❌ No se pudo conectar a MetaTrader 5")
    quit()

symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_M5  # M5 = 5 minutos
num_candles = 10000            # cantidad de velas (puedes ajustar)

# Tomamos datos de los últimos 30 días aprox.
utc_from = datetime.now(timezone.utc) - timedelta(days=30)

rates = mt5.copy_rates_from(symbol, timeframe, utc_from, num_candles)
mt5.shutdown()

# Convertir a DataFrame
df = pd.DataFrame(rates)
df['time'] = pd.to_datetime(df['time'], unit='s')
df.set_index('time', inplace=True)

print(df.head())
df.to_csv("eurusd_m5.csv")
print("✅ Datos guardados en 'eurusd_m5.csv'")
