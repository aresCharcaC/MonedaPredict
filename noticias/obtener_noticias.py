"""
MÓDULO DE NOTICIAS - PARTE 1: OBTENER NOTICIAS
==============================================
Obtiene noticias financieras relacionadas con EUR/USD
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import os

class ObtenerNoticias:
    def __init__(self):
        """
        Inicializa el obtener de noticias.
        
        OPCIONES GRATUITAS:
        1. NewsAPI (100 requests/día gratis): https://newsapi.org/
        2. Alpha Vantage (500 requests/día): https://www.alphavantage.co/
        3. Google News RSS (ilimitado pero sin API key)
        """
        # Por ahora usaremos Google News RSS (no requiere API key)
        self.base_url = "https://news.google.com/rss"
        
    def obtener_noticias_forex(self, query="EUR USD forex", max_noticias=20):
        """
        Obtiene noticias de Google News RSS
        
        Parámetros:
        - query: Términos de búsqueda
        - max_noticias: Cantidad máxima de noticias
        """
        print(f"📰 Obteniendo noticias sobre: {query}")
        
        try:
            # Importar BeautifulSoup para parsear RSS
            from bs4 import BeautifulSoup
            
            # Construir URL de búsqueda
            url = f"{self.base_url}/search?q={query.replace(' ', '+')}&hl=es&gl=US&ceid=US:es"
            
            # Hacer request
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Parsear XML
            soup = BeautifulSoup(response.content, features='xml')
            items = soup.findAll('item')
            
            noticias = []
            for item in items[:max_noticias]:
                noticia = {
                    'titulo': item.title.text if item.title else '',
                    'descripcion': item.description.text if item.description else '',
                    'fecha': item.pubDate.text if item.pubDate else '',
                    'link': item.link.text if item.link else '',
                    'fuente': item.source.text if item.source else 'Google News'
                }
                noticias.append(noticia)
            
            df = pd.DataFrame(noticias)
            
            # Convertir fecha
            if not df.empty:
                df['fecha'] = pd.to_datetime(df['fecha'], format='%a, %d %b %Y %H:%M:%S %Z', errors='coerce')
            
            print(f"✅ Se obtuvieron {len(df)} noticias")
            return df
            
        except Exception as e:
            print(f"❌ Error al obtener noticias: {e}")
            print("💡 Tip: Instala beautifulsoup4 con: pip install beautifulsoup4 lxml")
            return pd.DataFrame()
    
    def obtener_noticias_newsapi(self, api_key=None):
        """
        Método alternativo usando NewsAPI (requiere API key gratuita)
        Regístrate en: https://newsapi.org/
        """
        if not api_key:
            print("⚠️ Necesitas una API key de NewsAPI")
            print("👉 Regístrate gratis en: https://newsapi.org/")
            return pd.DataFrame()
        
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': 'EUR USD OR forex OR "european central bank" OR "federal reserve"',
            'language': 'en',
            'sortBy': 'publishedAt',
            'apiKey': api_key,
            'pageSize': 20
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'ok':
                articles = data['articles']
                noticias = []
                
                for article in articles:
                    noticia = {
                        'titulo': article.get('title', ''),
                        'descripcion': article.get('description', ''),
                        'fecha': article.get('publishedAt', ''),
                        'link': article.get('url', ''),
                        'fuente': article.get('source', {}).get('name', '')
                    }
                    noticias.append(noticia)
                
                df = pd.DataFrame(noticias)
                df['fecha'] = pd.to_datetime(df['fecha'])
                
                print(f"✅ Se obtuvieron {len(df)} noticias de NewsAPI")
                return df
            else:
                print(f"❌ Error en NewsAPI: {data.get('message', 'Unknown error')}")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"❌ Error al obtener noticias de NewsAPI: {e}")
            return pd.DataFrame()
    
    def guardar_noticias(self, df, filename="datos/noticias_raw.csv"):
        """Guarda las noticias en CSV"""
        if df.empty:
            print("⚠️ No hay noticias para guardar")
            return
        
        os.makedirs("datos", exist_ok=True)
        df.to_csv(filename, index=False)
        print(f"💾 Noticias guardadas en: {filename}")
        
        # Mostrar preview
        print("\n📋 Vista previa:")
        print(df[['fecha', 'titulo']].head())

def main():
    """Función principal de prueba"""
    print("="*60)
    print("📰 OBTENER NOTICIAS FOREX")
    print("="*60)
    
    obtener = ObtenerNoticias()
    
    # Opción 1: Google News RSS (GRATIS, sin API key)
    print("\n🔍 Método 1: Google News RSS (Recomendado para empezar)")
    df = obtener.obtener_noticias_forex(
        query="EUR USD forex currency",
        max_noticias=20
    )
    
    if not df.empty:
        obtener.guardar_noticias(df)
        print("\n✅ Noticias descargadas exitosamente!")
        print("\n👉 Siguiente paso: Ejecuta analizar_sentimiento.py")
    else:
        print("\n⚠️ No se pudieron obtener noticias")
        print("💡 Verifica tu conexión a internet")
    
    # Opción 2: NewsAPI (descomentar si tienes API key)
    # API_KEY = "tu_api_key_aqui"  # Obtén una gratis en https://newsapi.org/
    # df_newsapi = obtener.obtener_noticias_newsapi(api_key=API_KEY)

if __name__ == "__main__":
    main()
