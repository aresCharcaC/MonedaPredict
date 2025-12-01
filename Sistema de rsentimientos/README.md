# 🧠 Sistema de Análisis de Sentimientos para EUR/USD

## 📋 Descripción General

Sistema **independiente y autónomo** de análisis de sentimientos financieros específicamente diseñado para el par EUR/USD. Este sistema analiza noticias de múltiples fuentes, calcula el sentimiento con NLP, y genera señales de trading basadas en análisis fundamental.

---

## 🎯 Características Principales

### ✅ **Autonomía Completa**
- No requiere el sistema LSTM principal
- Funciona de forma independiente
- Genera sus propias señales de trading

### ✅ **Múltiples Fuentes de Noticias**
- Google News (EUR/USD, ECB, Fed)
- Investing.com (Forex)
- FXStreet (Análisis técnico)
- ForexLive (Noticias en tiempo real)

### ✅ **Análisis NLP Avanzado**
- VADER Sentiment (inglés)
- Detección de entidades (EUR, USD, ECB, Fed)
- Clasificación de impacto en el par
- Ponderación por relevancia

### ✅ **Generación de Señales**
- Señales COMPRA/VENTA/ESPERA
- Nivel de confianza (0-100%)
- Indicador de urgencia
- Horizonte temporal de la señal

---

## 📁 Estructura del Sistema

```
Sistema de rsentimientos/
├── README.md                          ← Este archivo
├── config_sentimientos.py             ← Configuración del sistema
├── recolector_noticias.py            ← Obtiene noticias de múltiples fuentes
├── analizador_sentimientos.py        ← Análisis NLP y clasificación
├── generador_señales_sentimientos.py ← Genera señales de trading
├── monitor_sentimientos.py           ← Monitoreo en tiempo real
├── visualizador_sentimientos.py      ← Dashboards y gráficos
├── datos_sentimientos/               ← Datos generados
│   ├── noticias_raw.csv
│   ├── noticias_analizadas.csv
│   ├── señales_sentimiento.csv
│   └── historico_sentimiento.csv
└── reportes/                         ← Reportes generados
    ├── reporte_diario_YYYYMMDD.txt
    └── reporte_semanal_YYYYMMDD.txt
```

---

## 🚀 Instalación

### 1. Instalar Dependencias

```bash
pip install vaderSentiment beautifulsoup4 requests pandas numpy matplotlib seaborn
pip install textblob nltk
```

### 2. Descargar Datos de NLTK (primera vez)

```python
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
```

---

## 💻 Uso del Sistema

### **Modo 1: Análisis Único (One-Shot)**

Obtiene noticias actuales y genera una señal:

```bash
cd "Sistema de rsentimientos"
python generador_señales_sentimientos.py
```

**Salida ejemplo:**
```
═══════════════════════════════════════════════════════════
🧠 SEÑAL DE SENTIMIENTO EUR/USD
═══════════════════════════════════════════════════════════

📈 RECOMENDACIÓN: COMPRA
🎯 Confianza: 78.5%
⚡ Urgencia: ALTA
⏰ Horizonte: 4-12 horas

📊 Análisis:
   • Noticias analizadas: 45
   • Sentimiento promedio: +0.65 (Muy Positivo para EUR)
   • Balance: 28 positivas, 12 neutrales, 5 negativas
   
💡 Principales factores:
   ✅ ECB mantiene política monetaria fuerte
   ✅ Datos económicos europeos superan expectativas
   ⚠️ Fed sugiere posible pausa en alzas de tasas
```

### **Modo 2: Monitoreo Continuo**

Monitorea noticias en tiempo real y actualiza señales:

```bash
python monitor_sentimientos.py
```

- Actualiza cada 30 minutos
- Genera alertas cuando cambia la señal
- Guarda histórico automáticamente

### **Modo 3: Solo Análisis (Sin Señales)**

Obtiene y analiza noticias sin generar señales:

```bash
python recolector_noticias.py
python analizador_sentimientos.py
```

---

## ⚙️ Configuración

Editar `config_sentimientos.py`:

```python
# Fuentes de noticias
USAR_GOOGLE_NEWS = True
USAR_INVESTING = True
USAR_FXSTREET = True
USAR_FOREXLIVE = True

# Cantidad de noticias
NOTICIAS_POR_FUENTE = 20
MAX_NOTICIAS_TOTALES = 100

# Análisis de sentimiento
UMBRAL_POSITIVO = 0.05      # Sentimiento > 0.05 = Positivo
UMBRAL_NEGATIVO = -0.05     # Sentimiento < -0.05 = Negativo

# Generación de señales
CONFIANZA_MINIMA = 60       # Mínimo 60% para generar señal
PESO_RECIENTE = 0.7         # 70% peso a noticias últimas 24h

# Actualización
INTERVALO_MINUTOS = 30      # Actualizar cada 30 min
```

---

## 📊 Interpretación de Resultados

### **Niveles de Sentimiento**

| Score | Clasificación | Significado |
|-------|---------------|-------------|
| +0.70 a +1.00 | Muy Positivo EUR | Fuerte señal de COMPRA |
| +0.30 a +0.69 | Positivo EUR | Señal de COMPRA moderada |
| -0.29 a +0.29 | Neutral | ESPERAR |
| -0.69 a -0.30 | Negativo EUR | Señal de VENTA moderada |
| -1.00 a -0.70 | Muy Negativo EUR | Fuerte señal de VENTA |

### **Niveles de Confianza**

| Confianza | Acción Recomendada |
|-----------|-------------------|
| 80-100% | Operar con alta confianza |
| 60-79% | Operar con precaución |
| 40-59% | Considerar esperar |
| 0-39% | NO operar |

### **Urgencia**

- **MUY ALTA**: Noticias de última hora (< 2 horas)
- **ALTA**: Noticias recientes (< 12 horas)
- **MEDIA**: Noticias del día (< 24 horas)
- **BAJA**: Noticias antiguas (> 24 horas)

---

## 📈 Casos de Uso

### **1. Trading de Noticias (News Trading)**

Ideal para operar eventos económicos importantes:

```bash
# Antes de evento (ej: decisión ECB)
python generador_señales_sentimientos.py

# Monitorear durante el evento
python monitor_sentimientos.py
```

### **2. Validación de Señales Técnicas**

Combinar con análisis técnico del sistema principal:

```python
# Obtener señal de sentimiento
from generador_señales_sentimientos import obtener_señal_actual

señal_sentimiento = obtener_señal_actual()
# Comparar con señal LSTM/KNN del sistema principal
```

### **3. Análisis Fundamental Diario**

Revisar el sentimiento del mercado cada mañana:

```bash
# Ejecutar cada día a las 8 AM
python generador_señales_sentimientos.py --reporte-diario
```

---

## 🔍 Detección de Eventos Importantes

El sistema identifica automáticamente:

### **Eventos del BCE (ECB)**
- Decisiones de tasas de interés
- Conferencias de prensa de Lagarde
- Minutas de reuniones
- Proyecciones económicas

### **Eventos de la Fed**
- Decisiones de tasas de interés
- Discursos de Powell
- Minutas del FOMC
- Datos de empleo (NFP)

### **Datos Económicos**
- PIB (Europa y USA)
- Inflación (CPI, PCE)
- Empleo (NFP, desempleo)
- Confianza del consumidor
- PMI manufacturero

### **Eventos Geopolíticos**
- Crisis políticas
- Elecciones importantes
- Conflictos internacionales
- Sanciones económicas

---

## 📊 Visualizaciones Disponibles

### **Dashboard de Sentimiento**

```bash
python visualizador_sentimientos.py --dashboard
```

Muestra:
- Evolución del sentimiento en tiempo real
- Balance positivo/negativo
- Fuentes más relevantes
- Palabras clave más frecuentes
- Correlación con movimientos de precio

### **Reporte Semanal**

```bash
python visualizador_sentimientos.py --reporte-semanal
```

Genera PDF con:
- Resumen ejecutivo
- Gráficas de tendencias
- Eventos más importantes
- Análisis de correlación
- Recomendaciones

---

## 🔄 Integración con Sistema Principal

Aunque es autónomo, puede integrarse:

```python
# En el sistema principal (MonedaPredict)
import sys
sys.path.append('Sistema de rsentimientos')

from generador_señales_sentimientos import obtener_señal_actual

# Obtener señal de sentimiento
señal_sent = obtener_señal_actual()

# Combinar con LSTM + KNN
if señal_lstm == "COMPRA" and señal_knn == "COMPRA" and señal_sent["accion"] == "COMPRA":
    confianza_final = (conf_lstm * 0.3 + conf_knn * 0.4 + señal_sent["confianza"] * 0.3)
    print(f"🚀 SEÑAL TRIPLE CONFIRMADA - Confianza: {confianza_final}%")
```

---

## 🎯 Ventajas del Sistema

### **vs Análisis Técnico Solo**
✅ Anticipa movimientos antes de que aparezcan en el precio  
✅ Identifica catalizadores fundamentales  
✅ Evita operar contra noticias importantes  

### **vs Lectura Manual de Noticias**
✅ Analiza 100+ noticias en segundos  
✅ Sin sesgo emocional  
✅ Cuantifica el sentimiento objetivamente  
✅ Funciona 24/7  

### **vs Sistemas Genéricos de Sentimiento**
✅ Específico para EUR/USD  
✅ Conoce eventos relevantes del par  
✅ Pondera correctamente fuentes forex  
✅ Entiende jerga financiera  

---

## 📝 Registro de Cambios

### v1.0.0 (01/12/2025)
- ✅ Sistema inicial completo
- ✅ 4 fuentes de noticias
- ✅ Análisis VADER
- ✅ Generación de señales
- ✅ Monitoreo en tiempo real

---

## 🔮 Roadmap Futuro

- [ ] Integración con API de Twitter para sentimiento social
- [ ] Análisis de correlación precio-sentimiento
- [ ] Machine Learning para mejorar clasificación
- [ ] Alertas por Telegram/Email
- [ ] API REST para consultas externas
- [ ] Backtesting de señales de sentimiento

---

## 📞 Soporte

Para dudas o problemas:
1. Revisar este README
2. Revisar logs en `datos_sentimientos/logs/`
3. Ejecutar modo debug: `python generador_señales_sentimientos.py --debug`

---

## ⚠️ Disclaimer

Este sistema es una **herramienta de ayuda** para toma de decisiones. No garantiza ganancias. Siempre:
- Usa gestión de riesgo apropiada
- Combina con análisis técnico
- Verifica noticias importantes manualmente
- Nunca arriesges más de lo que puedes perder

---

**Sistema de Sentimientos EUR/USD v1.0.0**  
*Análisis Fundamental Automatizado con NLP*
