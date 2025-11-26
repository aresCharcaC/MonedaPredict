"""
MÓDULO DE NOTICIAS - PARTE 1: OBTENER NOTICIAS
==============================================
Obtiene noticias financieras de MÚLTIPLES FUENTES
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import time

class ObtenerNoticias:
    def __init__(self):
        """
        Inicializa el obtener de noticias con múltiples fuentes.
        
        FUENTES DISPONIBLES:
        1. Google News RSS (ilimitado, gratis)
        2. NewsAPI (100 requests/día gratis)
        3. Investing.com RSS (ilimitado, gratis)
        4. FXStreet RSS (ilimitado, gratis)
        5. ForexLive RSS (ilimitado, gratis)
        """
        self.fuentes = {
            'google_news': "https://news.google.com/rss",
            'investing': "https://www.investing.com/rss/news.rss",
            'fxstreet': "https://www.fxstreet.com/rss",
            'forexlive': "https://www.forexlive.com/feed/news"
        }
        
    def obtener_noticias_google(self, query="EUR USD forex", max_noticias=20):
        """
        Obtiene noticias de Google News RSS
        
        Parámetros:
        - query: Términos de búsqueda
        - max_noticias: Cantidad máxima de noticias
        """
        print(f"\n📰 [Google News] Buscando: {query}")
        
        try:
            from bs4 import BeautifulSoup
            
            url = f"{self.fuentes['google_news']}/search?q={query.replace(' ', '+')}&hl=es&gl=US&ceid=US:es"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, features='xml')
            items = soup.find_all('item')
            
            noticias = []
            for item in items[:max_noticias]:
                noticia = {
                    'titulo': item.title.text if item.title else '',
                    'descripcion': item.description.text if item.description else '',
                    'fecha': item.pubDate.text if item.pubDate else '',
                    'link': item.link.text if item.link else '',
                    'fuente': 'Google News'
                }
                noticias.append(noticia)
            
            df = pd.DataFrame(noticias)
            
            if not df.empty:
                df['fecha'] = pd.to_datetime(df['fecha'], format='%a, %d %b %Y %H:%M:%S %Z', errors='coerce', utc=True)
            
            print(f"   ✅ {len(df)} noticias obtenidas")
            return df
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return pd.DataFrame()
    
    def obtener_noticias_investing(self, max_noticias=20):
        """
        Obtiene noticias de Investing.com RSS
        """
        print(f"\n📰 [Investing.com] Obteniendo noticias...")
        
        try:
            from bs4 import BeautifulSoup
            
            response = requests.get(self.fuentes['investing'], timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, features='xml')
            items = soup.find_all('item')
            
            noticias = []
            for item in items[:max_noticias]:
                noticia = {
                    'titulo': item.title.text if item.title else '',
                    'descripcion': item.description.text if item.description else '',
                    'fecha': item.pubDate.text if item.pubDate else '',
                    'link': item.link.text if item.link else '',
                    'fuente': 'Investing.com'
                }
                noticias.append(noticia)
            
            df = pd.DataFrame(noticias)
            
            if not df.empty:
                df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce', utc=True)
            
            print(f"   ✅ {len(df)} noticias obtenidas")
            return df
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return pd.DataFrame()
    
    def obtener_noticias_fxstreet(self, max_noticias=20):
        """
        Obtiene noticias de FXStreet RSS
        """
        print(f"\n📰 [FXStreet] Obteniendo noticias...")
        
        try:
            from bs4 import BeautifulSoup
            
            response = requests.get(self.fuentes['fxstreet'], timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, features='xml')
            items = soup.find_all('item')
            
            noticias = []
            for item in items[:max_noticias]:
                noticia = {
                    'titulo': item.title.text if item.title else '',
                    'descripcion': item.description.text if item.description else '',
                    'fecha': item.pubDate.text if item.pubDate else '',
                    'link': item.link.text if item.link else '',
                    'fuente': 'FXStreet'
                }
                noticias.append(noticia)
            
            df = pd.DataFrame(noticias)
            
            if not df.empty:
                df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce', utc=True)
            
            print(f"   ✅ {len(df)} noticias obtenidas")
            return df
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return pd.DataFrame()
    
    def obtener_noticias_forexlive(self, max_noticias=20):
        """
        Obtiene noticias de ForexLive RSS
        """
        print(f"\n📰 [ForexLive] Obteniendo noticias...")
        
        try:
            from bs4 import BeautifulSoup
            
            response = requests.get(self.fuentes['forexlive'], timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, features='xml')
            items = soup.find_all('item')
            
            noticias = []
            for item in items[:max_noticias]:
                noticia = {
                    'titulo': item.title.text if item.title else '',
                    'descripcion': item.description.text if item.description else '',
                    'fecha': item.pubDate.text if item.pubDate else '',
                    'link': item.link.text if item.link else '',
                    'fuente': 'ForexLive'
                }
                noticias.append(noticia)
            
            df = pd.DataFrame(noticias)
            
            if not df.empty:
                df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce', utc=True)
            
            print(f"   ✅ {len(df)} noticias obtenidas")
            return df
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return pd.DataFrame()
    
    def obtener_todas_las_fuentes(self, max_por_fuente=15):
        """
        Obtiene noticias de TODAS las fuentes disponibles y las combina
        
        Parámetros:
        - max_por_fuente: Cantidad máxima por cada fuente
        
        Retorna:
        - DataFrame con noticias de todas las fuentes, sin duplicados
        """
        print("\n🌐 OBTENIENDO NOTICIAS DE MÚLTIPLES FUENTES")
        print("="*60)
        
        todas_noticias = []
        
        # Fuente 1: Google News
        df_google = self.obtener_noticias_google(max_noticias=max_por_fuente)
        if not df_google.empty:
            todas_noticias.append(df_google)
        
        time.sleep(1)  # Pausa cortés entre requests
        
        # Fuente 2: Investing.com
        df_investing = self.obtener_noticias_investing(max_noticias=max_por_fuente)
        if not df_investing.empty:
            todas_noticias.append(df_investing)
        
        time.sleep(1)
        
        # Fuente 3: FXStreet
        df_fxstreet = self.obtener_noticias_fxstreet(max_noticias=max_por_fuente)
        if not df_fxstreet.empty:
            todas_noticias.append(df_fxstreet)
        
        time.sleep(1)
        
        # Fuente 4: ForexLive
        df_forexlive = self.obtener_noticias_forexlive(max_noticias=max_por_fuente)
        if not df_forexlive.empty:
            todas_noticias.append(df_forexlive)
        
        # Combinar todas las fuentes
        if todas_noticias:
            df_combined = pd.concat(todas_noticias, ignore_index=True)
            
            # Eliminar duplicados por título (case-insensitive)
            antes = len(df_combined)
            df_combined['titulo_lower'] = df_combined['titulo'].str.lower()
            df_combined = df_combined.drop_duplicates(subset=['titulo_lower'])
            df_combined = df_combined.drop(columns=['titulo_lower'])
            despues = len(df_combined)
            
            # Ordenar por fecha (más recientes primero)
            df_combined = df_combined.sort_values('fecha', ascending=False)
            df_combined = df_combined.reset_index(drop=True)
            
            # Estadísticas
            print("\n" + "="*60)
            print("📊 RESUMEN DE NOTICIAS")
            print("="*60)
            print(f"📰 Total obtenido: {antes} noticias")
            print(f"🗑️  Duplicados eliminados: {antes - despues}")
            print(f"✅ Noticias únicas: {despues}")
            print("\n📋 Por fuente:")
            for fuente, count in df_combined['fuente'].value_counts().items():
                print(f"   {fuente}: {count} noticias")
            
            return df_combined
        else:
            print("\n❌ No se pudo obtener noticias de ninguna fuente")
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
                df['fecha'] = pd.to_datetime(df['fecha'], utc=True)
                
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
    print("="*70)
    print("📰 OBTENER NOTICIAS FOREX - MÚLTIPLES FUENTES")
    print("="*70)
    
    obtener = ObtenerNoticias()
    
    # OPCIÓN 1: Obtener de TODAS las fuentes (RECOMENDADO)
    print("\n🌐 Método: Múltiples Fuentes (Google, Investing, FXStreet, ForexLive)")
    df = obtener.obtener_todas_las_fuentes(max_por_fuente=15)
    
    if not df.empty:
        obtener.guardar_noticias(df)
        print("\n✅ Noticias descargadas exitosamente!")
        print(f"📊 Total: {len(df)} noticias de {df['fuente'].nunique()} fuentes")
        print("\n👉 Siguiente paso: python noticias/analizar_sentimiento.py")
    else:
        print("\n⚠️ No se pudieron obtener noticias")
        print("💡 Verifica tu conexión a internet")
    
    # OPCIÓN 2: NewsAPI (descomentar si tienes API key)
    # print("\n\n📰 [OPCIONAL] NewsAPI")
    # API_KEY = "tu_api_key_aqui"  # Obtén una gratis en https://newsapi.org/
    # df_newsapi = obtener.obtener_noticias_newsapi(api_key=API_KEY)
    # if not df_newsapi.empty:
    #     df = pd.concat([df, df_newsapi]).drop_duplicates(subset=['titulo'])

if __name__ == "__main__":
    main()

