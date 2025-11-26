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

PAR_DIVISAS = "EURUSD"


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
# 🥇 CORRELACIÓN CON ORO
# ═══════════════════════════════════════════════════════════════

# Activar/Desactivar correlación con ORO (XAU/USD)
USAR_CORRELACION_ORO = True

# Ventana de correlación móvil (periodos)
# Valores típicos: 50-200
# Más alto = correlación más suave pero menos reactiva
# Más bajo = correlación más reactiva pero más volátil
VENTANA_CORRELACION_ORO = 100

# Peso de la correlación con oro en el modelo (0.0 - 1.0)
# 1.0 = máxima influencia del oro
# 0.5 = influencia moderada
# 0.0 = sin influencia (desactivado)
PESO_ORO = 0.7


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
    print(f"🥇 Correlación con ORO:   {'ACTIVADA' if USAR_CORRELACION_ORO else 'DESACTIVADA'}")
    if USAR_CORRELACION_ORO:
        print(f"   • Ventana correlación: {VENTANA_CORRELACION_ORO} periodos")
        print(f"   • Peso del oro:        {PESO_ORO*100:.0f}%")
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