# 🤖 MonedaPredict - Sistema Integral de Trading con IA

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Sistema de trading automatizado con 3 módulos de inteligencia artificial para predicción de divisas EUR/USD**

---

## 🎯 Descripción

MonedaPredict es un sistema completo de trading que combina **tres tecnologías de inteligencia artificial** diferentes para generar señales de trading precisas y confiables:

### 🧠 Tecnologías Implementadas

1. **📊 LSTM (Long Short-Term Memory)**
   - Redes neuronales recurrentes para análisis de series temporales
   - Predice tendencias basándose en patrones históricos complejos
   - Precisión: ~65-70% en validación

2. **🎯 KNN (K-Nearest Neighbors)**
   - Sistema de recomendación por similitud de patrones
   - Encuentra los 50 patrones históricos más parecidos
   - Explicable: muestra por qué recomienda cada acción
   - Precisión: ~51% con +7% ganancia simulada

3. **📰 Análisis de Sentimientos**
   - NLP con VADER Sentiment sobre noticias financieras
   - 4 fuentes: Google News, Investing.com, FXStreet, ForexLive
   - Actualización automática cada 30 minutos
   - Detecta eventos ECB, Fed, datos económicos

### 🔥 Sistema Híbrido

La combinación de los 3 sistemas genera señales más robustas:
- **Ponderación:** 60% KNN + 40% LSTM
- **Confirmación:** Sentimientos como factor validador
- **Resultado:** Mayor confianza y precisión en las predicciones

---

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.8 o superior
- MetaTrader 5 (para datos históricos)
- Cuenta en IQ Option (para ejecutar señales)

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/aresCharcaC/MonedaPredict.git
cd MonedaPredict

# Instalar dependencias principales
pip install -r requirements.txt

# Instalar dependencias del sistema de sentimientos
cd "Sistema de rsentimientos"
pip install -r requirements.txt
cd ..
```

### Ejecutar el Sistema

```bash
python ejecutar.py
```

El ejecutor principal te mostrará un menú interactivo para elegir entre los 4 sistemas.

---

## 📋 Estructura del Proyecto

```
MonedaPredict/
│
├── ejecutar.py                          # ⭐ EJECUTOR PRINCIPAL
├── config.py                            # Configuración global
├── GUIA_RAPIDA.md                       # Guía de uso rápido
│
├── 📊 Sistema LSTM
│   ├── extraer_datos.py                 # Descarga datos de MT5
│   ├── entrenar_modelo.py               # Entrena red neuronal LSTM
│   ├── prediccion_en_vivo.py            # Predicción en tiempo real
│   ├── generar_señales_iqoption.py      # Genera señales para IQ Option
│   └── visualizar_resultados.py         # Gráficos y métricas
│
├── 🎯 Sistema KNN
│   ├── sistema_knn.py                   # Clase principal del KNN
│   ├── entrenar_knn.py                  # Entrenamiento del KNN
│   ├── SISTEMA_KNN_README.md            # Documentación KNN
│   └── RESUMEN_SISTEMA_KNN.txt          # Resumen técnico
│
├── 📰 Sistema de Sentimientos
│   ├── config_sentimientos.py           # Configuración sentimientos
│   ├── recolector_noticias.py          # Obtiene noticias RSS
│   ├── analizador_sentimientos.py      # Análisis NLP
│   ├── generador_señales_sentimientos.py
│   ├── monitor_sentimientos.py         # Monitor continuo
│   ├── visualizador_sentimientos.py    # Dashboard
│   ├── README.md                       # Documentación completa
│   ├── INSTALACION.md                  # Guía de instalación
│   ├── PRUEBAS_SISTEMA.md              # Resultados de pruebas
│   └── requirements.txt                # Dependencias
│
├── datos/                              # Datos históricos
│   ├── eurusd_datos.csv
│   └── eurusd_con_oro.csv
│
├── modelos/                            # Modelos entrenados
│   ├── lstm_model.h5
│   └── sistema_knn.pkl
│
├── registros/                          # Señales generadas
│   └── señales_iqoption.csv
│
└── noticias/                           # Módulo noticias (legacy)
    ├── obtener_noticias.py
    ├── analizar_sentimiento.py
    └── integrar_modelo.py
```

---

## 🎮 Uso del Sistema

### Opción 1: Ejecutor Interactivo (Recomendado)

```bash
python ejecutar.py
```

Navegarás por menús interactivos para:
- Elegir sistema (LSTM, KNN, Sentimientos o Híbrido)
- Entrenar modelos
- Generar predicciones
- Visualizar resultados

### Opción 2: Comandos Directos

#### Sistema LSTM
```bash
# Descargar datos
python extraer_datos.py

# Entrenar modelo
python entrenar_modelo.py

# Predicción en vivo
python prediccion_en_vivo.py

# Generar señales IQ Option
python generar_señales_iqoption.py
```

#### Sistema KNN
```bash
# Entrenar KNN
python entrenar_knn.py

# Predicción con KNN (integrado en prediccion_en_vivo.py)
python prediccion_en_vivo.py
```

#### Sistema de Sentimientos
```bash
cd "Sistema de rsentimientos"

# Análisis único
python monitor_sentimientos.py --once

# Monitor continuo
python monitor_sentimientos.py

# Dashboard
python visualizador_sentimientos.py --dias 7
```

---

## ⚙️ Configuración

### Configuración Global (`config.py`)

```python
# Par de divisas
PAR_DIVISAS = "EURUSD"
TIMEFRAME = mt5.TIMEFRAME_H4

# Parámetros de trading
TAKE_PROFIT_PIPS = 80
STOP_LOSS_PIPS = 40
CONFIANZA_MINIMA = 60

# Sistema KNN
USAR_KNN = True
K_VECINOS = 50
HORIZONTE_KNN = 4
PESO_KNN = 0.6  # 60% KNN, 40% LSTM

# Correlación con Oro
USAR_CORRELACION_ORO = True
```

### Configuración de Sentimientos (`Sistema de rsentimientos/config_sentimientos.py`)

```python
# Fuentes de noticias
USAR_GOOGLE_NEWS = True
USAR_INVESTING = True
USAR_FXSTREET = True
USAR_FOREXLIVE = True

# Parámetros de análisis
CONFIANZA_MINIMA_COMPRA = 60
NOTICIAS_MINIMAS = 10
INTERVALO_ACTUALIZACION = 30  # minutos
```

---

## 📊 Resultados y Rendimiento

### Sistema LSTM
- **Precisión en validación:** ~65-70%
- **Arquitectura:** 3 capas LSTM (100, 50, 25 unidades)
- **Features:** 13 indicadores técnicos + 9 correlación oro

### Sistema KNN
- **Precisión en test:** 51%
- **Ganancia simulada:** +7.051%
- **Patrones analizados:** 1,726
- **Vecinos:** 50 (configurable)

### Sistema de Sentimientos
- **Fuentes activas:** 4
- **Noticias analizadas:** Variable según horario
- **Horizonte:** Corto (4h), Medio (12h), Largo (24h)
- **Ponderación:** Por antigüedad, fuente y tipo de evento

### Sistema Híbrido
- **Combinación:** 60% KNN + 40% LSTM + Sentimientos
- **Ventaja:** Mayor confianza en señales coincidentes
- **Señal fuerte:** Cuando los 3 sistemas coinciden

---

## 📈 Señales Generadas

El sistema genera 3 tipos de señales:

### 📈 COMPRA (Largo)
- EUR sube vs USD
- Confianza > 60%
- Take Profit: 80 pips
- Stop Loss: 40 pips

### 📉 VENTA (Corto)
- EUR baja vs USD
- Confianza > 60%
- Take Profit: 80 pips
- Stop Loss: 40 pips

### ⏸️ ESPERA
- No hay señal clara
- Confianza < 60%
- Esperar mejor oportunidad

---

## 🛠️ Tecnologías Utilizadas

### Core
- **Python 3.8+**
- **TensorFlow 2.x** - LSTM
- **scikit-learn** - KNN, preprocessing
- **pandas** - Manipulación de datos
- **numpy** - Operaciones numéricas

### Trading
- **MetaTrader5** - Datos históricos
- **ta-lib** - Indicadores técnicos

### NLP y Sentimientos
- **vaderSentiment** - Análisis de sentimiento
- **BeautifulSoup4** - Parsing RSS
- **requests** - HTTP

### Visualización
- **matplotlib** - Gráficos
- **seaborn** - Visualización estadística

---

## 📚 Documentación Completa

- **[GUIA_RAPIDA.md](GUIA_RAPIDA.md)** - Guía de uso paso a paso
- **[SISTEMA_KNN_README.md](SISTEMA_KNN_README.md)** - Documentación KNN
- **[Sistema de rsentimientos/README.md](Sistema%20de%20rsentimientos/README.md)** - Sistema de sentimientos
- **[Sistema de rsentimientos/PRUEBAS_SISTEMA.md](Sistema%20de%20rsentimientos/PRUEBAS_SISTEMA.md)** - Resultados de pruebas

---

## 🧪 Testing

### Probar Sistema LSTM
```bash
python entrenar_modelo.py
python prediccion_en_vivo.py
```

### Probar Sistema KNN
```bash
python entrenar_knn.py
```

### Probar Sistema de Sentimientos
```bash
cd "Sistema de rsentimientos"
python monitor_sentimientos.py --once
```

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## ⚠️ Disclaimer

**IMPORTANTE:** Este sistema es para fines educativos y de investigación. El trading de divisas conlleva riesgos significativos. NO se garantizan ganancias. Siempre:

- ✅ Prueba en cuenta DEMO primero
- ✅ Nunca inviertas más de lo que puedes perder
- ✅ Usa gestión de riesgo adecuada
- ✅ Las señales son sugerencias, no garantías
- ✅ Consulta con un asesor financiero profesional

Los desarrolladores NO se responsabilizan por pérdidas financieras.

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

**aresCharcaC**
- GitHub: [@aresCharcaC](https://github.com/aresCharcaC)
- Proyecto: MonedaPredict
- Rama actual: `Recomendacion`

---

## 🎓 Proyecto Académico

Este sistema fue desarrollado como proyecto de **Minería de Datos** aplicada al trading financiero, combinando técnicas de:
- Deep Learning (LSTM)
- Machine Learning (KNN)
- Natural Language Processing (Análisis de sentimientos)
- Análisis de series temporales
- Feature Engineering

---

## 📅 Historial de Versiones

### v3.0 (Diciembre 2025) - Sistema Integral
- ✅ Sistema de Sentimientos independiente
- ✅ Ejecutor unificado con menús
- ✅ Dashboard integrado
- ✅ Documentación completa

### v2.0 (Noviembre 2025) - Sistema KNN
- ✅ Implementación KNN
- ✅ Sistema híbrido LSTM+KNN
- ✅ Correlación con oro

### v1.0 (Octubre 2025) - Sistema Base
- ✅ Red LSTM básica
- ✅ Integración MetaTrader5
- ✅ Generación de señales

---

## 🙏 Agradecimientos

- MetaTrader 5 por la API de datos
- TensorFlow y scikit-learn por las bibliotecas de ML
- Fuentes de noticias: Google News, Investing.com, FXStreet, ForexLive

---

## 📞 Soporte

Si tienes preguntas o problemas:
1. Revisa la [GUIA_RAPIDA.md](GUIA_RAPIDA.md)
2. Consulta la documentación específica de cada sistema
3. Abre un Issue en GitHub

---

**🚀 ¡Happy Trading!**

