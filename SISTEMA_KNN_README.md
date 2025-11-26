# 🎯 Sistema de Recomendación con K-Nearest Neighbors (KNN)

## 📋 Índice
- [¿Qué es el Sistema KNN?](#qué-es-el-sistema-knn)
- [¿Cómo Funciona?](#cómo-funciona)
- [Ventajas del KNN para Trading](#ventajas-del-knn-para-trading)
- [Instalación y Configuración](#instalación-y-configuración)
- [Uso del Sistema](#uso-del-sistema)
- [Interpretación de Resultados](#interpretación-de-resultados)
- [Comparación LSTM vs KNN](#comparación-lstm-vs-knn)
- [Optimización y Mejores Prácticas](#optimización-y-mejores-prácticas)

---

## 🤔 ¿Qué es el Sistema KNN?

El **Sistema de Recomendación basado en K-Nearest Neighbors** es un método de aprendizaje automático que encuentra **patrones históricos similares** a la situación actual del mercado y recomienda acciones basándose en lo que ocurrió en esas situaciones pasadas.

### Analogía Simple
```
Imagina que eres un médico:
1. Llega un paciente con síntomas específicos
2. Buscas en tu historial los 50 casos MÁS SIMILARES
3. Ves qué tratamiento funcionó en esos casos
4. Recomiendas el tratamiento que tuvo más éxito

El KNN hace lo mismo con el trading:
1. Analiza el mercado actual (precio, indicadores, oro, noticias)
2. Busca las 50 situaciones MÁS SIMILARES del pasado
3. Ve qué pasó después (subió, bajó, se mantuvo)
4. Recomienda la acción que tuvo más éxito en esos casos
```

---

## ⚙️ ¿Cómo Funciona?

### Proceso Paso a Paso

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUJO DEL SISTEMA KNN                        │
└─────────────────────────────────────────────────────────────────┘

1. EXTRACCIÓN DE CONTEXTO ACTUAL
   ▼
   ┌──────────────────────────────┐
   │ Precio: 1.0580               │
   │ RSI: 45                      │
   │ MA_10: 1.0575                │
   │ Oro: 2050                    │
   │ Sentimiento: +0.3            │
   │ ... (22 features totales)    │
   └──────────────────────────────┘
            │
            ▼
2. BÚSQUEDA DE PATRONES SIMILARES
   ▼
   ┌──────────────────────────────┐
   │ Buscar en 2000+ patrones     │
   │ históricos                   │
   │                              │
   │ Encontrados 50 más similares │
   │ (usando distancia euclidiana)│
   └──────────────────────────────┘
            │
            ▼
3. ANÁLISIS DE RESULTADOS PASADOS
   ▼
   ┌──────────────────────────────┐
   │ De los 50 patrones:          │
   │ • 32 → Precio SUBIÓ  (64%)   │
   │ • 12 → Precio BAJÓ   (24%)   │
   │ • 6  → Se MANTUVO    (12%)   │
   └──────────────────────────────┘
            │
            ▼
4. RECOMENDACIÓN
   ▼
   ┌──────────────────────────────┐
   │ 📈 COMPRAR                   │
   │ Confianza: 64%               │
   │ Retorno esperado: +0.15%     │
   └──────────────────────────────┘
```

### Features Analizadas

El sistema KNN analiza **hasta 27 features** (según disponibilidad):

#### 📊 Features Básicas (13)
```python
- open, high, low, close, tick_volume  # Datos OHLCV
- MA_10, MA_30, MA_50                  # Medias móviles
- RSI                                   # Relative Strength Index
- Volatility                            # Volatilidad del precio
- HL_Range                              # Rango alto-bajo
- Price_Change                          # Cambio porcentual
- Volume_MA                             # Volumen promedio
```

#### 🥇 Features de Oro (9) - Si `USAR_CORRELACION_ORO = True`
```python
- close_oro                # Precio del oro
- ratio_eur_oro            # Relación EUR/ORO
- ratio_desviacion         # Desviación de la relación
- divergencia_retornos     # Divergencia de retornos
- oro_tendencia            # Tendencia del oro
- ratio_volatilidad        # Relación de volatilidad
- correlacion              # Correlación actual
- correlacion_ma           # Media móvil de correlación
- oro_momentum             # Momentum del oro
```

#### 📰 Features de Sentimiento (5) - Si hay datos de noticias
```python
- sent_mean                # Sentimiento promedio
- impact_mean              # Impacto promedio en EUR
- sent_balance             # Balance de sentimientos
- sent_ma_24h              # Media móvil 24h del sentimiento
- sent_trend               # Tendencia del sentimiento
```

---

## ✅ Ventajas del KNN para Trading

### 1. **Explicabilidad** 🔍
```
LSTM (Red Neuronal):
❓ "El modelo predice COMPRA" 
   → No sabemos por qué (caja negra)

KNN:
✅ "Recomiendo COMPRA porque en 32 de 50 situaciones 
   similares del pasado, el precio subió"
   → Podemos ver exactamente esos 50 casos
```

### 2. **No requiere Re-entrenamiento Constante** 🔄
```
LSTM:
- Hay que re-entrenar cada semana (10-15 minutos)
- Requiere GPU para entrenamiento rápido
- Proceso complejo

KNN:
- NO requiere entrenamiento
- Solo necesita datos históricos
- Actualización instantánea
```

### 3. **Se adapta automáticamente** 🎯
```
Cuando agregas nuevos datos históricos:

LSTM:
→ Hay que re-entrenar TODO el modelo
→ Tiempo: 10-15 minutos

KNN:
→ Automáticamente usa los nuevos datos
→ Tiempo: 0 segundos
```

### 4. **Combina Múltiples Factores** 🌟
```
El KNN considera SIMULTÁNEAMENTE:
✅ Análisis técnico (precio, indicadores)
✅ Correlación con oro (mercado de materias primas)
✅ Sentimiento de noticias (análisis fundamental)

Todo en UNA SOLA recomendación
```

### 5. **Robusto contra Overfitting** 💪
```
LSTM puede "memorizar" datos de entrenamiento

KNN usa "votación democrática" de vecinos:
→ Menos propenso a sobreajuste
→ Más estable en mercados cambiantes
```

---

## 🛠️ Instalación y Configuración

### Paso 1: Instalar Dependencias
```bash
pip install scikit-learn pandas numpy
```

Ya tienes el resto instalado del sistema LSTM.

### Paso 2: Configurar en `config.py`
```python
# ═══════════════════════════════════════════════════════════════
# 🎯 SISTEMA DE RECOMENDACIÓN KNN
# ═══════════════════════════════════════════════════════════════

# Activar/Desactivar sistema KNN
USAR_KNN = True

# Número de vecinos a analizar
K_VECINOS = 50         # Recomendado: 30-100

# Horizonte de predicción (cuántas velas adelante)
HORIZONTE_KNN = 4      # H4: 16 horas, H1: 4 horas

# Peso del KNN vs LSTM (0.0 - 1.0)
PESO_KNN = 0.6         # 60% KNN, 40% LSTM
```

### Parámetros Explicados

#### `K_VECINOS` (30-100)
```
K_VECINOS = 30
→ Más específico, más volátil
→ Usa para mercados estables

K_VECINOS = 50  ← RECOMENDADO
→ Balance entre especificidad y estabilidad

K_VECINOS = 100
→ Más estable, más general
→ Usa para mercados volátiles
```

#### `HORIZONTE_KNN` (2-8)
```
HORIZONTE_KNN = 2
→ Predicción a corto plazo (8 horas en H4)

HORIZONTE_KNN = 4  ← RECOMENDADO
→ Predicción a medio plazo (16 horas en H4)

HORIZONTE_KNN = 8
→ Predicción a largo plazo (32 horas en H4)
```

#### `PESO_KNN` (0.0-1.0)
```
PESO_KNN = 0.4
→ Confiar más en LSTM (40% KNN, 60% LSTM)

PESO_KNN = 0.6  ← RECOMENDADO
→ Confiar más en KNN (60% KNN, 40% LSTM)

PESO_KNN = 1.0
→ Ignorar LSTM, solo KNN (100% KNN)
```

---

## 🚀 Uso del Sistema

### Flujo Completo

```bash
# 1. Obtener datos históricos
python extraer_datos.py

# 2. (Opcional) Obtener y analizar noticias
python noticias/obtener_noticias.py
python noticias/analizar_sentimiento.py
python noticias/integrar_modelo.py

# 3. Entrenar sistema KNN  ← NUEVO
python entrenar_knn.py

# 4. Hacer predicciones en vivo (ahora usa LSTM + KNN)
python prediccion_en_vivo.py

# 5. Generar señales para IQ Option (ahora usa LSTM + KNN)
python generar_señales_iqoption.py
```

### Uso Individual del KNN

```python
import sistema_knn
import pandas as pd

# 1. Cargar datos
df = pd.read_csv("datos/eurusd_con_oro.csv")

# 2. Crear sistema
sistema = sistema_knn.SistemaRecomendacionKNN(k_vecinos=50)

# 3. Preparar datos históricos
sistema.preparar_datos_historicos(df, horizonte_prediccion=4)

# 4. Obtener recomendación
recomendacion = sistema.obtener_recomendacion(df, explicar=True)

# 5. Mostrar resultado
sistema.mostrar_recomendacion(recomendacion)

# 6. Guardar modelo
sistema.guardar_modelo("modelos/sistema_knn.pkl")
```

### Ejemplo de Salida

```
══════════════════════════════════════════════════════════════════
🎯 RECOMENDACIÓN DEL SISTEMA KNN
══════════════════════════════════════════════════════════════════

📈 🟢 ACCIÓN RECOMENDADA: COMPRA
🎯 Confianza: 68.5%
📊 Retorno esperado: +0.152%

🔍 Análisis de 50 patrones similares:
   📈 COMPRA: 32 patrones (64.0%)
   📉 VENTA:  12 patrones (24.0%)
   ⏸️  ESPERA: 6 patrones (12.0%)

📋 Top 10 situaciones más similares del pasado:
──────────────────────────────────────────────────────────────────
   🟢 2025-11-20 14:00 | COMPRA | Retorno: +0.185% | Similitud: 0.945
   🟢 2025-11-18 10:00 | COMPRA | Retorno: +0.142% | Similitud: 0.932
   🟢 2025-11-15 22:00 | COMPRA | Retorno: +0.098% | Similitud: 0.921
   🔴 2025-11-14 18:00 | VENTA  | Retorno: -0.056% | Similitud: 0.918
   🟢 2025-11-12 14:00 | COMPRA | Retorno: +0.165% | Similitud: 0.912
   ...

💡 Interpretación:
   ✅ Confianza ALTA - Patrón muy claro en el histórico
══════════════════════════════════════════════════════════════════
```

---

## 📖 Interpretación de Resultados

### Niveles de Confianza

```
┌──────────────────────────────────────────────────────────────┐
│ CONFIANZA        SIGNIFICADO          ACCIÓN RECOMENDADA     │
├──────────────────────────────────────────────────────────────┤
│ 70-100%         MUY ALTA ✅           OPERAR con confianza   │
│ 50-70%          ALTA ⚠️               OPERAR con precaución  │
│ 30-50%          MEDIA ⏸️              CONSIDERAR esperar     │
│ 0-30%           BAJA ❌               NO OPERAR              │
└──────────────────────────────────────────────────────────────┘
```

### Interpretación de Vecinos

```
Ejemplo: 50 vecinos analizados
├─ 35 COMPRA (70%)
├─ 10 VENTA  (20%)
└─ 5  ESPERA (10%)

Interpretación:
✅ SEÑAL MUY CLARA de COMPRA
   → 70% de los casos similares resultaron en subida
   → Solo 20% resultaron en bajada
   → Confianza alta para operar
```

```
Ejemplo: 50 vecinos analizados
├─ 18 COMPRA (36%)
├─ 17 VENTA  (34%)
└─ 15 ESPERA (30%)

Interpretación:
⚠️ SEÑAL AMBIGUA
   → No hay consenso claro
   → Distribución casi uniforme
   → MEJOR ESPERAR
```

### Similitud de Patrones

```
Similitud: 0.95  → 95% similar  ✅ Muy confiable
Similitud: 0.80  → 80% similar  ⚠️ Moderadamente confiable
Similitud: 0.50  → 50% similar  ❌ Poco confiable
```

---

## ⚖️ Comparación LSTM vs KNN

| Aspecto | LSTM | KNN | LSTM + KNN |
|---------|------|-----|------------|
| **Tipo** | Red Neuronal | Vecinos Cercanos | Híbrido |
| **Explicabilidad** | ❌ Caja negra | ✅ Muy claro | ⚠️ Parcial |
| **Entrenamiento** | 10-15 min | Instantáneo | 10-15 min |
| **Re-entrenamiento** | Semanal | No necesario | Semanal (solo LSTM) |
| **Adaptabilidad** | Media | Alta | Muy Alta |
| **Precisión** | Alta | Media-Alta | **MUY ALTA** ✅ |
| **Estabilidad** | Media | Alta | **MUY ALTA** ✅ |
| **Patrones complejos** | ✅ Excelente | ⚠️ Bueno | ✅ Excelente |
| **Robustez** | Media | Alta | **Muy Alta** ✅ |

### Cuándo Usar Cada Uno

```
┌─────────────────────────────────────────────────────────────┐
│ SOLO LSTM:                                                  │
│ ✅ Mercados con patrones complejos                          │
│ ✅ Datos de alta frecuencia                                 │
│ ✅ Cuando tienes GPU para entrenar rápido                   │
├─────────────────────────────────────────────────────────────┤
│ SOLO KNN:                                                   │
│ ✅ Necesitas explicar las decisiones                        │
│ ✅ No tienes tiempo para re-entrenar                        │
│ ✅ Mercados más predecibles                                 │
├─────────────────────────────────────────────────────────────┤
│ LSTM + KNN (RECOMENDADO):                                   │
│ ✅ Mejor de ambos mundos                                    │
│ ✅ Mayor precisión y estabilidad                            │
│ ✅ Confirmación cruzada de señales                          │
│ ✅ Reducción de falsos positivos                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎓 Optimización y Mejores Prácticas

### 1. Ajuste de K_VECINOS

```python
# Probar diferentes valores
for k in [30, 50, 75, 100]:
    sistema = SistemaRecomendacionKNN(k_vecinos=k)
    sistema.preparar_datos_historicos(df)
    metricas = sistema.evaluar_rendimiento()
    print(f"K={k}: Accuracy={metricas['accuracy']:.2f}%")

# Elegir el K con mejor accuracy
```

### 2. Actualización de Datos

```bash
# Re-entrenar KNN semanalmente
# (Mucho más rápido que LSTM)

# Lunes 8 AM:
python extraer_datos.py        # 2 minutos
python entrenar_knn.py         # 1 minuto
# Total: 3 minutos ✅

# vs LSTM:
python entrenar_modelo.py      # 15 minutos ⏰
```

### 3. Combinar con Análisis Manual

```
Recomendación KNN: COMPRA (confianza 65%)
    ├─ Ver top 10 patrones similares
    ├─ Revisar qué pasó en esos casos
    ├─ Validar con análisis técnico manual
    └─ Tomar decisión informada
```

### 4. Backtesting

```python
# Evaluar en diferentes periodos
sistema.evaluar_rendimiento(ventana_test=100)  # Último mes
sistema.evaluar_rendimiento(ventana_test=500)  # Últimos 3 meses
sistema.evaluar_rendimiento(ventana_test=1000) # Últimos 6 meses

# Comparar resultados en diferentes condiciones de mercado
```

---

## 🔧 Troubleshooting

### Error: "Sistema KNN no entrenado"
```bash
# Solución:
python entrenar_knn.py
```

### Error: "Se necesitan al menos 500 registros"
```bash
# Solución: Descargar más datos
# En config.py:
CANTIDAD_DATOS = 3000  # Aumentar

# Luego:
python extraer_datos.py
python entrenar_knn.py
```

### Confianza muy baja (< 40%)
```
Posibles causas:
1. Mercado en situación inédita (sin patrones similares)
2. K_VECINOS muy bajo (aumentar a 75-100)
3. Datos insuficientes (aumentar CANTIDAD_DATOS)

Solución:
→ En estos casos, ESPERAR es la mejor opción
```

---

## 📚 Referencias y Recursos

### Documentación Interna
- `sistema_knn.py` - Código fuente del sistema
- `entrenar_knn.py` - Script de entrenamiento
- `config.py` - Configuración de parámetros

### Aprendizaje Adicional
- [K-Nearest Neighbors (Wikipedia)](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm)
- [scikit-learn KNN Documentation](https://scikit-learn.org/stable/modules/neighbors.html)

---

## 💡 Consejos Finales

1. **Empieza con configuración por defecto** (K=50, Horizonte=4)
2. **Monitorea el accuracy** en evaluaciones semanales
3. **Combina siempre con LSTM** para mejores resultados
4. **No operes si confianza < 50%** 
5. **Re-entrena el KNN semanalmente** (solo toma 1 minuto)
6. **Revisa los top 10 patrones** antes de operar
7. **Usa gestión de riesgo** (Stop Loss siempre activo)

---

**✅ SISTEMA KNN IMPLEMENTADO Y DOCUMENTADO**

🎯 El sistema está listo para generar recomendaciones basadas en patrones históricos exitosos.
