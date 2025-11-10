import MetaTrader5 as mt5

# Inicializar la conexión
if not mt5.initialize():
    print("❌ No se pudo conectar a MetaTrader 5")
    mt5.shutdown()
else:
    print("✅ Conectado correctamente a MetaTrader 5")

# Obtener información de un símbolo (EURUSD)
symbol = "EURUSD"
info = mt5.symbol_info(symbol)
if info:
    print(f"Símbolo: {info.name}")
    print(f"Precio actual BID: {info.bid}")
    print(f"Precio actual ASK: {info.ask}")
else:
    print(f"⚠️ No se encontró el símbolo {symbol}")

mt5.shutdown()
