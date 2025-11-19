"""
MÓDULO DE NOTICIAS - PARTE 2: ANÁLISIS DE SENTIMIENTO
=====================================================
Analiza el sentimiento de las noticias usando VADER y TextBlob
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

class AnalizadorSentimiento:
    def __init__(self):
        """Inicializa el analizador de sentimiento"""
        self.analyzer = None
        self._inicializar_vader()
    
    def _inicializar_vader(self):
        """Inicializa VADER Sentiment Analyzer"""
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            self.analyzer = SentimentIntensityAnalyzer()
            print("✅ VADER Sentiment cargado correctamente")
        except ImportError:
            print("⚠️ VADER no está instalado")
            print("💡 Instala con: pip install vaderSentiment")
            self.analyzer = None
    
    def analizar_texto(self, texto):
        """
        Analiza el sentimiento de un texto
        
        Retorna:
        - compound: Score general (-1 a 1)
        - pos: Positividad (0 a 1)
        - neg: Negatividad (0 a 1)
        - neu: Neutralidad (0 a 1)
        """
        if not self.analyzer or not texto:
            return {
                'compound': 0,
                'pos': 0,
                'neg': 0,
                'neu': 1
            }
        
        # Analizar sentimiento
        scores = self.analyzer.polarity_scores(texto)
        return scores
    
    def clasificar_sentimiento(self, compound_score):
        """
        Clasifica el sentimiento basado en el score compound
        
        Criterios VADER:
        - Positivo: compound >= 0.05
        - Negativo: compound <= -0.05
        - Neutral: -0.05 < compound < 0.05
        """
        if compound_score >= 0.05:
            return 'POSITIVO'
        elif compound_score <= -0.05:
            return 'NEGATIVO'
        else:
            return 'NEUTRAL'
    
    def interpretar_para_forex(self, compound_score, titulo):
        """
        Interpreta cómo afecta la noticia al EUR/USD
        
        Lógica simplificada:
        - Noticias positivas sobre economía EU/Euro -> EUR sube (1)
        - Noticias negativas sobre economía EU/Euro -> EUR baja (-1)
        - Noticias positivas sobre USD/Fed -> EUR baja (-1)
        - Noticias negativas sobre USD/Fed -> EUR sube (1)
        """
        titulo_lower = titulo.lower()
        
        # Palabras clave para identificar contexto
        keywords_eur = ['euro', 'europe', 'ecb', 'european central bank', 'eurozone']
        keywords_usd = ['dollar', 'usd', 'fed', 'federal reserve', 'us economy']
        
        # Detectar contexto
        es_sobre_eur = any(keyword in titulo_lower for keyword in keywords_eur)
        es_sobre_usd = any(keyword in titulo_lower for keyword in keywords_usd)
        
        # Interpretación
        if es_sobre_eur and not es_sobre_usd:
            # Noticia sobre EUR: positivo->EUR sube, negativo->EUR baja
            return 1 if compound_score > 0 else -1
        elif es_sobre_usd and not es_sobre_eur:
            # Noticia sobre USD: positivo->USD sube (EUR baja), negativo->USD baja (EUR sube)
            return -1 if compound_score > 0 else 1
        else:
            # Noticia general o ambigua
            return compound_score  # Usar score directo
    
    def analizar_noticias(self, df):
        """
        Analiza todas las noticias en el DataFrame
        
        Parámetros:
        - df: DataFrame con columnas 'titulo' y 'descripcion'
        """
        if df.empty:
            print("⚠️ DataFrame vacío")
            return df
        
        print(f"📊 Analizando {len(df)} noticias...")
        
        resultados = []
        
        for idx, row in df.iterrows():
            # Combinar título y descripción
            texto = f"{row.get('titulo', '')} {row.get('descripcion', '')}"
            
            # Analizar sentimiento
            scores = self.analizar_texto(texto)
            
            # Clasificar
            clasificacion = self.clasificar_sentimiento(scores['compound'])
            
            # Interpretar para forex
            impacto_eur = self.interpretar_para_forex(
                scores['compound'],
                row.get('titulo', '')
            )
            
            resultado = {
                'sentimiento_compound': scores['compound'],
                'sentimiento_pos': scores['pos'],
                'sentimiento_neg': scores['neg'],
                'sentimiento_neu': scores['neu'],
                'clasificacion': clasificacion,
                'impacto_eur': impacto_eur
            }
            
            resultados.append(resultado)
        
        # Agregar resultados al DataFrame
        df_resultados = pd.DataFrame(resultados)
        df_final = pd.concat([df, df_resultados], axis=1)
        
        print("✅ Análisis completado!")
        
        # Mostrar estadísticas
        self._mostrar_estadisticas(df_final)
        
        return df_final
    
    def _mostrar_estadisticas(self, df):
        """Muestra estadísticas del análisis"""
        print("\n📈 ESTADÍSTICAS DEL ANÁLISIS:")
        print("="*50)
        
        # Distribución de sentimientos
        if 'clasificacion' in df.columns:
            print("\n🎯 Distribución de Sentimientos:")
            print(df['clasificacion'].value_counts())
        
        # Promedio de scores
        if 'sentimiento_compound' in df.columns:
            print(f"\n📊 Score Promedio: {df['sentimiento_compound'].mean():.3f}")
            print(f"📈 Score Máximo: {df['sentimiento_compound'].max():.3f}")
            print(f"📉 Score Mínimo: {df['sentimiento_compound'].min():.3f}")
        
        # Impacto promedio en EUR
        if 'impacto_eur' in df.columns:
            impacto_promedio = df['impacto_eur'].mean()
            print(f"\n💹 Impacto Promedio en EUR/USD: {impacto_promedio:.3f}")
            if impacto_promedio > 0.05:
                print("   → Las noticias favorecen al EURO 📈")
            elif impacto_promedio < -0.05:
                print("   → Las noticias favorecen al DÓLAR 📉")
            else:
                print("   → Las noticias son neutrales ➡️")
    
    def guardar_analisis(self, df, filename="datos/noticias_sentimiento.csv"):
        """Guarda el análisis en CSV"""
        os.makedirs("datos", exist_ok=True)
        df.to_csv(filename, index=False)
        print(f"\n💾 Análisis guardado en: {filename}")

def main():
    """Función principal"""
    print("="*60)
    print("🧠 ANÁLISIS DE SENTIMIENTO DE NOTICIAS")
    print("="*60)
    
    # Leer noticias
    archivo_noticias = "datos/noticias_raw.csv"
    
    if not os.path.exists(archivo_noticias):
        print(f"❌ No se encontró: {archivo_noticias}")
        print("👉 Primero ejecuta: obtener_noticias.py")
        return
    
    print(f"📂 Leyendo noticias desde: {archivo_noticias}")
    df = pd.read_csv(archivo_noticias)
    
    # Analizar sentimiento
    analizador = AnalizadorSentimiento()
    
    if analizador.analyzer is None:
        print("\n❌ No se puede continuar sin VADER")
        print("💡 Instala con: pip install vaderSentiment")
        return
    
    df_analizado = analizador.analizar_noticias(df)
    
    # Guardar resultados
    analizador.guardar_analisis(df_analizado)
    
    # Mostrar ejemplos
    print("\n📋 EJEMPLOS DE ANÁLISIS:")
    print("="*60)
    for idx, row in df_analizado.head(5).iterrows():
        print(f"\n📰 {row['titulo'][:80]}...")
        print(f"   Sentimiento: {row['clasificacion']} ({row['sentimiento_compound']:.3f})")
        print(f"   Impacto EUR: {'📈 Positivo' if row['impacto_eur'] > 0 else '📉 Negativo' if row['impacto_eur'] < 0 else '➡️ Neutral'}")
    
    print("\n✅ PROCESO COMPLETADO!")
    print("👉 Siguiente paso: Integrar con el modelo LSTM")

if __name__ == "__main__":
    main()
