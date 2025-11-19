# 📰 Módulo de Análisis de Noticias

## 🎯 Objetivo
Agregar inteligencia de noticias al modelo de predicción EUR/USD mediante análisis de sentimiento.

## 🏗️ Estructura

```
noticias/
├── obtener_noticias.py      # Descarga noticias de Google News RSS
├── analizar_sentimiento.py  # Análisis con VADER Sentiment
├── integrar_modelo.py        # Integra features con datos de precio
└── README.md                 # Esta documentación
```

## 🚀 Cómo Usar

### Paso 1: Instalar Dependencias
```bash
pip install vaderSentiment beautifulsoup4 lxml requests
```

### Paso 2: Obtener Noticias
```bash
python noticias/obtener_noticias.py
```
- Descarga noticias de Google News RSS (gratis, sin API key)
- Guarda en: `datos/noticias_raw.csv`

### Paso 3: Analizar Sentimiento
```bash
python noticias/analizar_sentimiento.py
```
- Analiza sentimiento con VADER
- Clasifica: POSITIVO, NEGATIVO, NEUTRAL
- Interpreta impacto en EUR/USD
- Guarda en: `datos/noticias_sentimiento.csv`

### Paso 4: Integrar con Modelo
```bash
python noticias/integrar_modelo.py
```
- Une noticias con datos de precio
- Crea features: `sent_mean`, `impact_mean`, `sent_balance`
- Guarda en: `datos/eurusd_con_sentimiento.csv`

## 📊 Features Generadas

| Feature | Descripción |
|---------|-------------|
| `sent_mean` | Sentimiento promedio diario (-1 a 1) |
| `sent_std` | Volatilidad del sentimiento |
| `impact_mean` | Impacto promedio en EUR/USD |
| `sent_balance` | Balance noticias positivas - negativas |
| `sent_ma_24h` | Media móvil sentimiento 24h |
| `sent_trend` | Tendencia del sentimiento |

## 🔧 Tecnologías

- **VADER Sentiment**: Análisis de sentimiento sin entrenamiento
- **Google News RSS**: Fuente de noticias gratuita
- **BeautifulSoup**: Parseo de XML/RSS
- **Pandas**: Procesamiento de datos

## 📈 Para Escalar Después

### Opción 1: NewsAPI (100 requests/día gratis)
- Regístrate en: https://newsapi.org/
- Descomentar método en `obtener_noticias.py`

### Opción 2: FinBERT (Modelo especializado)
```bash
pip install transformers torch
```
- Mejor precisión en noticias financieras
- Requiere más recursos computacionales

## 🎓 Interpretación

### Sentimiento Compound (VADER)
- **> 0.05**: POSITIVO
- **< -0.05**: NEGATIVO
- **-0.05 a 0.05**: NEUTRAL

### Impacto en EUR/USD
- **+1**: Favorece al EUR (EUR sube)
- **-1**: Favorece al USD (EUR baja)
- **0**: Neutral

## ⚠️ Consideraciones

1. **Correlación no es causalidad**: Las noticias pueden no tener impacto inmediato
2. **Latencia**: Hay delay entre noticia y reacción del mercado
3. **Contexto**: El mismo sentimiento puede tener efectos diferentes según contexto económico
4. **Calidad**: Google News RSS es bueno para empezar, pero fuentes especializadas son mejores

## 🔄 Integración con LSTM

Para usar las features en el modelo, modifica `entrenar_modelo.py`:

```python
# En lugar de solo usar precios OHLCV
features = ['open', 'high', 'low', 'close', 'volume', 
            'sent_mean', 'impact_mean', 'sent_balance']  # ← Agregar estas

# Cargar datos integrados
df = pd.read_csv('datos/eurusd_con_sentimiento.csv')
```

## 📝 Próximos Pasos

1. ✅ Implementación básica con VADER
2. ⏳ Agregar más fuentes de noticias
3. ⏳ Implementar FinBERT para mayor precisión
4. ⏳ Análisis de correlación temporal (lag analysis)
5. ⏳ Dashboard de visualización de sentimiento
