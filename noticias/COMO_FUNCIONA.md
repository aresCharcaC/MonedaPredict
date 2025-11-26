# 🧠 Cómo Funciona el Sistema de Análisis de Sentimiento

## 📋 Visión General

El sistema de sentimiento analiza noticias financieras para predecir el impacto en EUR/USD mediante **Procesamiento de Lenguaje Natural (NLP)**.

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUJO DEL SISTEMA                            │
└─────────────────────────────────────────────────────────────────┘

1. OBTENER NOTICIAS          2. ANALIZAR              3. INTEGRAR
   (obtener_noticias.py)        (analizar_sentimiento)    (integrar_modelo)
         │                            │                         │
         ▼                            ▼                         ▼
    ┌─────────┐               ┌──────────────┐         ┌──────────────┐
    │ Google  │               │    VADER     │         │   Agregar    │
    │  News   │──────────────▶│  Sentiment   │────────▶│  Features    │
    │   RSS   │   20 noticias │   Analyzer   │  Scores │  al modelo   │
    └─────────┘               └──────────────┘         └──────────────┘
                                      │                         │
                                      ▼                         ▼
                              sentimiento_compound      sent_mean, impact_mean
                              clasificacion             sent_balance, sent_trend
                              impacto_eur               sent_ma_24h
```

---

## 🔍 PASO 1: Obtener Noticias

### Fuente de Datos
- **Google News RSS** (método actual - gratis, ilimitado)
- **NewsAPI** (opcional - 100 requests/día)
- **Alpha Vantage** (opcional - 500 requests/día)

### Búsqueda
```python
query = "EUR USD forex currency"
```

### Datos Extraídos
```
┌──────────────────────────────────────────────────┐
│ Noticia #1                                       │
├──────────────────────────────────────────────────┤
│ Título: "EUR/USD Forecast: Euro shows signs..."  │
│ Descripción: "The euro gained strength..."      │
│ Fecha: 2025-11-14 22:59:59                       │
│ Fuente: Google News                              │
└──────────────────────────────────────────────────┘
```

### Salida
📁 **`datos/noticias_raw.csv`**
- 20+ noticias recientes
- Título, descripción, fecha, link

---

## 🧠 PASO 2: Análisis de Sentimiento con VADER

### ¿Qué es VADER?
**VADER** (Valence Aware Dictionary and sEntiment Reasoner):
- Modelo pre-entrenado para análisis de sentimiento
- Especializado en textos de redes sociales y noticias
- **No requiere entrenamiento** - funciona out-of-the-box
- Retorna scores entre -1 (negativo) y +1 (positivo)

### Proceso de Análisis

```python
texto = "EUR/USD Forecast: Euro shows signs of life"

# VADER analiza el texto
scores = analyzer.polarity_scores(texto)
# Output:
{
    'compound': 0.34,    # Score general (-1 a 1)
    'pos': 0.24,         # Positividad (0 a 1)
    'neg': 0.0,          # Negatividad (0 a 1)
    'neu': 0.76          # Neutralidad (0 a 1)
}
```

### Clasificación
```
compound >= 0.05   →  POSITIVO
compound <= -0.05  →  NEGATIVO
-0.05 a 0.05       →  NEUTRAL
```

### Interpretación para FOREX

El sistema es **inteligente** - distingue contexto:

```python
┌───────────────────────────────────────────────────────────┐
│ LÓGICA DE INTERPRETACIÓN                                  │
├───────────────────────────────────────────────────────────┤
│                                                            │
│  📰 Noticia POSITIVA sobre EURO                           │
│     → EUR sube (impacto_eur = +1)                         │
│                                                            │
│  📰 Noticia NEGATIVA sobre EURO                           │
│     → EUR baja (impacto_eur = -1)                         │
│                                                            │
│  📰 Noticia POSITIVA sobre USD/FED                        │
│     → USD sube, EUR baja (impacto_eur = -1)               │
│                                                            │
│  📰 Noticia NEGATIVA sobre USD/FED                        │
│     → USD baja, EUR sube (impacto_eur = +1)               │
│                                                            │
└───────────────────────────────────────────────────────────┘
```

### Palabras Clave Detectadas
- **EUR**: euro, europe, ecb, european central bank, eurozone
- **USD**: dollar, usd, fed, federal reserve, us economy

### Ejemplo Real

```
Noticia: "ECB raises rates to combat inflation"
         
         ┌─────────────────────────────┐
         │ 1. VADER Analiza            │
         │    compound: 0.05 (neutral) │
         └─────────────────────────────┘
                     │
                     ▼
         ┌─────────────────────────────┐
         │ 2. Detecta Keywords         │
         │    "ECB" → Es sobre EURO    │
         └─────────────────────────────┘
                     │
                     ▼
         ┌─────────────────────────────┐
         │ 3. Interpreta Contexto      │
         │    Subida de tasas = bueno  │
         │    para el EURO             │
         └─────────────────────────────┘
                     │
                     ▼
              impacto_eur = +1
              (EUR tiende a SUBIR)
```

### Salida
📁 **`datos/noticias_sentimiento.csv`**
```
| titulo | fecha | sentimiento_compound | clasificacion | impacto_eur |
|--------|-------|---------------------|---------------|-------------|
| ECB... | 11/14 | 0.05                | NEUTRAL       | +1          |
| Fed... | 11/13 | -0.34               | NEGATIVO      | +1          |
```

---

## 🔗 PASO 3: Integración con Modelo

### Agregación Diaria

Las noticias se agrupan **por día** y se calculan estadísticas:

```python
Día: 2025-11-14
Noticias: 5
  ├─ Positivas: 2
  ├─ Negativas: 1
  └─ Neutrales: 2

Cálculos:
  sent_mean     = promedio(sentimiento_compound)
  sent_std      = desviación_estándar(sentimiento)
  impact_mean   = promedio(impacto_eur)
  sent_balance  = positivas - negativas = 2 - 1 = 1
```

### Features Generadas (5 features nuevas)

```
┌─────────────────┬──────────────────────────────────────────┐
│ Feature         │ Descripción                              │
├─────────────────┼──────────────────────────────────────────┤
│ sent_mean       │ Sentimiento promedio del día (-1 a 1)    │
│ impact_mean     │ Impacto promedio en EUR/USD (-1 a 1)     │
│ sent_balance    │ Noticias positivas - negativas           │
│ sent_ma_24h     │ Media móvil 24h del sentimiento          │
│ sent_trend      │ Tendencia del sentimiento (diferencia)   │
└─────────────────┴──────────────────────────────────────────┘
```

### Unión con Datos de Precio

```
Datos de PRECIO (cada 15 min)          Datos de NOTICIAS (diarios)
┌─────────────────────────┐            ┌──────────────────────┐
│ time       | close      │            │ fecha  | sent_mean  │
├────────────┼────────────┤            ├────────┼────────────┤
│ 2025-11-14 | 1.0580     │   MERGE    │ 11/14  | 0.15       │
│ 2025-11-14 | 1.0582     │  ──────▶   │ 11/14  | 0.15       │
│ 2025-11-14 | 1.0579     │            │ 11/15  | -0.08      │
└────────────┴────────────┘            └────────┴────────────┘
                 │
                 ▼
         DATOS INTEGRADOS
┌─────────────────────────────────────────┐
│ time       | close  | sent_mean | ...  │
├────────────┼────────┼───────────┼──────┤
│ 2025-11-14 | 1.0580 | 0.15      | ...  │
│ 2025-11-14 | 1.0582 | 0.15      | ...  │
│ 2025-11-15 | 1.0579 | -0.08     | ...  │
└────────────┴────────┴───────────┴──────┘
```

### Salida Final
📁 **`datos/eurusd_con_sentimiento.csv`**
- Combina precio + indicadores técnicos + sentimiento
- Listo para entrenar el modelo LSTM

---

## 🤖 PASO 4: Uso en el Modelo LSTM

### Arquitectura del Modelo

```
FEATURES TOTALES (27):
├─ 13 Básicas (precio + indicadores técnicos)
│   ├─ open, high, low, close, volume
│   ├─ MA_10, MA_30, MA_50
│   ├─ RSI, Volatilidad
│   └─ HL_Range, Price_Change, Volume_MA
│
├─ 9 Oro (correlación XAU/USD)
│   ├─ close_oro, ratio_eur_oro
│   ├─ correlacion, oro_tendencia
│   └─ ... (5 más)
│
└─ 5 Sentimiento (análisis de noticias) ← NUEVO
    ├─ sent_mean
    ├─ impact_mean
    ├─ sent_balance
    ├─ sent_ma_24h
    └─ sent_trend
```

### Ventaja del Sentimiento

```
MODELO SIN SENTIMIENTO         MODELO CON SENTIMIENTO
      (solo técnico)                 (técnico + fundamental)
           │                                  │
           ▼                                  ▼
    ┌──────────────┐                  ┌──────────────┐
    │ Ve solo:     │                  │ Ve:          │
    │ - Precio     │                  │ - Precio     │
    │ - RSI        │                  │ - RSI        │
    │ - Volumen    │                  │ - Volumen    │
    └──────────────┘                  │ - Oro        │
           │                          │ + NOTICIAS   │ ← EXTRA
           │                          │ + SENTIMIENTO│
           ▼                          └──────────────┘
    Predicción limitada                      │
                                             ▼
                                    Predicción más informada
```

### Ejemplo de Impacto

```
Escenario: EUR/USD está en 1.0580

SIN SENTIMIENTO:
  - RSI: 45 (neutral)
  - MA cruzada: neutral
  → Predicción: 1.0582 (pequeño cambio)

CON SENTIMIENTO:
  - RSI: 45 (neutral)
  - MA cruzada: neutral
  - sent_mean: +0.65 (muy positivo)  ← CLAVE
  - impact_mean: +0.8 (noticias favorecen EUR)
  → Predicción: 1.0620 (cambio más significativo)
  
  Razón: Las noticias indican fortaleza del EUR
         que aún no se refleja en el precio
```

---

## 📊 Estadísticas y Visualización

### Correlación con Precio

```python
Sentimiento vs Retorno: 0.0026
  → Correlación débil pero positiva
  → Las noticias tienen cierto efecto predictivo
```

### Dashboard de Sentimiento

```
NOTICIAS DEL DÍA: 2025-11-14
═══════════════════════════════════════
📊 Distribución:
    POSITIVO: 8
    NEUTRAL:  10
    NEGATIVO: 2

📈 Sentimiento Promedio: +0.32
💹 Impacto en EUR: ALCISTA (+0.45)

🔝 Noticia más positiva:
   "ECB signals strong economic growth"
   Score: +0.81

🔻 Noticia más negativa:
   "Dollar strengthens on Fed hawkish tone"
   Score: -0.53
```

---

## 🎯 Casos de Uso Real

### 1. Detección de Cambios de Sentimiento

```
Día 1: sent_mean = -0.3  (negativo)
Día 2: sent_mean = +0.5  (positivo)  ← CAMBIO BRUSCO
Día 3: sent_mean = +0.6  (positivo)

sent_trend = +0.8  → Tendencia muy positiva

Acción: El modelo detecta cambio de sentimiento
        y ajusta predicción hacia arriba
```

### 2. Divergencia Precio-Sentimiento

```
Precio EUR/USD: Bajando (-0.5%)
Sentimiento: Muy positivo (+0.7)

Interpretación: 
  → Oportunidad de COMPRA
  → El mercado aún no refleja las buenas noticias
  → Probable rebote alcista
```

### 3. Confirmación de Señales

```
Señal Técnica: RSI<30 (sobreventa) → COMPRAR
Sentimiento: +0.65 (muy positivo)   → CONFIRMA

Señal combinada: COMPRAR con alta confianza
```

---

## ⚙️ Configuración y Mantenimiento

### Actualización de Noticias

```bash
# Ejecutar diariamente (automatizable con cron/task scheduler)
python noticias/obtener_noticias.py      # 30 segundos
python noticias/analizar_sentimiento.py  # 10 segundos
python noticias/integrar_modelo.py       # 5 segundos

# Re-entrenar modelo semanalmente
python entrenar_modelo.py  # 10-15 minutos
```

### Mejoras Futuras

1. **FinBERT**: Modelo especializado en finanzas
   ```bash
   pip install transformers torch
   # Mayor precisión, requiere más recursos
   ```

2. **Más Fuentes**: Twitter, Reddit, Bloomberg
   ```python
   # APIs de redes sociales
   # Análisis de sentimiento en tiempo real
   ```

3. **Lag Analysis**: Estudiar retraso entre noticia y efecto
   ```python
   # ¿El impacto es inmediato o tarda horas/días?
   ```

---

## 🎓 Conceptos Técnicos

### VADER Sentiment Analysis
- **Léxico-basado**: Usa diccionario de palabras con scores
- **Reglas gramaticales**: Detecta negaciones, intensificadores
- **Emojis y slang**: Entiende lenguaje informal
- **Score compound**: Normalizado entre -1 y +1

### NLP (Natural Language Processing)
- Procesamiento de texto para extraer significado
- Tokenización, stemming, análisis sintáctico
- En este proyecto: análisis de polaridad (positivo/negativo)

### Feature Engineering
- Transformar datos raw en features útiles
- Agregación temporal (promedios, tendencias)
- Creación de indicadores derivados

---

## 📝 Resumen Ejecutivo

| Aspecto | Detalle |
|---------|---------|
| **Entrada** | Noticias de Google News RSS |
| **Procesamiento** | VADER Sentiment Analysis |
| **Salida** | 5 features de sentimiento |
| **Integración** | Union con datos de precio |
| **Frecuencia** | Actualización diaria/semanal |
| **Impacto** | Mejora predicciones del modelo |
| **Ventaja** | Combina análisis técnico + fundamental |

---

## 🔧 Troubleshooting

**Problema**: "No hay noticias"
→ Verifica conexión a internet
→ Google News RSS puede tener rate limits

**Problema**: "VADER no instalado"
→ `pip install vaderSentiment`

**Problema**: "Correlación muy baja"
→ Normal: sentimiento es solo uno de muchos factores
→ Su valor es en combinación con otros indicadores

---

🚀 **El sistema ahora tiene "ojos y oídos" en el mercado!**
