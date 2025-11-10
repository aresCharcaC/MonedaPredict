"""
GENERADOR DE SEÑALES PARA COPIAR EN IQ OPTION
==============================================
Este código te da señales con precios EXACTOS para que las copies manualmente
"""

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import pickle
from datetime import datetime
import time
import os
import config  # Importar configuración

class GeneradorSeñales:
    """Genera señales para copiar manualmente en IQ Option"""
    
    def __init__(self):
        self.modelo = None
        self.scaler = None
        self.look_back = config.LOOK_BACK
        
        # CONFIGURACIÓN desde config.py
        self.take_profit_pips = config.TAKE_PROFIT_PIPS
        self.stop_loss_pips = config.STOP_LOSS_PIPS
        self.confianza_minima = config.CONFIANZA_MINIMA
        
    def cargar_modelo(self):
        """Carga el modelo"""
        print("📂 Cargando modelo...")
        
        if not os.path.exists('modelos/lstm_model.h5'):
            print("❌ Error: No se encuentra el modelo")
            print("👉 Primero ejecuta: entrenar_modelo.py")
            return False
        
        self.modelo = load_model('modelos/lstm_model.h5')
        with open('modelos/scaler.pkl', 'rb') as f:
            self.scaler = pickle.load(f)
        
        print("✅ Modelo cargado!")
        return True
    
    def conectar_mt5(self):
        """Conecta con MT5"""
        print("🔌 Conectando con MetaTrader5...")
        
        if not mt5.initialize():
            print("❌ No se pudo conectar con MT5")
            print("👉 Abre MetaTrader5 primero")
            return False
        
        print("✅ Conectado!")
        return True
    
    def calcular_indicadores(self, df):
        """Calcula indicadores técnicos"""
        
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
        df['HL_Range'] = df['high'] - df['low']
        df['Price_Change'] = df['close'].pct_change()
        df['Volume_MA'] = df['tick_volume'].rolling(window=20).mean()
        
        # Bollinger Bands (detecta ciclos)
        df['BB_Middle'] = df['close'].rolling(window=20).mean()
        df['BB_Std'] = df['close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (df['BB_Std'] * 2)
        df['BB_Lower'] = df['BB_Middle'] - (df['BB_Std'] * 2)
        
        return df
    
    def obtener_datos(self, symbol="EURUSD", timeframe=mt5.TIMEFRAME_H4):
        """Obtiene datos de MT5"""
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, self.look_back + 100)
        
        if rates is None:
            return None
        
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = self.calcular_indicadores(df)
        df = df.dropna()
        
        return df
    
    def hacer_prediccion(self, df):
        """Predice el precio futuro"""
        features = ['open', 'high', 'low', 'close', 'tick_volume', 
                   'MA_10', 'MA_30', 'MA_50', 'RSI', 'Volatility', 
                   'HL_Range', 'Price_Change', 'Volume_MA']
        
        datos = df[features].tail(self.look_back).values
        datos_scaled = self.scaler.transform(datos)
        X = datos_scaled.reshape(1, self.look_back, len(features))
        
        prediccion_scaled = self.modelo.predict(X, verbose=0)
        
        dummy = np.zeros((1, self.scaler.n_features_in_))
        dummy[0, 3] = prediccion_scaled[0, 0]
        precio_predicho = self.scaler.inverse_transform(dummy)[0, 3]
        
        return precio_predicho
    
    def generar_senal(self, df, precio_actual):
        """Genera la señal con todos los detalles"""
        
        # Predicción
        precio_predicho = self.hacer_prediccion(df)
        diferencia = precio_predicho - precio_actual
        porcentaje = (diferencia / precio_actual) * 100
        
        # Calcular confianza
        confianza = min(abs(porcentaje) * 1000, 100)
        
        # Analizar ciclos
        ultima_fila = df.iloc[-1]
        en_zona_baja = precio_actual <= ultima_fila['BB_Lower']
        en_zona_alta = precio_actual >= ultima_fila['BB_Upper']
        rsi = ultima_fila['RSI']
        
        # Ajustar confianza con ciclos
        if en_zona_baja and diferencia > 0:
            confianza = min(confianza * 1.3, 100)
        if en_zona_alta and diferencia < 0:
            confianza = min(confianza * 1.3, 100)
        if rsi < 30 and diferencia > 0:
            confianza = min(confianza * 1.2, 100)
        if rsi > 70 and diferencia < 0:
            confianza = min(confianza * 1.2, 100)
        
        # Determinar acción
        if diferencia > 0.0002 and confianza >= self.confianza_minima:
            accion = "COMPRAR"
            # Calcular TP y SL para COMPRA
            precio_entrada = precio_actual
            take_profit = precio_entrada + (self.take_profit_pips * 0.0001)
            stop_loss = precio_entrada - (self.stop_loss_pips * 0.0001)
            
        elif diferencia < -0.0002 and confianza >= self.confianza_minima:
            accion = "VENDER"
            # Calcular TP y SL para VENTA
            precio_entrada = precio_actual
            take_profit = precio_entrada - (self.take_profit_pips * 0.0001)
            stop_loss = precio_entrada + (self.stop_loss_pips * 0.0001)
        else:
            accion = "ESPERAR"
            precio_entrada = precio_actual
            take_profit = None
            stop_loss = None
        
        return {
            'accion': accion,
            'precio_actual': precio_actual,
            'precio_predicho': precio_predicho,
            'precio_entrada': precio_entrada,
            'take_profit': take_profit,
            'stop_loss': stop_loss,
            'diferencia': diferencia,
            'confianza': confianza,
            'rsi': rsi,
            'en_zona_baja': en_zona_baja,
            'en_zona_alta': en_zona_alta
        }
    
    def mostrar_senal(self, senal, ahora):
        """Muestra la señal de forma clara para copiar"""
        
        print("\n" + "═"*80)
        print("🎯 SEÑAL DE TRADING - COPIA EN IQ OPTION")
        print("═"*80)
        print(f"📅 Fecha/Hora: {ahora}")
        print(f"💵 Precio Actual: {senal['precio_actual']:.5f}")
        print(f"🔮 Precio Predicho: {senal['precio_predicho']:.5f}")
        print(f"📊 Diferencia: {senal['diferencia']:.5f}")
        print(f"🎲 Confianza: {senal['confianza']:.1f}%")
        print(f"📈 RSI: {senal['rsi']:.1f}")
        
        # Info de ciclos
        if senal['en_zona_baja']:
            print("🔵 ZONA BAJA detectada (posible rebote al alza)")
        if senal['en_zona_alta']:
            print("🔴 ZONA ALTA detectada (posible corrección a la baja)")
        
        print("\n" + "─"*80)
        
        if senal['accion'] == "COMPRAR":
            print("🟢 ACCIÓN: COMPRAR (BUY)")
            print("─"*80)
            print(f"📍 Precio de Entrada:  {senal['precio_entrada']:.5f}")
            print(f"✅ Take Profit (TP):   {senal['take_profit']:.5f}  (+{self.take_profit_pips} pips)")
            print(f"❌ Stop Loss (SL):     {senal['stop_loss']:.5f}  (-{self.stop_loss_pips} pips)")
            print("─"*80)
            print("\n📝 COPIA ESTO EN IQ OPTION:")
            print(f"   Tipo: COMPRAR / BUY")
            print(f"   Entrada: {senal['precio_entrada']:.5f}")
            print(f"   TP: {senal['take_profit']:.5f}")
            print(f"   SL: {senal['stop_loss']:.5f}")
            
        elif senal['accion'] == "VENDER":
            print("🔴 ACCIÓN: VENDER (SELL)")
            print("─"*80)
            print(f"📍 Precio de Entrada:  {senal['precio_entrada']:.5f}")
            print(f"✅ Take Profit (TP):   {senal['take_profit']:.5f}  (-{self.take_profit_pips} pips)")
            print(f"❌ Stop Loss (SL):     {senal['stop_loss']:.5f}  (+{self.stop_loss_pips} pips)")
            print("─"*80)
            print("\n📝 COPIA ESTO EN IQ OPTION:")
            print(f"   Tipo: VENDER / SELL")
            print(f"   Entrada: {senal['precio_entrada']:.5f}")
            print(f"   TP: {senal['take_profit']:.5f}")
            print(f"   SL: {senal['stop_loss']:.5f}")
            
        else:
            print("⚪ ACCIÓN: ESPERAR")
            print("─"*80)
            print("No hay señal clara en este momento.")
            print(f"Razón: Confianza baja ({senal['confianza']:.1f}% < {self.confianza_minima}%)")
        
        print("═"*80 + "\n")
    
    def guardar_senal(self, senal, ahora):
        """Guarda la señal en CSV"""
        os.makedirs("registros", exist_ok=True)
        
        datos = {
            'timestamp': ahora,
            'accion': senal['accion'],
            'precio_actual': senal['precio_actual'],
            'precio_predicho': senal['precio_predicho'],
            'precio_entrada': senal['precio_entrada'],
            'take_profit': senal['take_profit'],
            'stop_loss': senal['stop_loss'],
            'confianza': senal['confianza'],
            'rsi': senal['rsi']
        }
        
        df = pd.DataFrame([datos])
        filename = "registros/señales_iqoption.csv"
        
        if os.path.exists(filename):
            df.to_csv(filename, mode='a', header=False, index=False)
        else:
            df.to_csv(filename, index=False)
    
    def ejecutar(self, symbol=None, timeframe=None, revisar_cada_minutos=None):
        """
        Ejecuta el generador de señales
        
        Los parámetros se toman de config.py si no se especifican
        """
        
        # Usar valores de config.py si no se especifican
        symbol = symbol or config.PAR_DIVISAS
        timeframe = timeframe or config.get_timeframe_mt5()
        revisar_cada_minutos = revisar_cada_minutos or config.REVISAR_CADA_MINUTOS
        
        print("\n" + "═"*80)
        print("🤖 GENERADOR DE SEÑALES PARA IQ OPTION")
        print("═"*80)
        print(f"📊 Par: {symbol}")
        print(f"⏱️ Timeframe: {config.TIMEFRAME}")
        print(f"🔄 Actualización cada: {revisar_cada_minutos} minutos")
        print(f"🎯 Take Profit: {self.take_profit_pips} pips")
        print(f"🛡️ Stop Loss: {self.stop_loss_pips} pips")
        print(f"📊 Confianza mínima: {self.confianza_minima}%")
        print("═"*80)
        print("\n💡 TIP: Copia los valores exactos que aparecen en cada señal")
        print("⚠️ Presiona Ctrl+C para detener\n")
        
        iteracion = 0
        
        try:
            while True:
                iteracion += 1
                ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                print(f"\n🔄 Iteración {iteracion} - {ahora}")
                print("⏳ Analizando mercado...")
                
                # Obtener datos
                df = self.obtener_datos(symbol, timeframe)
                
                if df is None:
                    print("❌ Error al obtener datos")
                    time.sleep(revisar_cada_minutos * 60)
                    continue
                
                # Obtener precio actual
                tick = mt5.symbol_info_tick(symbol)
                if tick is None:
                    print("❌ Error al obtener precio")
                    time.sleep(revisar_cada_minutos * 60)
                    continue
                
                precio_actual = tick.bid
                
                # Generar señal
                senal = self.generar_senal(df, precio_actual)
                
                # Mostrar señal
                self.mostrar_senal(senal, ahora)
                
                # Guardar señal
                self.guardar_senal(senal, ahora)
                
                # Esperar
                print(f"💤 Esperando {revisar_cada_minutos} minutos hasta la próxima revisión...")
                print(f"📁 Señal guardada en: registros/señales_iqoption.csv\n")
                
                time.sleep(revisar_cada_minutos * 60)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Generador detenido")
            print(f"📊 Total de iteraciones: {iteracion}")
            print("📁 Todas las señales guardadas en: registros/señales_iqoption.csv")


def main():
    """Función principal"""
    
    generador = GeneradorSeñales()
    
    # Cargar modelo
    if not generador.cargar_modelo():
        return
    
    # Conectar MT5
    if not generador.conectar_mt5():
        return
    
    # Ejecutar
    try:
        generador.ejecutar()  # Usa config.py automáticamente
    finally:
        mt5.shutdown()
        print("🔌 Conexión cerrada")


if __name__ == "__main__":
    main()