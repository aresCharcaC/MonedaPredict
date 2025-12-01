# 🚀 GUÍA RÁPIDA - SISTEMA INTEGRAL DE TRADING

**Fecha de actualización:** 1 Diciembre 2025

---

## 📋 INICIO RÁPIDO

### Ejecutar el sistema:
```bash
python ejecutar.py
```

---

## 🎯 SISTEMAS DISPONIBLES

El ejecutor principal integra **3 sistemas de inteligencia artificial** que puedes usar de forma individual o combinada:

### 1️⃣ 📊 Sistema LSTM (Redes Neuronales)
**¿Qué hace?** Predice tendencias usando redes neuronales profundas entrenadas con datos históricos.

**Opciones disponibles:**
- Ver configuración LSTM
- Descargar datos de MT5
- Entrenar modelo LSTM
- Predicción en vivo (LSTM)
- Generar señales IQ Option
- Visualizar resultados
- Proceso completo automatizado

**Cuándo usarlo:** Para análisis técnico basado en patrones históricos complejos.

---

### 2️⃣ 🎯 Sistema KNN (Recomendación por Patrones)
**¿Qué hace?** Encuentra los 50 patrones históricos más similares a la situación actual y recomienda la mejor acción.

**Opciones disponibles:**
- Ver configuración KNN
- Entrenar sistema KNN
- Predicción en vivo (KNN)
- Evaluar rendimiento KNN
- Ver reportes de entrenamiento

**Cuándo usarlo:** Para decisiones basadas en "vecinos cercanos" que tuvieron éxito en el pasado.

**Ventajas:**
- Explicable (muestra los patrones similares)
- Rápido de entrenar
- No requiere GPU

---

### 3️⃣ 📰 Sistema de Sentimientos (Análisis de Noticias)
**¿Qué hace?** Analiza noticias financieras de 4 fuentes (Google News, Investing.com, FXStreet, ForexLive) usando NLP y VADER Sentiment.

**Opciones disponibles:**
- Ver configuración Sentimientos
- Recolectar noticias (una vez)
- Analizar sentimientos
- Generar señal de sentimiento
- Monitor continuo (actualización cada 30 min)
- Visualizar dashboard
- Generar reporte completo

**Cuándo usarlo:** Para trading basado en noticias fundamentales y sentimiento del mercado.

**Características:**
- 4 fuentes de noticias RSS
- Análisis NLP con VADER
- Ponderación por antigüedad, fuente y tipo de evento
- 3 horizontes: corto (4h), medio (12h), largo plazo (24h)
- Alertas automáticas de cambios

---

### 4️⃣ 🔥 Sistema Híbrido (LSTM + KNN + Sentimientos)
**¿Qué hace?** Combina los 3 sistemas para generar señales más robustas y confiables.

**Opciones disponibles:**
- Ver configuración híbrida
- Predicción híbrida en vivo
- Generar señales combinadas
- Comparar sistemas
- Dashboard unificado

**Cuándo usarlo:** Para máxima precisión combinando análisis técnico, patrones y sentimiento.

**Ponderación actual:**
- KNN: 60%
- LSTM: 40%
- Sentimientos: Factor confirmatorio

---

## 📖 FLUJOS DE TRABAJO RECOMENDADOS

### 🔰 Para Principiantes - Proceso Completo LSTM

1. Ejecuta `python ejecutar.py`
2. Selecciona `1` (Sistema LSTM)
3. Selecciona `7` (Proceso completo)
4. El sistema hará todo automáticamente:
   - Descarga datos de MT5
   - Entrena el modelo
   - Genera señales en vivo

### 🎯 Para Traders Experimentados - Sistema Híbrido

1. Ejecuta `python ejecutar.py`
2. Selecciona `4` (Sistema Híbrido)
3. Selecciona `2` (Predicción híbrida en vivo)
4. Observa las señales combinadas con mayor confianza

### 📰 Para Trading de Noticias - Sistema de Sentimientos

1. Ejecuta `python ejecutar.py`
2. Selecciona `3` (Sistema de Sentimientos)
3. Selecciona `5` (Monitor continuo)
4. El sistema analizará noticias cada 30 minutos y te alertará

---

## 🎨 NAVEGACIÓN POR MENÚS

### Menú Principal
```
🎯 SELECCIONA EL SISTEMA DE TRADING
1️⃣  📊 Sistema LSTM
2️⃣  🎯 Sistema KNN
3️⃣  📰 Sistema de Sentimientos
4️⃣  🔥 Sistema Híbrido
5️⃣  ⚙️  Configuración Global
0️⃣  ❌ Salir
```

### Menú LSTM
```
📊 SISTEMA LSTM - REDES NEURONALES
1️⃣  Ver configuración LSTM
2️⃣  Descargar datos de MT5
3️⃣  Entrenar modelo LSTM
4️⃣  Predicción en vivo (LSTM)
5️⃣  Generar señales IQ Option
6️⃣  Visualizar resultados
7️⃣  Proceso completo (2 → 3 → 4)
0️⃣  ← Volver
```

### Menú KNN
```
🎯 SISTEMA KNN - RECOMENDACIÓN POR PATRONES
1️⃣  Ver configuración KNN
2️⃣  Entrenar sistema KNN
3️⃣  Predicción en vivo (KNN)
4️⃣  Evaluar rendimiento KNN
5️⃣  Ver reportes de entrenamiento
0️⃣  ← Volver
```

### Menú Sentimientos
```
📰 SISTEMA DE SENTIMIENTOS - ANÁLISIS DE NOTICIAS
1️⃣  Ver configuración Sentimientos
2️⃣  Recolectar noticias (una vez)
3️⃣  Analizar sentimientos
4️⃣  Generar señal de sentimiento
5️⃣  Monitor continuo (actualización cada 30 min)
6️⃣  Visualizar dashboard
7️⃣  Generar reporte completo
0️⃣  ← Volver
```

### Menú Híbrido
```
🔥 SISTEMA HÍBRIDO - LSTM + KNN + SENTIMIENTOS
1️⃣  Ver configuración híbrida
2️⃣  Predicción híbrida en vivo
3️⃣  Generar señales combinadas
4️⃣  Comparar sistemas
5️⃣  Dashboard unificado
0️⃣  ← Volver
```

---

## 📁 ESTRUCTURA DE ARCHIVOS GENERADOS

```
MonedaPredict/
│
├── datos/
│   ├── eurusd_datos.csv          # Datos históricos EUR/USD
│   └── eurusd_con_oro.csv        # Datos con correlación oro
│
├── modelos/
│   ├── lstm_model.h5             # Modelo LSTM entrenado
│   └── sistema_knn.pkl           # Sistema KNN entrenado
│
├── registros/
│   ├── señales_iqoption.csv      # Señales para IQ Option
│   └── reporte_entrenamiento_knn_*.txt
│
├── Sistema de rsentimientos/
│   ├── datos_sentimientos/
│   │   ├── noticias_raw.csv
│   │   ├── noticias_analizadas.csv
│   │   └── señales_sentimiento.csv
│   └── reportes/
│       └── reporte_*.txt
│
└── ejecutar.py                   # ⭐ EJECUTOR PRINCIPAL
```

---

## 🛠️ CONFIGURACIÓN

### Cambiar parámetros globales:

Edita `config.py`:
```python
PAR_DIVISAS = "EURUSD"           # Par a operar
TIMEFRAME = mt5.TIMEFRAME_H4     # Temporalidad
USAR_KNN = True                  # Activar/desactivar KNN
K_VECINOS = 50                   # Número de vecinos
PESO_KNN = 0.6                   # Peso KNN vs LSTM
```

### Cambiar parámetros de Sentimientos:

Edita `Sistema de rsentimientos/config_sentimientos.py`:
```python
INTERVALO_ACTUALIZACION = 30     # Minutos entre actualizaciones
CONFIANZA_MINIMA_COMPRA = 60     # % mínimo para COMPRA
NOTICIAS_MINIMAS = 10            # Mínimo de noticias para señal
```

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### ❌ Error: "No se encuentra config.py"
**Solución:** Asegúrate de ejecutar `python ejecutar.py` desde la carpeta raíz del proyecto.

### ❌ Error en Sistema de Sentimientos
**Solución:** Instala las dependencias:
```bash
cd "Sistema de rsentimientos"
pip install -r requirements.txt
cd ..
```

### ❌ MetaTrader5 no conecta
**Solución:** 
1. Abre MT5 manualmente
2. Inicia sesión en tu cuenta
3. Vuelve a intentar

### ❌ Pocas noticias recolectadas
**Solución:** Es normal en fines de semana. Las fuentes tienen menos noticias. El sistema generará señal ESPERA si no hay suficientes datos.

---

## 💡 TIPS Y MEJORES PRÁCTICAS

### ✅ Recomendaciones generales:
1. **Entrena con datos actualizados:** Descarga datos frescos antes de entrenar
2. **Combina sistemas:** El híbrido tiene mejor precisión
3. **Monitorea sentimientos:** Úsalo para confirmar señales técnicas
4. **Revisa reportes:** Los reportes KNN muestran exactamente por qué se toma cada decisión

### ✅ Para trading en vivo:
1. **Empieza con demo:** Prueba primero en cuenta demo de IQ Option
2. **Valida señales:** No operes ciegamente, usa tu criterio
3. **Gestión de riesgo:** Respeta siempre el stop loss
4. **Horarios:** El sistema de sentimientos funciona mejor en horario de mercado europeo/americano

### ✅ Optimización:
1. **KNN:** Ajusta K_VECINOS (50 por defecto) según tu estilo
2. **Sentimientos:** Reduce INTERVALO_ACTUALIZACION a 15 min en sesiones activas
3. **LSTM:** Reentrena semanalmente con datos frescos

---

## 📊 INTERPRETACIÓN DE SEÑALES

### Sistema LSTM/KNN
```
🎯 SEÑAL: COMPRA
📊 Confianza LSTM: 75%
🎯 Confianza KNN: 82%
💰 Confianza combinada: 79%
```
- **COMPRA:** Entrar largo (EUR sube vs USD)
- **VENTA:** Entrar corto (EUR baja vs USD)
- **ESPERA:** No hay señal clara, esperar

### Sistema de Sentimientos
```
⏸️  ⚪ SEÑAL PRINCIPAL: ESPERA
   Confianza:   65%
   Urgencia:    🔴 ALTA
   Total noticias: 25
```
- **Urgencia ALTA:** Los 3 horizontes coinciden
- **Urgencia MEDIA:** 2 de 3 horizontes coinciden
- **Urgencia BAJA:** Sin consenso claro

---

## 🎓 RECURSOS ADICIONALES

### Documentación específica:
- **LSTM:** `entrenar_modelo.py` - Comentarios en el código
- **KNN:** `SISTEMA_KNN_README.md` - Documentación completa
- **Sentimientos:** `Sistema de rsentimientos/README.md`

### Reportes generados:
- **KNN:** `registros/reporte_entrenamiento_knn_*.txt`
- **Sentimientos:** `Sistema de rsentimientos/reportes/`

---

## ⚡ COMANDOS RÁPIDOS

```bash
# Iniciar sistema completo
python ejecutar.py

# Solo LSTM (desde raíz)
python prediccion_en_vivo.py

# Solo KNN (entrenar)
python entrenar_knn.py

# Solo Sentimientos (monitor)
cd "Sistema de rsentimientos"
python monitor_sentimientos.py

# Generar señales IQ Option
python generar_señales_iqoption.py
```

---

## 🏆 VENTAJAS DEL SISTEMA INTEGRADO

✅ **Flexibilidad:** Usa uno, dos o los 3 sistemas
✅ **Explicabilidad:** KNN muestra patrones similares
✅ **Fundamentos:** Sentimientos analiza noticias reales
✅ **Precisión:** La combinación mejora la confianza
✅ **Automatización:** Proceso completo en 1 clic
✅ **Reportes:** Documentación detallada de cada decisión

---

## 📞 SOPORTE

Si encuentras problemas:
1. Revisa `PRUEBAS_SISTEMA.md` en cada carpeta
2. Verifica la configuración con opción `5` del menú
3. Revisa los logs en consola

---

**¡Listo para operar! 🚀**

Sistema desarrollado: Diciembre 2025
Versión: 3.0 (LSTM + KNN + Sentimientos)
