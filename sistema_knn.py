"""
╔══════════════════════════════════════════════════════════════════╗
║   SISTEMA DE RECOMENDACIÓN - K-NEAREST NEIGHBORS (KNN)          ║
║   Encuentra patrones históricos similares para recomendar        ║
║   operaciones basadas en situaciones pasadas exitosas           ║
╚══════════════════════════════════════════════════════════════════╝

🎯 ¿Cómo funciona?
------------------
1. Extrae el contexto actual del mercado (precio, indicadores, oro, sentimiento)
2. Busca en el histórico las K situaciones más similares
3. Analiza qué pasó después en esas situaciones
4. Recomienda la acción con mayor probabilidad de éxito

📊 Ventajas del KNN para Trading:
---------------------------------
✅ No requiere re-entrenamiento constante
✅ Explica sus decisiones (muestra casos similares)
✅ Se adapta automáticamente a nuevos datos
✅ Combina análisis técnico + fundamental + sentimiento
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import pickle
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class SistemaRecomendacionKNN:
    """
    Sistema de recomendación basado en K-Nearest Neighbors para trading.
    
    Encuentra patrones históricos similares al contexto actual del mercado
    y recomienda operaciones basadas en lo que ocurrió en esas situaciones.
    """
    
    def __init__(self, k_vecinos=50, min_datos=500):
        """
        Inicializa el sistema de recomendación.
        
        Parámetros:
        -----------
        k_vecinos : int
            Número de vecinos más cercanos a considerar (default: 50)
            Más vecinos = más estable pero menos específico
            Menos vecinos = más específico pero puede ser ruidoso
            
        min_datos : int
            Mínimo de registros históricos necesarios (default: 500)
        """
        self.k_vecinos = k_vecinos
        self.min_datos = min_datos
        self.modelo_knn = None
        self.scaler = StandardScaler()
        self.datos_historicos = None
        self.features_usadas = []
        self.estadisticas = {}
        
    def preparar_datos_historicos(self, df, horizonte_prediccion=4):
        """
        Prepara datos históricos para el sistema KNN.
        
        Parámetros:
        -----------
        df : DataFrame
            Datos históricos con features
        horizonte_prediccion : int
            Cuántas velas hacia adelante mirar para etiquetar resultados
            H4: 4 velas = 16 horas
            H1: 4 velas = 4 horas
        
        Retorna:
        --------
        bool : True si se preparó correctamente
        """
        print("\n" + "="*70)
        print("🔧 PREPARANDO SISTEMA DE RECOMENDACIÓN KNN")
        print("="*70)
        
        if df is None or len(df) < self.min_datos:
            print(f"❌ Error: Se necesitan al menos {self.min_datos} registros")
            print(f"   Tienes: {len(df) if df is not None else 0}")
            return False
        
        # Hacer una copia para no modificar el original
        df = df.copy()
        
        # Identificar features disponibles
        features_basicas = ['open', 'high', 'low', 'close', 'tick_volume']
        features_tecnicas = ['MA_10', 'MA_30', 'MA_50', 'RSI', 'Volatility', 
                            'HL_Range', 'Price_Change', 'Volume_MA']
        features_oro = ['close_oro', 'ratio_eur_oro', 'ratio_desviacion', 
                       'divergencia_retornos', 'oro_tendencia', 'ratio_volatilidad',
                       'correlacion', 'correlacion_ma', 'oro_momentum']
        features_sentimiento = ['sent_mean', 'impact_mean', 'sent_balance', 
                               'sent_ma_24h', 'sent_trend']
        
        # Seleccionar solo las features que existen en el DataFrame
        self.features_usadas = []
        
        for feat in features_basicas + features_tecnicas:
            if feat in df.columns:
                self.features_usadas.append(feat)
        
        print(f"\n📊 Features detectadas:")
        print(f"   • Básicas/Técnicas: {len(self.features_usadas)}")
        
        # Agregar features de oro si existen
        oro_count = 0
        for feat in features_oro:
            if feat in df.columns:
                self.features_usadas.append(feat)
                oro_count += 1
        if oro_count > 0:
            print(f"   • Correlación ORO: {oro_count} ✅")
        
        # Agregar features de sentimiento si existen
        sent_count = 0
        for feat in features_sentimiento:
            if feat in df.columns:
                self.features_usadas.append(feat)
                sent_count += 1
        if sent_count > 0:
            print(f"   • Sentimiento: {sent_count} ✅")
        
        print(f"\n🎯 Total features para KNN: {len(self.features_usadas)}")
        
        # Crear etiquetas de resultado (qué pasó después)
        df['retorno_futuro'] = df['close'].shift(-horizonte_prediccion) / df['close'] - 1
        
        # Clasificar el resultado
        # COMPRA: El precio subió más de 0.05% en las próximas velas
        # VENTA: El precio bajó más de 0.05% en las próximas velas
        # ESPERA: El precio se mantuvo estable (±0.05%)
        umbral = 0.0005  # 0.05%
        
        df['accion_resultado'] = 'ESPERA'
        df.loc[df['retorno_futuro'] > umbral, 'accion_resultado'] = 'COMPRA'
        df.loc[df['retorno_futuro'] < -umbral, 'accion_resultado'] = 'VENTA'
        
        # Eliminar las últimas filas sin etiqueta
        df = df.dropna(subset=['retorno_futuro'])
        
        # Guardar datos históricos
        self.datos_historicos = df
        
        # Preparar matriz de features
        X = df[self.features_usadas].values
        
        # Normalizar features
        X_scaled = self.scaler.fit_transform(X)
        
        # Entrenar modelo KNN
        print(f"\n🔍 Entrenando KNN con {self.k_vecinos} vecinos...")
        self.modelo_knn = NearestNeighbors(
            n_neighbors=min(self.k_vecinos, len(df)),
            algorithm='auto',
            metric='euclidean'
        )
        self.modelo_knn.fit(X_scaled)
        
        # Calcular estadísticas
        self._calcular_estadisticas()
        
        print(f"✅ Sistema KNN entrenado con {len(df)} patrones históricos")
        
        return True
    
    def _calcular_estadisticas(self):
        """Calcula estadísticas del histórico"""
        df = self.datos_historicos
        
        total = len(df)
        compras = len(df[df['accion_resultado'] == 'COMPRA'])
        ventas = len(df[df['accion_resultado'] == 'VENTA'])
        esperas = len(df[df['accion_resultado'] == 'ESPERA'])
        
        self.estadisticas = {
            'total_patrones': total,
            'compras': compras,
            'ventas': ventas,
            'esperas': esperas,
            'pct_compras': (compras/total)*100,
            'pct_ventas': (ventas/total)*100,
            'pct_esperas': (esperas/total)*100,
            'retorno_medio_compras': df[df['accion_resultado'] == 'COMPRA']['retorno_futuro'].mean(),
            'retorno_medio_ventas': df[df['accion_resultado'] == 'VENTA']['retorno_futuro'].mean()
        }
        
        print(f"\n📈 Estadísticas del histórico:")
        print(f"   • Patrones COMPRA: {compras} ({self.estadisticas['pct_compras']:.1f}%)")
        print(f"   • Patrones VENTA: {ventas} ({self.estadisticas['pct_ventas']:.1f}%)")
        print(f"   • Patrones ESPERA: {esperas} ({self.estadisticas['pct_esperas']:.1f}%)")
    
    def obtener_recomendacion(self, datos_actuales, explicar=True):
        """
        Obtiene recomendación basada en patrones similares.
        
        Parámetros:
        -----------
        datos_actuales : dict o DataFrame
            Datos del mercado actual con todas las features
        explicar : bool
            Si True, retorna explicación detallada
        
        Retorna:
        --------
        dict : {
            'accion': 'COMPRA'|'VENTA'|'ESPERA',
            'confianza': 0-100,
            'vecinos_compra': int,
            'vecinos_venta': int,
            'vecinos_espera': int,
            'retorno_esperado': float,
            'patrones_similares': DataFrame (si explicar=True)
        }
        """
        if self.modelo_knn is None:
            print("❌ Error: Sistema KNN no entrenado")
            return None
        
        # Convertir datos_actuales a array
        if isinstance(datos_actuales, dict):
            X_actual = np.array([datos_actuales[feat] for feat in self.features_usadas]).reshape(1, -1)
        elif isinstance(datos_actuales, pd.DataFrame):
            X_actual = datos_actuales[self.features_usadas].iloc[-1:].values
        elif isinstance(datos_actuales, pd.Series):
            X_actual = np.array([datos_actuales[feat] for feat in self.features_usadas]).reshape(1, -1)
        else:
            X_actual = np.array(datos_actuales).reshape(1, -1)
        
        # Normalizar
        X_actual_scaled = self.scaler.transform(X_actual)
        
        # Encontrar vecinos más cercanos
        distancias, indices = self.modelo_knn.kneighbors(X_actual_scaled)
        
        # Obtener los patrones similares
        vecinos = self.datos_historicos.iloc[indices[0]]
        
        # Contar acciones de los vecinos
        conteo_acciones = vecinos['accion_resultado'].value_counts()
        vecinos_compra = conteo_acciones.get('COMPRA', 0)
        vecinos_venta = conteo_acciones.get('VENTA', 0)
        vecinos_espera = conteo_acciones.get('ESPERA', 0)
        
        # Determinar acción recomendada (mayoría de votos)
        if vecinos_compra > vecinos_venta and vecinos_compra > vecinos_espera:
            accion = 'COMPRA'
            confianza = (vecinos_compra / len(vecinos)) * 100
            retorno_esperado = vecinos[vecinos['accion_resultado'] == 'COMPRA']['retorno_futuro'].mean()
        elif vecinos_venta > vecinos_compra and vecinos_venta > vecinos_espera:
            accion = 'VENTA'
            confianza = (vecinos_venta / len(vecinos)) * 100
            retorno_esperado = vecinos[vecinos['accion_resultado'] == 'VENTA']['retorno_futuro'].mean()
        else:
            accion = 'ESPERA'
            confianza = (vecinos_espera / len(vecinos)) * 100
            retorno_esperado = 0.0
        
        # Ajustar confianza basado en distancias (vecinos más cercanos = mayor confianza)
        distancia_media = distancias[0].mean()
        factor_distancia = max(0.5, 1 - (distancia_media / 10))  # Penalizar si están muy lejos
        confianza = confianza * factor_distancia
        
        resultado = {
            'accion': accion,
            'confianza': min(confianza, 100),
            'vecinos_compra': int(vecinos_compra),
            'vecinos_venta': int(vecinos_venta),
            'vecinos_espera': int(vecinos_espera),
            'retorno_esperado': retorno_esperado * 100,  # En porcentaje
            'distancia_media': distancia_media
        }
        
        if explicar:
            # Agregar columna de distancia a los vecinos
            vecinos_explicacion = vecinos.copy()
            vecinos_explicacion['distancia'] = distancias[0]
            vecinos_explicacion = vecinos_explicacion.sort_values('distancia')
            resultado['patrones_similares'] = vecinos_explicacion[
                ['time', 'close', 'accion_resultado', 'retorno_futuro', 'distancia']
            ].head(10)
        
        return resultado
    
    def mostrar_recomendacion(self, recomendacion):
        """
        Muestra la recomendación de forma visual y comprensible.
        
        Parámetros:
        -----------
        recomendacion : dict
            Resultado de obtener_recomendacion()
        """
        print("\n" + "="*70)
        print("🎯 RECOMENDACIÓN DEL SISTEMA KNN")
        print("="*70)
        
        accion = recomendacion['accion']
        confianza = recomendacion['confianza']
        
        # Emoji según la acción
        if accion == 'COMPRA':
            emoji = "📈 🟢"
            color = "VERDE"
        elif accion == 'VENTA':
            emoji = "📉 🔴"
            color = "ROJO"
        else:
            emoji = "⏸️ 🟡"
            color = "AMARILLO"
        
        print(f"\n{emoji} ACCIÓN RECOMENDADA: {accion}")
        print(f"🎯 Confianza: {confianza:.1f}%")
        print(f"📊 Retorno esperado: {recomendacion['retorno_esperado']:.3f}%")
        
        print(f"\n🔍 Análisis de {self.k_vecinos} patrones similares:")
        print(f"   📈 COMPRA: {recomendacion['vecinos_compra']} patrones ({recomendacion['vecinos_compra']/self.k_vecinos*100:.1f}%)")
        print(f"   📉 VENTA:  {recomendacion['vecinos_venta']} patrones ({recomendacion['vecinos_venta']/self.k_vecinos*100:.1f}%)")
        print(f"   ⏸️  ESPERA: {recomendacion['vecinos_espera']} patrones ({recomendacion['vecinos_espera']/self.k_vecinos*100:.1f}%)")
        
        if 'patrones_similares' in recomendacion:
            print(f"\n📋 Top 10 situaciones más similares del pasado:")
            print("-" * 70)
            for idx, row in recomendacion['patrones_similares'].iterrows():
                fecha = row['time'] if 'time' in row else idx
                resultado = row['accion_resultado']
                retorno = row['retorno_futuro'] * 100
                distancia = row['distancia']
                
                emoji_resultado = "🟢" if resultado == "COMPRA" else ("🔴" if resultado == "VENTA" else "🟡")
                
                print(f"   {emoji_resultado} {fecha} | {resultado:6} | Retorno: {retorno:+.3f}% | Similitud: {1/(1+distancia):.3f}")
        
        # Interpretación de confianza
        print(f"\n💡 Interpretación:")
        if confianza >= 70:
            print(f"   ✅ Confianza ALTA - Patrón muy claro en el histórico")
        elif confianza >= 50:
            print(f"   ⚠️  Confianza MEDIA - Señal moderadamente confiable")
        else:
            print(f"   ❌ Confianza BAJA - Señal débil, considerar esperar")
        
        print("="*70)
    
    def guardar_modelo(self, filename="modelos/sistema_knn.pkl"):
        """Guarda el sistema KNN entrenado"""
        os.makedirs("modelos", exist_ok=True)
        
        datos = {
            'modelo_knn': self.modelo_knn,
            'scaler': self.scaler,
            'features_usadas': self.features_usadas,
            'k_vecinos': self.k_vecinos,
            'estadisticas': self.estadisticas,
            'datos_historicos': self.datos_historicos
        }
        
        with open(filename, 'wb') as f:
            pickle.dump(datos, f)
        
        print(f"💾 Sistema KNN guardado en: {filename}")
    
    def cargar_modelo(self, filename="modelos/sistema_knn.pkl"):
        """Carga un sistema KNN previamente guardado"""
        if not os.path.exists(filename):
            print(f"❌ Error: No se encuentra {filename}")
            return False
        
        with open(filename, 'rb') as f:
            datos = pickle.load(f)
        
        self.modelo_knn = datos['modelo_knn']
        self.scaler = datos['scaler']
        self.features_usadas = datos['features_usadas']
        self.k_vecinos = datos['k_vecinos']
        self.estadisticas = datos.get('estadisticas', {})
        self.datos_historicos = datos['datos_historicos']
        
        print(f"✅ Sistema KNN cargado desde: {filename}")
        print(f"   • {len(self.features_usadas)} features")
        print(f"   • {self.k_vecinos} vecinos")
        print(f"   • {len(self.datos_historicos)} patrones históricos")
        
        return True
    
    def evaluar_rendimiento(self, df_test=None, ventana_test=200):
        """
        Evalúa el rendimiento del sistema KNN con datos de prueba.
        
        Parámetros:
        -----------
        df_test : DataFrame (opcional)
            Datos de prueba. Si None, usa los últimos registros del histórico
        ventana_test : int
            Cantidad de registros a usar para testing
        
        Retorna:
        --------
        dict : Métricas de rendimiento
        """
        print("\n" + "="*70)
        print("📊 EVALUANDO RENDIMIENTO DEL SISTEMA KNN")
        print("="*70)
        
        if df_test is None:
            # Usar últimos registros del histórico
            df_test = self.datos_historicos.tail(ventana_test).copy()
        
        predicciones_correctas = 0
        total_predicciones = 0
        ganancias_acumuladas = 0
        
        resultados = []
        
        for idx in range(len(df_test)):
            # Obtener datos hasta este punto
            datos_actuales = df_test.iloc[idx]
            resultado_real = datos_actuales['accion_resultado']
            retorno_real = datos_actuales['retorno_futuro']
            
            # Obtener recomendación
            rec = self.obtener_recomendacion(datos_actuales, explicar=False)
            
            if rec:
                predicho = rec['accion']
                
                # Verificar si la predicción fue correcta
                if predicho == resultado_real:
                    predicciones_correctas += 1
                
                # Calcular ganancia/pérdida si se siguió la recomendación
                if predicho == 'COMPRA' and resultado_real == 'COMPRA':
                    ganancias_acumuladas += retorno_real
                elif predicho == 'VENTA' and resultado_real == 'VENTA':
                    ganancias_acumuladas += abs(retorno_real)
                elif predicho in ['COMPRA', 'VENTA'] and resultado_real != predicho:
                    ganancias_acumuladas -= abs(retorno_real)
                
                total_predicciones += 1
                
                resultados.append({
                    'predicho': predicho,
                    'real': resultado_real,
                    'correcto': predicho == resultado_real,
                    'ganancia': ganancias_acumuladas
                })
        
        accuracy = (predicciones_correctas / total_predicciones * 100) if total_predicciones > 0 else 0
        
        print(f"\n✅ Evaluación completada:")
        print(f"   • Predicciones totales: {total_predicciones}")
        print(f"   • Predicciones correctas: {predicciones_correctas}")
        print(f"   • Accuracy: {accuracy:.2f}%")
        print(f"   • Ganancia acumulada: {ganancias_acumuladas*100:.3f}%")
        
        return {
            'accuracy': accuracy,
            'predicciones_correctas': predicciones_correctas,
            'total_predicciones': total_predicciones,
            'ganancia_acumulada': ganancias_acumuladas * 100,
            'resultados': resultados
        }


def ejemplo_uso():
    """Ejemplo de cómo usar el sistema de recomendación KNN"""
    print("\n" + "╔" + "═"*68 + "╗")
    print("║" + " "*15 + "EJEMPLO DE USO - SISTEMA KNN" + " "*25 + "║")
    print("╚" + "═"*68 + "╝")
    
    # 1. Cargar datos históricos
    print("\n📂 Paso 1: Cargar datos históricos...")
    
    # Intentar cargar datos con oro
    if os.path.exists("datos/eurusd_con_oro.csv"):
        df = pd.read_csv("datos/eurusd_con_oro.csv")
        print(f"✅ Cargados {len(df)} registros con ORO")
    elif os.path.exists("datos/eurusd_con_sentimiento.csv"):
        df = pd.read_csv("datos/eurusd_con_sentimiento.csv")
        print(f"✅ Cargados {len(df)} registros con sentimiento")
    elif os.path.exists("datos/eurusd_datos.csv"):
        df = pd.read_csv("datos/eurusd_datos.csv")
        print(f"✅ Cargados {len(df)} registros básicos")
    else:
        print("❌ No hay datos disponibles. Ejecuta extraer_datos.py primero")
        return
    
    # 2. Crear features si no existen
    if 'MA_10' not in df.columns:
        print("\n🔧 Creando features técnicas...")
        df['MA_10'] = df['close'].rolling(window=10).mean()
        df['MA_30'] = df['close'].rolling(window=30).mean()
        df['MA_50'] = df['close'].rolling(window=50).mean()
        
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        df['Volatility'] = df['close'].rolling(window=20).std()
        df['HL_Range'] = df['high'] - df['low']
        df['Price_Change'] = df['close'].pct_change()
        df['Volume_MA'] = df['tick_volume'].rolling(window=20).mean()
        
        df = df.dropna()
        print(f"✅ Features creadas")
    
    # 3. Inicializar sistema KNN
    print("\n🎯 Paso 2: Inicializar sistema KNN...")
    sistema = SistemaRecomendacionKNN(k_vecinos=50, min_datos=500)
    
    # 4. Preparar datos históricos
    print("\n📊 Paso 3: Preparar datos históricos...")
    if sistema.preparar_datos_historicos(df, horizonte_prediccion=4):
        
        # 5. Guardar modelo
        sistema.guardar_modelo()
        
        # 6. Evaluar rendimiento
        metricas = sistema.evaluar_rendimiento(ventana_test=200)
        
        # 7. Obtener recomendación para el momento actual
        print("\n🔮 Paso 4: Obtener recomendación actual...")
        recomendacion = sistema.obtener_recomendacion(df, explicar=True)
        
        if recomendacion:
            sistema.mostrar_recomendacion(recomendacion)
        
        print("\n✅ EJEMPLO COMPLETADO!")
        print("💡 Ahora puedes usar el sistema KNN en prediccion_en_vivo.py")
    else:
        print("❌ No se pudo preparar el sistema KNN")


if __name__ == "__main__":
    ejemplo_uso()
