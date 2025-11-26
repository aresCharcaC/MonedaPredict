"""
ARCHIVO 3: PREDICCIÓN EN TIEMPO REAL
=====================================
Este script hace predicciones en vivo y genera señales de compra/venta
"""

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import pickle
from datetime import datetime
import time
import os
import sistema_knn  # Sistema de recomendación KNN

# Para alertas de sonido (opcional)
try:
    import winsound
    SONIDO_DISPONIBLE = True
except:
    SONIDO_DISPONIBLE = False
    print("⚠️ Alertas de sonido no disponibles (solo Windows)")

class PrediccionForex:
    """Clase para hacer predicciones en tiempo real"""
    
    def __init__(self, usar_knn=True):
        self.modelo = None
        self.scaler = None
        self.look_back = 60
        self.datos_historicos = []
        self.usar_knn = usar_knn
        self.sistema_knn = None
        
    def cargar_modelo(self):
        """Carga el modelo entrenado"""
        
        print("📂 Cargando modelo...")
        
        if not os.path.exists('modelos/lstm_model.h5'):
            print("❌ Error: No se encuentra el modelo")
            print("👉 Primero ejecuta: entrenar_modelo.py")
            return False
        
        # Cargar modelo
        self.modelo = load_model('modelos/lstm_model.h5')
        
        # Cargar scaler
        with open('modelos/scaler.pkl', 'rb') as f:
            self.scaler = pickle.load(f)
        
        print("✅ Modelo LSTM cargado exitosamente!")
        
        # Cargar sistema KNN si está disponible
        if self.usar_knn and os.path.exists('modelos/sistema_knn.pkl'):
            try:
                self.sistema_knn = sistema_knn.SistemaRecomendacionKNN()
                if self.sistema_knn.cargar_modelo('modelos/sistema_knn.pkl'):
                    print("✅ Sistema KNN cargado exitosamente!")
                else:
                    print("⚠️ No se pudo cargar sistema KNN")
                    self.sistema_knn = None
            except Exception as e:
                print(f"⚠️ Error al cargar KNN: {e}")
                self.sistema_knn = None
        else:
            if self.usar_knn:
                print("ℹ️ Sistema KNN no disponible (entrénalo con sistema_knn.py)")
        
        return True
    
    def conectar_mt5(self):
        """Conecta con MetaTrader5"""
        
        print("\n🔌 Conectando con MetaTrader5...")
        
        if not mt5.initialize():
            print("❌ Error al conectar con MT5")
            print("👉 Asegúrate de que MetaTrader5 esté ABIERTO")
            return False
        
        print("✅ Conectado a MT5!")
        return True
    
    def calcular_indicadores(self, df):
        """Calcula los indicadores técnicos"""
        
        # Medias móviles
        df['MA_10'] = df['close'].rolling(window=10).mean()
        df['MA_30'] = df['close'].rolling(window=30).mean()
        df['MA_50'] = df['close'].rolling(window=50).mean()
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Volatilidad
        df['Volatility'] = df['close'].rolling(window=20).std()
        
        # Rango Alto-Bajo
        df['HL_Range'] = df['high'] - df['low']
        
        # Cambio porcentual
        df['Price_Change'] = df['close'].pct_change()
        
        # Volumen medio
        df['Volume_MA'] = df['tick_volume'].rolling(window=20).mean()
        
        return df
    
    def obtener_datos_recientes(self, symbol="EURUSD", timeframe=mt5.TIMEFRAME_M15):
        """Obtiene los últimos datos de MT5"""
        
        # Obtener datos (necesitamos look_back + extra para indicadores)
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, self.look_back + 100)
        
        if rates is None:
            return None
        
        # Convertir a DataFrame
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        # Calcular indicadores
        df = self.calcular_indicadores(df)
        
        # Eliminar NaN
        df = df.dropna()
        
        return df
    
    def hacer_prediccion(self, df):
        """Hace la predicción del próximo precio"""
        
        # Features básicas (13)
        features = ['open', 'high', 'low', 'close', 'tick_volume', 
                   'MA_10', 'MA_30', 'MA_50', 'RSI', 'Volatility', 
                   'HL_Range', 'Price_Change', 'Volume_MA']
        
        # Features de ORO (9) - correlación con oro
        oro_features = ['close_oro', 'ratio_eur_oro', 'ratio_desviacion', 
                       'divergencia_retornos', 'oro_tendencia', 'ratio_volatilidad',
                       'correlacion', 'correlacion_ma', 'oro_momentum']
        
        # Rellenar features de oro con ceros si no están disponibles
        for feat in oro_features:
            if feat not in df.columns:
                df[feat] = 0.0
        
        # Combinar todas las features (13 + 9 = 22)
        features.extend(oro_features)
        
        # Tomar los últimos 'look_back' registros
        datos = df[features].tail(self.look_back).values
        
        # Normalizar
        datos_scaled = self.scaler.transform(datos)
        
        # Preparar para predicción
        X = datos_scaled.reshape(1, self.look_back, len(features))
        
        # Predecir
        prediccion_scaled = self.modelo.predict(X, verbose=0)
        
        # Desnormalizar
        dummy = np.zeros((1, self.scaler.n_features_in_))
        dummy[0, 3] = prediccion_scaled[0, 0]
        precio_predicho = self.scaler.inverse_transform(dummy)[0, 3]
        
        return precio_predicho
        
        # Tomar los últimos 'look_back' registros
        datos = df[features].tail(self.look_back).values
        
        # Normalizar
        datos_scaled = self.scaler.transform(datos)
        
        # Preparar para predicción
        X = datos_scaled.reshape(1, self.look_back, len(features))
        
        # Predecir
        prediccion_scaled = self.modelo.predict(X, verbose=0)
        
        # Desnormalizar
        dummy = np.zeros((1, self.scaler.n_features_in_))
        dummy[0, 3] = prediccion_scaled[0, 0]
        precio_predicho = self.scaler.inverse_transform(dummy)[0, 3]
        
        return precio_predicho
    
    def obtener_recomendacion_knn(self, df):
        """
        Obtiene recomendación del sistema KNN basado en patrones similares.
        
        Retorna:
        --------
        dict o None : Recomendación KNN si está disponible
        """
        if self.sistema_knn is None:
            return None
        
        try:
            recomendacion = self.sistema_knn.obtener_recomendacion(
                df, 
                explicar=False  # No mostrar patrones en tiempo real para ser más rápido
            )
            return recomendacion
        except Exception as e:
            print(f"⚠️ Error en KNN: {e}")
            return None
    
    def generar_senal(self, precio_actual, precio_predicho, df=None, umbral=0.0001):
        """
        Genera señal de trading combinando LSTM y KNN (si disponible).
        
        umbral: cambio mínimo para generar señal (en pips aprox)
        df: DataFrame con datos actuales (para KNN)
        """
        
        diferencia = precio_predicho - precio_actual
        porcentaje = (diferencia / precio_actual) * 100
        
        # Señal base del LSTM
        if diferencia > umbral:
            senal_lstm = "COMPRAR"
            emoji = "📈"
        elif diferencia < -umbral:
            senal_lstm = "VENDER"
            emoji = "📉"
        else:
            senal_lstm = "ESPERAR"
            emoji = "➡️"
        
        # Confianza base del LSTM
        confianza_lstm = min(abs(porcentaje) * 1000, 100)
        
        # Obtener recomendación KNN si está disponible
        recomendacion_knn = None
        if df is not None and self.sistema_knn is not None:
            recomendacion_knn = self.obtener_recomendacion_knn(df)
        
        # Combinar señales LSTM + KNN
        if recomendacion_knn:
            accion_knn = recomendacion_knn['accion']
            confianza_knn = recomendacion_knn['confianza']
            
            # Si ambos sistemas coinciden, aumentar confianza
            if senal_lstm == accion_knn:
                confianza_final = min((confianza_lstm * 0.4 + confianza_knn * 0.6), 100)
                senal_final = senal_lstm
                metodo = "LSTM+KNN (Concordancia ✅)"
            # Si difieren, usar el de mayor confianza
            elif confianza_knn > confianza_lstm:
                confianza_final = confianza_knn * 0.8  # Penalizar ligeramente por conflicto
                senal_final = accion_knn
                metodo = "KNN (Mayor confianza)"
                # Actualizar emoji según KNN
                if accion_knn == "COMPRAR":
                    emoji = "📈"
                elif accion_knn == "VENDER":
                    emoji = "📉"
                else:
                    emoji = "➡️"
            else:
                confianza_final = confianza_lstm * 0.8
                senal_final = senal_lstm
                metodo = "LSTM (Mayor confianza)"
        else:
            # Solo LSTM
            confianza_final = confianza_lstm
            senal_final = senal_lstm
            metodo = "LSTM"
        
        # Formatear señal con color
        if senal_final == "COMPRAR":
            senal = "🟢 COMPRAR"
        elif senal_final == "VENDER":
            senal = "🔴 VENDER"
        else:
            senal = "⚪ ESPERAR"
        
        resultado = {
            'senal': senal,
            'emoji': emoji,
            'diferencia': diferencia,
            'porcentaje': porcentaje,
            'confianza': confianza_final,
            'metodo': metodo
        }
        
        # Agregar info KNN si está disponible
        if recomendacion_knn:
            resultado['knn_accion'] = recomendacion_knn['accion']
            resultado['knn_confianza'] = recomendacion_knn['confianza']
            resultado['knn_retorno_esperado'] = recomendacion_knn['retorno_esperado']
            resultado['knn_vecinos_compra'] = recomendacion_knn['vecinos_compra']
            resultado['knn_vecinos_venta'] = recomendacion_knn['vecinos_venta']
        
        return resultado
    
    def alerta_sonido(self, tipo_senal):
        """Emite alerta sonora"""
        
        if not SONIDO_DISPONIBLE:
            return
        
        try:
            if "COMPRAR" in tipo_senal:
                # Sonido agudo para compra
                winsound.Beep(1000, 200)
            elif "VENDER" in tipo_senal:
                # Sonido grave para venta
                winsound.Beep(500, 200)
        except:
            pass
    
    def guardar_registro(self, datos):
        """Guarda registro de señales"""
        
        # Crear carpeta si no existe
        os.makedirs("registros", exist_ok=True)
        
        # Crear DataFrame con el registro
        registro = pd.DataFrame([datos])
        
        # Agregar al archivo
        filename = "registros/señales.csv"
        
        if os.path.exists(filename):
            registro.to_csv(filename, mode='a', header=False, index=False)
        else:
            registro.to_csv(filename, index=False)
    
    def monitorear(self, symbol="EURUSD", timeframe=mt5.TIMEFRAME_M15, intervalo=30):
        """
        Monitorea el mercado y hace predicciones
        
        symbol: Par de divisas
        timeframe: Periodo de tiempo
        intervalo: Cada cuántos segundos actualizar (default: 30)
        """
        
        print("\n" + "="*80)
        print("🤖 SISTEMA DE PREDICCIÓN EN TIEMPO REAL")
        print("="*80)
        print(f"📊 Par: {symbol}")
        print(f"⏱️ Timeframe: {self._get_timeframe_name(timeframe)}")
        print(f"🔄 Actualización cada: {intervalo} segundos")
        print("="*80)
        print("\n⚠️ Presiona Ctrl+C para detener\n")
        
        contador = 0
        
        try:
            while True:
                contador += 1
                
                # Obtener hora actual
                ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Obtener datos
                df = self.obtener_datos_recientes(symbol, timeframe)
                
                if df is None:
                    print(f"❌ [{ahora}] Error al obtener datos")
                    time.sleep(intervalo)
                    continue
                
                # Precio actual
                precio_actual = df['close'].iloc[-1]
                
                # Hacer predicción LSTM
                precio_predicho = self.hacer_prediccion(df)
                
                # Generar señal (combinando LSTM + KNN)
                resultado = self.generar_senal(precio_actual, precio_predicho, df)
                
                # Mostrar resultados
                print("─" * 80)
                print(f"🕐 Tiempo: {ahora} | Iteración: {contador}")
                print(f"💵 Precio Actual:    {precio_actual:.5f}")
                print(f"🔮 Precio Predicho:  {precio_predicho:.5f}")
                print(f"📊 Diferencia:       {resultado['diferencia']:.5f} ({resultado['porcentaje']:.3f}%)")
                print(f"🎯 Confianza:        {resultado['confianza']:.1f}%")
                print(f"⚙️ Método:           {resultado['metodo']}")
                
                # Mostrar info KNN si está disponible
                if 'knn_accion' in resultado:
                    print(f"\n🔍 Análisis KNN:")
                    print(f"   Recomendación: {resultado['knn_accion']}")
                    print(f"   Confianza KNN: {resultado['knn_confianza']:.1f}%")
                    print(f"   Retorno esperado: {resultado['knn_retorno_esperado']:.3f}%")
                    print(f"   Vecinos COMPRA: {resultado['knn_vecinos_compra']} | VENTA: {resultado['knn_vecinos_venta']}")
                
                print(f"\n{resultado['emoji']} SEÑAL: {resultado['senal']}")
                print("─" * 80)
                
                # Alerta sonora si hay señal de compra/venta
                if "ESPERAR" not in resultado['senal']:
                    self.alerta_sonido(resultado['senal'])
                    print("🔔 ¡ALERTA ACTIVADA!")
                
                # Guardar registro
                registro = {
                    'timestamp': ahora,
                    'precio_actual': precio_actual,
                    'precio_predicho': precio_predicho,
                    'diferencia': resultado['diferencia'],
                    'porcentaje': resultado['porcentaje'],
                    'senal': resultado['senal'],
                    'confianza': resultado['confianza']
                }
                self.guardar_registro(registro)
                
                # Esperar
                time.sleep(intervalo)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoreo detenido por el usuario")
            print(f"📊 Total de iteraciones: {contador}")
            print(f"📁 Registros guardados en: registros/señales.csv")
    
    def _get_timeframe_name(self, timeframe):
        """Obtiene el nombre del timeframe"""
        timeframes = {
            mt5.TIMEFRAME_M5: "5 minutos",
            mt5.TIMEFRAME_M15: "15 minutos",
            mt5.TIMEFRAME_M30: "30 minutos",
            mt5.TIMEFRAME_H1: "1 hora",
            mt5.TIMEFRAME_H4: "4 horas",
            mt5.TIMEFRAME_D1: "1 día"
        }
        return timeframes.get(timeframe, "Desconocido")

def main():
    """Función principal"""
    
    # Crear instancia
    predictor = PrediccionForex()
    
    # Cargar modelo
    if not predictor.cargar_modelo():
        return
    
    # Conectar MT5
    if not predictor.conectar_mt5():
        return
    
    # Iniciar monitoreo
    try:
        predictor.monitorear(
            symbol="EURUSD",              # Par de divisas
            timeframe=mt5.TIMEFRAME_M15,   # 15 minutos
            intervalo=30                   # Actualizar cada 30 segundos
        )
    finally:
        mt5.shutdown()
        print("\n🔌 Conexión cerrada")

if __name__ == "__main__":
    main()