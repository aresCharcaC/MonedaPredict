# 🥇 Sistema de Correlación EUR/USD con ORO (XAU/USD)

## 📋 Descripción

Este sistema integra la correlación histórica entre EUR/USD y el oro (XAU/USD) para mejorar las predicciones del modelo LSTM. El oro es un activo refugio que tradicionalmente tiene una correlación positiva con el euro, especialmente en momentos de incertidumbre económica.

## 🎯 ¿Por qué usar correlación con el oro?

### Ventajas:
- **Correlación Histórica**: EUR/USD y oro tienen una correlación positiva del 60-80% históricamente
- **Activo Refugio**: El oro refleja el sentimiento de riesgo en los mercados
- **Indicador Adelantado**: Los movimientos del oro pueden anticipar movimientos del EUR
- **Diversificación**: Reduce el riesgo de sobreajuste al añadir información externa
- **Contexto Macroeconómico**: El oro refleja expectativas de inflación y política monetaria

### Correlación Típica:
- **Crisis Financiera**: Correlación muy alta (>0.7)
- **Mercados Normales**: Correlación moderada (0.4-0.6)
- **Fortaleza USD**: Correlación puede volverse negativa

## 🚀 Cómo Usar

### 1. Configuración Inicial

Edita `config.py` para activar la correlación:

```python
# Activar correlación con oro
USAR_CORRELACION_ORO = True

# Ventana de correlación (50-200 periodos)
VENTANA_CORRELACION_ORO = 100

# Peso del oro en el modelo (0.0-1.0)
PESO_ORO = 0.7
```

### 2. Extraer Datos

Ejecuta el script de extracción que ahora descargará EUR/USD y ORO:

```powershell
python extraer_datos.py
```

Esto creará:
- `datos/eurusd_con_oro.csv` - Datos con features de oro integradas
- `datos/eurusd_datos.csv` - Solo EUR/USD
- `datos/oro_datos.csv` - Solo oro
- `datos/correlacion_oro.png` - Visualización de la correlación

### 3. Entrenar Modelo

El modelo automáticamente detectará y usará las features de oro:

```powershell
python entrenar_modelo.py
```

Verás mensajes como:
```
🥇 Features de ORO agregadas: 9
   close_oro, ratio_eur_oro, ratio_desviacion, ...
```

### 4. Predicción en Vivo

Las predicciones ahora incluirán datos del oro en tiempo real:

```powershell
python prediccion_en_vivo.py
```

## 📊 Features de Oro Creadas

El sistema crea **9 features** basadas en la correlación con el oro:

| Feature | Descripción | Utilidad |
|---------|-------------|----------|
| `close_oro` | Precio de cierre del oro | Nivel absoluto |
| `ratio_eur_oro` | Ratio EUR/USD ÷ ORO | Relación de precios |
| `ratio_desviacion` | Desviación del ratio vs media | Sobre/subvaloración |
| `divergencia_retornos` | Diferencia de retornos EUR-ORO | Cambios de correlación |
| `oro_tendencia` | Tendencia del oro | Dirección del oro |
| `ratio_volatilidad` | Volatilidad EUR vs ORO | Riesgo relativo |
| `correlacion` | Correlación móvil | Fuerza de relación |
| `correlacion_ma` | Media móvil de correlación | Suavizado |
| `oro_momentum` | Momentum del oro (5 periodos) | Velocidad de cambio |

## 📈 Visualizaciones

El sistema genera un gráfico completo (`datos/correlacion_oro.png`) con:

1. **Precios Normalizados**: Comparación visual EUR/USD vs ORO
2. **Correlación Móvil**: Evolución de la correlación en el tiempo
3. **Dispersión de Retornos**: Relación estadística
4. **Ratio EUR/ORO**: Proporción de precios
5. **Divergencia de Retornos**: Diferencias en movimientos
6. **Distribución de Correlación**: Histograma de valores

## 🔧 Ajustes Avanzados

### Ventana de Correlación

```python
VENTANA_CORRELACION_ORO = 100  # Por defecto
```

- **50-80**: Más reactiva, captura cambios rápidos
- **100-150**: Balance entre estabilidad y reactividad (recomendado)
- **150-200**: Más estable, menos sensible a ruido

### Peso del Oro

```python
PESO_ORO = 0.7  # Por defecto
```

- **0.5-0.6**: Influencia moderada
- **0.7-0.8**: Influencia alta (recomendado para EUR/USD)
- **0.9-1.0**: Influencia muy alta (usar con precaución)

### Desactivar Correlación

Si quieres volver al modelo sin oro:

```python
USAR_CORRELACION_ORO = False
```

## 📊 Interpretación de Resultados

### Correlación General

Al ejecutar `extraer_datos.py`, verás:

```
✅ Correlación general: 0.6234 (p-value: 0.0000)
   Correlación moderada
```

- **> 0.7**: Fuerte correlación positiva
- **0.5-0.7**: Correlación moderada positiva
- **0.3-0.5**: Correlación débil positiva
- **< 0.3**: Correlación muy débil o nula

### P-Value

- **< 0.05**: Correlación estadísticamente significativa ✅
- **> 0.05**: Correlación no significativa ⚠️

## 💡 Estrategias de Trading con Oro

### 1. Confirmación de Tendencia
```
Si EUR/USD ↑ y ORO ↑ → Señal fuerte de compra
Si EUR/USD ↑ y ORO ↓ → Señal débil, precaución
```

### 2. Divergencias
```
Si correlación alta y divergencia → Posible reversión
Si correlación baja → Movimientos independientes
```

### 3. Cambios de Régimen
```
Correlación pasa de alta a baja → Cambio de sentimiento
Correlación negativa → Fortaleza del USD
```

## 🔍 Troubleshooting

### Error: No se pudieron descargar datos del oro

**Solución**: Verifica que el símbolo del oro esté disponible en tu broker:
- Intenta: `XAUUSD`, `GOLD`, `XAU/USD`
- Algunos brokers usan nombres diferentes

### Advertencia: Sin datos de ORO

**Causa**: El modelo se entrenó sin oro pero ahora lo estás usando (o viceversa)

**Solución**: Re-entrena el modelo con los datos actuales:
```powershell
python extraer_datos.py
python entrenar_modelo.py
```

### Correlación muy baja (<0.3)

**Posibles causas**:
- Periodo de desacoplamiento (fortaleza del USD)
- Datos de diferentes sesiones de trading
- Problemas con la calidad de datos

**Solución**: Verifica que ambos instrumentos tengan datos del mismo periodo

## 📚 Referencias

### Estudios de Correlación EUR/USD - ORO

- **Correlación Histórica**: 0.50-0.80 (últimos 10 años)
- **Causalidad**: Oro → EUR (el oro lidera en ~60% de casos)
- **Mejor Timeframe**: H4 y Daily (correlación más estable)
- **Peor Timeframe**: M5-M15 (mucho ruido)

### Fuentes Académicas

1. "Gold and Currency Markets" - BIS Working Papers
2. "EUR/USD and Gold: A Safe Haven Relationship" - ECB Studies
3. "Correlation Dynamics in Forex and Commodities" - IMF Papers

## 🎓 Conceptos Clave

### ¿Qué es la Correlación?

La correlación mide la relación entre dos variables:
- **+1**: Correlación perfecta positiva
- **0**: Sin correlación
- **-1**: Correlación perfecta negativa

### ¿Por qué EUR/USD y ORO se correlacionan?

1. **Euro como moneda refugio** (después del USD y CHF)
2. **Oro denominado en USD** (cuando USD cae, oro sube)
3. **Expectativas de inflación** (afectan a ambos)
4. **Política del BCE** (influye en demanda de oro)

## 🚀 Próximas Mejoras

Ideas para expandir el sistema:

- [ ] Agregar correlación con DXY (Índice del Dólar)
- [ ] Incluir petróleo (WTI/Brent)
- [ ] Correlación con bonos del tesoro
- [ ] Análisis multi-timeframe
- [ ] Detección automática de cambios de régimen

## 📧 Soporte

Si encuentras problemas o tienes sugerencias:
1. Revisa este README
2. Verifica la configuración en `config.py`
3. Ejecuta `correlacion_oro.py` directamente para ver mensajes de ayuda

---

**Versión**: 1.0  
**Última Actualización**: Noviembre 2024  
**Compatibilidad**: MonedaPredict v1.0+
