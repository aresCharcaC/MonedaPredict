"""
MÓDULO DE NOTICIAS - PARTE 3: INTEGRAR CON MODELO LSTM
======================================================
Integra el análisis de sentimiento de noticias con el modelo de predicción
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

class IntegradorNoticias:
    def __init__(self):
        """Inicializa el integrador"""
        pass
    
    def cargar_datos_precio(self, archivo="datos/eurusd_datos.csv"):
        """Carga datos de precios históricos"""
        if not os.path.exists(archivo):
            print(f"❌ No se encontró: {archivo}")
            return None
        
        df = pd.read_csv(archivo)
        df['time'] = pd.to_datetime(df['time'])
        print(f"✅ Cargados {len(df)} registros de precios")
        return df
    
    def cargar_datos_noticias(self, archivo="datos/noticias_sentimiento.csv"):
        """Carga datos de noticias analizadas"""
        if not os.path.exists(archivo):
            print(f"❌ No se encontró: {archivo}")
            return None
        
        df = pd.read_csv(archivo)
        df['fecha'] = pd.to_datetime(df['fecha'])
        print(f"✅ Cargadas {len(df)} noticias analizadas")
        return df
    
    def agregar_sentimiento_diario(self, df_precios, df_noticias):
        """
        Agrega features de sentimiento al DataFrame de precios
        
        Estrategia:
        - Agrupa noticias por día
        - Calcula sentimiento promedio diario
        - Une con datos de precios
        """
        print("\n🔄 Integrando sentimiento con precios...")
        
        # Extraer solo la fecha (sin hora) de los precios
        df_precios['fecha'] = pd.to_datetime(df_precios['time']).dt.date
        
        # Extraer fecha de noticias
        df_noticias['fecha'] = pd.to_datetime(df_noticias['fecha']).dt.date
        
        # Agrupar noticias por día y calcular estadísticas
        sentimiento_diario = df_noticias.groupby('fecha').agg({
            'sentimiento_compound': ['mean', 'std', 'min', 'max'],
            'impacto_eur': ['mean', 'sum'],
            'clasificacion': lambda x: (x == 'POSITIVO').sum() - (x == 'NEGATIVO').sum()
        }).reset_index()
        
        # Aplanar columnas
        sentimiento_diario.columns = [
            'fecha',
            'sent_mean',      # Sentimiento promedio
            'sent_std',       # Volatilidad del sentimiento
            'sent_min',       # Sentimiento más negativo
            'sent_max',       # Sentimiento más positivo
            'impact_mean',    # Impacto promedio en EUR
            'impact_sum',     # Impacto acumulado
            'sent_balance'    # Balance positivas - negativas
        ]
        
        # Unir con precios
        df_integrado = df_precios.merge(
            sentimiento_diario,
            on='fecha',
            how='left'
        )
        
        # Rellenar valores faltantes (días sin noticias)
        df_integrado['sent_mean'] = df_integrado['sent_mean'].fillna(0)
        df_integrado['sent_std'] = df_integrado['sent_std'].fillna(0)
        df_integrado['sent_min'] = df_integrado['sent_min'].fillna(0)
        df_integrado['sent_max'] = df_integrado['sent_max'].fillna(0)
        df_integrado['impact_mean'] = df_integrado['impact_mean'].fillna(0)
        df_integrado['impact_sum'] = df_integrado['impact_sum'].fillna(0)
        df_integrado['sent_balance'] = df_integrado['sent_balance'].fillna(0)
        
        # Eliminar columna auxiliar 'fecha'
        df_integrado = df_integrado.drop('fecha', axis=1)
        
        print(f"✅ Datos integrados: {len(df_integrado)} registros")
        print(f"📊 Nuevas features agregadas: sent_mean, sent_std, impact_mean, sent_balance, etc.")
        
        return df_integrado
    
    def crear_features_temporales(self, df):
        """
        Crea features de sentimiento con ventanas temporales
        
        Ejemplos:
        - Sentimiento promedio últimas 24 horas
        - Tendencia del sentimiento
        """
        print("\n🔧 Creando features temporales de sentimiento...")
        
        # Sentimiento móvil (últimas 24 horas para M15)
        # 24 horas = 96 períodos de 15 minutos
        df['sent_ma_24h'] = df['sent_mean'].rolling(window=96, min_periods=1).mean()
        
        # Tendencia del sentimiento (diferencia)
        df['sent_trend'] = df['sent_mean'].diff()
        
        # Volatilidad del impacto
        df['impact_volatility'] = df['impact_mean'].rolling(window=96, min_periods=1).std()
        
        # Rellenar NaN
        df = df.fillna(0)
        
        print("✅ Features temporales creadas")
        
        return df
    
    def guardar_datos_integrados(self, df, filename="datos/eurusd_con_sentimiento.csv"):
        """Guarda los datos integrados"""
        os.makedirs("datos", exist_ok=True)
        df.to_csv(filename, index=False)
        print(f"\n💾 Datos integrados guardados en: {filename}")
        
        # Mostrar info
        print("\n📊 COLUMNAS DISPONIBLES:")
        print(list(df.columns))
        
        print("\n📈 ESTADÍSTICAS DE SENTIMIENTO:")
        print(df[['sent_mean', 'impact_mean', 'sent_balance']].describe())
    
    def visualizar_correlacion(self, df):
        """Analiza correlación entre sentimiento y precio"""
        print("\n📊 ANÁLISIS DE CORRELACIÓN:")
        print("="*60)
        
        # Calcular retorno del precio
        df['retorno'] = df['close'].pct_change()
        
        # Correlaciones
        correlaciones = {
            'Sentimiento vs Retorno': df['sent_mean'].corr(df['retorno']),
            'Impacto vs Retorno': df['impact_mean'].corr(df['retorno']),
            'Balance vs Retorno': df['sent_balance'].corr(df['retorno'])
        }
        
        for nombre, corr in correlaciones.items():
            print(f"{nombre}: {corr:.4f}")
            if abs(corr) > 0.1:
                print(f"  → {'Correlación positiva significativa' if corr > 0 else 'Correlación negativa significativa'}")
            else:
                print(f"  → Correlación débil")

def main():
    """Función principal"""
    print("="*60)
    print("🔗 INTEGRAR NOTICIAS CON MODELO")
    print("="*60)
    
    integrador = IntegradorNoticias()
    
    # 1. Cargar datos
    df_precios = integrador.cargar_datos_precio()
    df_noticias = integrador.cargar_datos_noticias()
    
    if df_precios is None or df_noticias is None:
        print("\n❌ Faltan datos necesarios")
        print("👉 Ejecuta primero: obtener_noticias.py y analizar_sentimiento.py")
        return
    
    # 2. Integrar
    df_integrado = integrador.agregar_sentimiento_diario(df_precios, df_noticias)
    
    # 3. Crear features temporales
    df_integrado = integrador.crear_features_temporales(df_integrado)
    
    # 4. Visualizar correlación
    integrador.visualizar_correlacion(df_integrado)
    
    # 5. Guardar
    integrador.guardar_datos_integrados(df_integrado)
    
    print("\n✅ INTEGRACIÓN COMPLETADA!")
    print("\n📝 PRÓXIMOS PASOS:")
    print("1. Modificar entrenar_modelo.py para usar las nuevas features")
    print("2. Incluir sent_mean, impact_mean, sent_balance en el modelo LSTM")
    print("3. Re-entrenar el modelo con datos enriquecidos")

if __name__ == "__main__":
    main()
