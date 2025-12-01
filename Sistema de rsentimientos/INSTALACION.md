# Sistema de Análisis de Sentimientos EUR/USD

Este archivo contiene información sobre las dependencias necesarias para el sistema.

## 📦 Dependencias Requeridas

### Instalación mediante pip:

```bash
pip install vaderSentiment beautifulsoup4 requests pandas numpy matplotlib lxml
```

### Lista detallada:

- **vaderSentiment**: Análisis de sentimiento VADER
- **beautifulsoup4**: Parsing de RSS feeds
- **requests**: Obtención de noticias HTTP
- **pandas**: Manejo de datos
- **numpy**: Operaciones numéricas
- **matplotlib**: Visualización de gráficos
- **lxml**: Parser XML para BeautifulSoup

## ✅ Verificar instalación

Ejecuta desde PowerShell:

```powershell
python -c "import vaderSentiment; import bs4; import requests; import pandas; import numpy; import matplotlib; print('✅ Todas las dependencias instaladas correctamente')"
```

## 🚀 Inicio Rápido

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Verificar configuración:
   ```bash
   python config_sentimientos.py
   ```

3. Ejecutar análisis único:
   ```bash
   python monitor_sentimientos.py --once
   ```

4. Iniciar monitoreo continuo:
   ```bash
   python monitor_sentimientos.py
   ```
