"""
═══════════════════════════════════════════════════════════════
    CONFIGURACIÓN DEL SISTEMA
═══════════════════════════════════════════════════════════════

🎯 AQUÍ CAMBIAS TODO LO QUE NECESITES

Solo modifica las variables de abajo y guarda el archivo.
"""

# ═══════════════════════════════════════════════════════════════
# 📊 PAR DE DIVISAS
# ═══════════════════════════════════════════════════════════════
# Opciones comunes:
#   "EURUSD"  → Euro / Dólar
#   "GBPUSD"  → Libra / Dólar
#   "USDJPY"  → Dólar / Yen
#   "EURJPY"  → Euro / Yen
#   "AUDUSD"  → Dólar Australiano / Dólar
#   "USDCAD"  → Dólar / Dólar Canadiense
#   "NZDUSD"  → Dólar Neozelandés / Dólar
#   "EURGBP"  → Euro / Libra

PAR_DIVISAS = "EURAUD"


# ═══════════════════════════════════════════════════════════════
# ⏰ TIMEFRAME (Periodo de tiempo)
# ═══════════════════════════════════════════════════════════════
# Opciones disponibles:
#   "H1"  → 1 hora (señales cada 1-3 horas)
#   "H4"  → 4 horas (señales cada 4-12 horas) ← RECOMENDADO
#   "D1"  → 1 día (señales cada varios días)

TIMEFRAME = "H4"


# ═══════════════════════════════════════════════════════════════
# 💰 GESTIÓN DE RIESGO
# ═══════════════════════════════════════════════════════════════

# Take Profit en pips (ganancia objetivo)
TAKE_PROFIT_PIPS = 80

# Stop Loss en pips (pérdida máxima)
STOP_LOSS_PIPS = 40

# Confianza mínima para generar señal (0-100)
# Recomendado: 60-70
CONFIANZA_MINIMA = 60


# ═══════════════════════════════════════════════════════════════
# ⏱️ FRECUENCIA DE ACTUALIZACIÓN
# ═══════════════════════════════════════════════════════════════

# Cada cuántos MINUTOS revisar el mercado
# Para H1: usar 30-60 minutos
# Para H4: usar 60-120 minutos
REVISAR_CADA_MINUTOS = 60


# ═══════════════════════════════════════════════════════════════
# 📈 CANTIDAD DE DATOS HISTÓRICOS
# ═══════════════════════════════════════════════════════════════

# Cantidad de velas a descargar para entrenar
# H1: 5000-8000 velas (aprox 6-12 meses)
# H4: 2000-3000 velas (aprox 6-12 meses)
CANTIDAD_DATOS = 3000


# ═══════════════════════════════════════════════════════════════
# 🔧 CONFIGURACIÓN AVANZADA (no tocar si no sabes)
# ═══════════════════════════════════════════════════════════════

# Ventana de memoria del modelo (cuántas velas mira atrás)
LOOK_BACK = 60

# Épocas de entrenamiento (más = mejor pero más lento)
EPOCHS = 50


# ═══════════════════════════════════════════════════════════════
# ✅ RESUMEN DE TU CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════

def mostrar_configuracion():
    """Muestra la configuración actual"""
    print("\n" + "═"*70)
    print("⚙️  CONFIGURACIÓN DEL SISTEMA")
    print("═"*70)
    print(f"📊 Par de divisas:        {PAR_DIVISAS}")
    print(f"⏰ Timeframe:             {TIMEFRAME}")
    print(f"🎯 Take Profit:           {TAKE_PROFIT_PIPS} pips")
    print(f"🛡️  Stop Loss:             {STOP_LOSS_PIPS} pips")
    print(f"📈 Confianza mínima:      {CONFIANZA_MINIMA}%")
    print(f"🔄 Revisar cada:          {REVISAR_CADA_MINUTOS} minutos")
    print(f"💾 Datos históricos:      {CANTIDAD_DATOS} velas")
    print("═"*70 + "\n")


# ═══════════════════════════════════════════════════════════════
# 📝 MAPEO DE TIMEFRAMES
# ═══════════════════════════════════════════════════════════════

TIMEFRAME_MAP = {
    "M5": 5,
    "M15": 15,
    "M30": 30,
    "H1": 16385,
    "H4": 16388,
    "D1": 16408
}

def get_timeframe_mt5():
    """Obtiene el código de timeframe para MT5"""
    return TIMEFRAME_MAP.get(TIMEFRAME, 16388)  # Default H4


# ═══════════════════════════════════════════════════════════════
# 💡 EJEMPLOS DE USO
# ═══════════════════════════════════════════════════════════════

"""
EJEMPLO 1: Quiero EUR/USD en H1
-------------------------------
PAR_DIVISAS = "EURUSD"
TIMEFRAME = "H1"


EJEMPLO 2: Quiero EUR/JPY en H4
--------------------------------
PAR_DIVISAS = "EURJPY"
TIMEFRAME = "H4"


EJEMPLO 3: Quiero GBP/USD en H1 con más riesgo
-----------------------------------------------
PAR_DIVISAS = "GBPUSD"
TIMEFRAME = "H1"
TAKE_PROFIT_PIPS = 100
STOP_LOSS_PIPS = 50
"""