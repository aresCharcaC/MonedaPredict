"""
╔══════════════════════════════════════════════════════════════════╗
║          CONFIGURACIÓN - SISTEMA DE SENTIMIENTOS EUR/USD         ║
╚══════════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════════
# 📰 FUENTES DE NOTICIAS
# ═══════════════════════════════════════════════════════════════

# Activar/Desactivar fuentes
USAR_GOOGLE_NEWS = True
USAR_INVESTING = True
USAR_FXSTREET = True
USAR_FOREXLIVE = True

# Cantidad de noticias por fuente
NOTICIAS_POR_FUENTE = 20

# Máximo total de noticias a analizar
MAX_NOTICIAS_TOTALES = 100


# ═══════════════════════════════════════════════════════════════
# 🔍 BÚSQUEDA Y FILTRADO
# ═══════════════════════════════════════════════════════════════

# Palabras clave para búsqueda (EUR/USD específico)
KEYWORDS_EURUSD = [
    "EUR USD", "EURUSD", "euro dollar",
    "ECB", "European Central Bank", "Lagarde",
    "Fed", "Federal Reserve", "Powell",
    "EUR", "euro", "eurozone",
    "dollar", "USD", "US economy"
]

# Palabras clave de eventos importantes
KEYWORDS_EVENTOS_IMPORTANTES = [
    "interest rate", "tasa de interés",
    "inflation", "inflación",
    "GDP", "PIB",
    "employment", "empleo", "NFP",
    "CPI", "PCE",
    "monetary policy", "política monetaria",
    "FOMC", "meeting", "decision"
]

# Filtrar solo noticias relevantes para EUR/USD
FILTRAR_RELEVANCIA = True
RELEVANCIA_MINIMA = 0.3  # 0.0 - 1.0


# ═══════════════════════════════════════════════════════════════
# 🧠 ANÁLISIS DE SENTIMIENTO
# ═══════════════════════════════════════════════════════════════

# Umbrales de clasificación
UMBRAL_POSITIVO = 0.05      # Sentimiento > 0.05 = Positivo
UMBRAL_NEGATIVO = -0.05     # Sentimiento < -0.05 = Negativo

# Ponderación por antigüedad de noticias
PESO_ULTIMAS_2H = 1.0       # Noticias últimas 2 horas: peso 100%
PESO_ULTIMAS_12H = 0.8      # Noticias últimas 12 horas: peso 80%
PESO_ULTIMAS_24H = 0.6      # Noticias últimas 24 horas: peso 60%
PESO_MAS_24H = 0.3          # Noticias más antiguas: peso 30%

# Ponderación por fuente
PESO_FUENTES = {
    'FXStreet': 1.0,        # Especialistas en Forex
    'ForexLive': 1.0,       # Noticias en tiempo real
    'Investing.com': 0.9,   # General financiero
    'Google News': 0.7      # Noticias generales
}

# Multiplicadores por tipo de evento
MULTIPLICADOR_EVENTO_ECB = 2.0      # Eventos del BCE tienen doble peso
MULTIPLICADOR_EVENTO_FED = 1.8      # Eventos de la Fed tienen 1.8x peso
MULTIPLICADOR_DATO_ECONOMICO = 1.5  # Datos económicos importantes
MULTIPLICADOR_GEOPOLITICO = 1.3     # Eventos geopolíticos


# ═══════════════════════════════════════════════════════════════
# 📊 GENERACIÓN DE SEÑALES
# ═══════════════════════════════════════════════════════════════

# Confianza mínima para generar señal
CONFIANZA_MINIMA_COMPRA = 60    # Mínimo 60% para COMPRA
CONFIANZA_MINIMA_VENTA = 60     # Mínimo 60% para VENTA

# Balance mínimo de noticias para señal fuerte
BALANCE_MINIMO_FUERTE = 0.6     # 60% de noticias en la misma dirección

# Cantidad mínima de noticias para generar señal
NOTICIAS_MINIMAS = 10           # Al menos 10 noticias para analizar

# Horizonte temporal de señales
HORIZONTE_CORTO_PLAZO = 4       # 4 horas
HORIZONTE_MEDIO_PLAZO = 12      # 12 horas
HORIZONTE_LARGO_PLAZO = 24      # 24 horas


# ═══════════════════════════════════════════════════════════════
# ⏰ ACTUALIZACIÓN Y MONITOREO
# ═══════════════════════════════════════════════════════════════

# Intervalo de actualización (minutos)
INTERVALO_ACTUALIZACION = 30    # Actualizar cada 30 minutos

# Guardar histórico
GUARDAR_HISTORICO = True
DIAS_HISTORICO = 30             # Mantener últimos 30 días


# ═══════════════════════════════════════════════════════════════
# 📁 RUTAS Y ARCHIVOS
# ═══════════════════════════════════════════════════════════════

# Carpetas
CARPETA_DATOS = "datos_sentimientos"
CARPETA_REPORTES = "reportes"
CARPETA_LOGS = f"{CARPETA_DATOS}/logs"

# Archivos de datos
ARCHIVO_NOTICIAS_RAW = f"{CARPETA_DATOS}/noticias_raw.csv"
ARCHIVO_NOTICIAS_ANALIZADAS = f"{CARPETA_DATOS}/noticias_analizadas.csv"
ARCHIVO_SEÑALES = f"{CARPETA_DATOS}/señales_sentimiento.csv"
ARCHIVO_HISTORICO = f"{CARPETA_DATOS}/historico_sentimiento.csv"


# ═══════════════════════════════════════════════════════════════
# 🎨 VISUALIZACIÓN
# ═══════════════════════════════════════════════════════════════

# Configuración de gráficos
ESTILO_GRAFICOS = "seaborn-v0_8-darkgrid"
TAMAÑO_FIGURA = (15, 8)
DPI = 100

# Colores
COLOR_POSITIVO = "#2ecc71"      # Verde
COLOR_NEGATIVO = "#e74c3c"      # Rojo
COLOR_NEUTRAL = "#95a5a6"       # Gris


# ═══════════════════════════════════════════════════════════════
# 🔔 ALERTAS
# ═══════════════════════════════════════════════════════════════

# Activar alertas
ALERTAS_ACTIVADAS = True

# Umbral para alerta de cambio de señal
UMBRAL_CAMBIO_SEÑAL = 20        # 20% cambio en sentimiento = alerta

# Eventos que siempre generan alerta
ALERTAS_EVENTOS_CRITICOS = [
    "interest rate decision",
    "ECB press conference",
    "FOMC meeting",
    "NFP",
    "CPI release"
]


# ═══════════════════════════════════════════════════════════════
# 🐛 DEBUG Y LOGGING
# ═══════════════════════════════════════════════════════════════

# Nivel de logging
# DEBUG, INFO, WARNING, ERROR, CRITICAL
NIVEL_LOG = "INFO"

# Mostrar detalles en consola
MODO_VERBOSE = True

# Guardar logs en archivo
GUARDAR_LOGS = True


# ═══════════════════════════════════════════════════════════════
# 🌐 URLs DE FUENTES (No modificar a menos que cambien)
# ═══════════════════════════════════════════════════════════════

URLS = {
    'google_news': "https://news.google.com/rss",
    'investing': "https://www.investing.com/rss/news.rss",
    'fxstreet': "https://www.fxstreet.com/rss",
    'forexlive': "https://www.forexlive.com/feed/news"
}


# ═══════════════════════════════════════════════════════════════
# ✅ VALIDACIÓN DE CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════

def validar_configuracion():
    """Valida que la configuración sea correcta"""
    errores = []
    
    # Validar umbrales
    if UMBRAL_POSITIVO <= UMBRAL_NEGATIVO:
        errores.append("UMBRAL_POSITIVO debe ser mayor que UMBRAL_NEGATIVO")
    
    # Validar confianza mínima
    if not (0 <= CONFIANZA_MINIMA_COMPRA <= 100):
        errores.append("CONFIANZA_MINIMA_COMPRA debe estar entre 0 y 100")
    
    if not (0 <= CONFIANZA_MINIMA_VENTA <= 100):
        errores.append("CONFIANZA_MINIMA_VENTA debe estar entre 0 y 100")
    
    # Validar balance
    if not (0 <= BALANCE_MINIMO_FUERTE <= 1):
        errores.append("BALANCE_MINIMO_FUERTE debe estar entre 0 y 1")
    
    # Validar noticias
    if NOTICIAS_MINIMAS < 5:
        errores.append("NOTICIAS_MINIMAS debe ser al menos 5")
    
    if errores:
        print("\n❌ ERRORES EN CONFIGURACIÓN:")
        for error in errores:
            print(f"   • {error}")
        return False
    
    return True


def mostrar_configuracion():
    """Muestra la configuración actual"""
    print("\n" + "═"*70)
    print("⚙️  CONFIGURACIÓN DEL SISTEMA DE SENTIMIENTOS")
    print("═"*70)
    
    print("\n📰 FUENTES DE NOTICIAS:")
    print(f"   Google News:    {'✅' if USAR_GOOGLE_NEWS else '❌'}")
    print(f"   Investing.com:  {'✅' if USAR_INVESTING else '❌'}")
    print(f"   FXStreet:       {'✅' if USAR_FXSTREET else '❌'}")
    print(f"   ForexLive:      {'✅' if USAR_FOREXLIVE else '❌'}")
    print(f"   Noticias/fuente: {NOTICIAS_POR_FUENTE}")
    print(f"   Máximo total:    {MAX_NOTICIAS_TOTALES}")
    
    print("\n🧠 ANÁLISIS:")
    print(f"   Umbral positivo:  {UMBRAL_POSITIVO}")
    print(f"   Umbral negativo:  {UMBRAL_NEGATIVO}")
    print(f"   Relevancia mín:   {RELEVANCIA_MINIMA}")
    
    print("\n📊 SEÑALES:")
    print(f"   Confianza mín (COMPRA): {CONFIANZA_MINIMA_COMPRA}%")
    print(f"   Confianza mín (VENTA):  {CONFIANZA_MINIMA_VENTA}%")
    print(f"   Noticias mínimas:       {NOTICIAS_MINIMAS}")
    
    print("\n⏰ ACTUALIZACIÓN:")
    print(f"   Intervalo:     {INTERVALO_ACTUALIZACION} minutos")
    print(f"   Histórico:     {DIAS_HISTORICO} días")
    
    print("\n🔔 ALERTAS:")
    print(f"   Activadas:     {'✅' if ALERTAS_ACTIVADAS else '❌'}")
    
    print("═"*70 + "\n")


if __name__ == "__main__":
    if validar_configuracion():
        print("✅ Configuración válida")
        mostrar_configuracion()
    else:
        print("\n❌ Corrige los errores antes de continuar")
