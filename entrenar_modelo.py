"""
ARCHIVO 2: ENTRENAR MODELO DE PREDICCIÓN
=========================================
Este script lee los datos y entrena un modelo LSTM para predecir EUR/USD
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import os
import pickle
import correlacion_oro  # Módulo de correlación con oro

# Configurar estilo de gráficos
sns.set_style("darkgrid")
plt.rcParams['figure.figsize'] = (15, 8)

def cargar_datos(filename="datos/eurusd_con_sentimiento.csv"):
    """Carga los datos desde el CSV (con sentimiento de noticias si está disponible)"""
    
    print("📂 Cargando datos...")
    
    # Prioridad 1: Intentar cargar datos con oro y sentimiento
    filename_oro_sent = "datos/eurusd_con_oro.csv"
    if os.path.exists(filename_oro_sent):
        df = pd.read_csv(filename_oro_sent)
        # Verificar si tiene features de oro
        if 'close_oro' in df.columns or 'ratio_eur_oro' in df.columns:
            print(f"✅ Datos con ORO cargados: {len(df)} registros")
            print("🥇 Incluye correlación con ORO (XAU/USD)")
            
            # Verificar si también tiene sentimiento
            if 'sent_mean' in df.columns:
                print("📰 También incluye análisis de noticias")
            
            return df
    
    # Prioridad 2: Intentar cargar datos con sentimiento
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        print(f"✅ Datos con sentimiento cargados: {len(df)} registros")
        print("📰 Incluye análisis de noticias")
        print("⚠️ Sin datos de ORO (ejecuta extraer_datos.py para agregarlo)")
        return df
    
    # Prioridad 3: Fallback a datos sin sentimiento
    filename_simple = "datos/eurusd_datos.csv"
    if os.path.exists(filename_simple):
        df = pd.read_csv(filename_simple)
        print(f"✅ Datos básicos cargados: {len(df)} registros")
        print("⚠️ Sin análisis de noticias (ejecuta noticias/integrar_modelo.py para agregarlo)")
        print("⚠️ Sin correlación con ORO (ejecuta extraer_datos.py para agregarlo)")
        return df
    
    print(f"❌ Error: No se encuentra ningún archivo de datos")
    print("👉 Primero ejecuta: extraer_datos.py")
    return None

def crear_features(df):
    """Crea características adicionales para el modelo"""
    
    print("\n🔧 Creando características...")
    
    # Calcular indicadores técnicos
    
    # 1. Medias móviles
    df['MA_10'] = df['close'].rolling(window=10).mean()
    df['MA_30'] = df['close'].rolling(window=30).mean()
    df['MA_50'] = df['close'].rolling(window=50).mean()
    
    # 2. RSI (Relative Strength Index)
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # 3. Volatilidad
    df['Volatility'] = df['close'].rolling(window=20).std()
    
    # 4. Rango Alto-Bajo
    df['HL_Range'] = df['high'] - df['low']
    
    # 5. Cambio porcentual
    df['Price_Change'] = df['close'].pct_change()
    
    # 6. Volumen medio
    df['Volume_MA'] = df['tick_volume'].rolling(window=20).mean()
    
    # Eliminar filas con NaN
    df = df.dropna()
    
    print(f"✅ Features creadas. Registros válidos: {len(df)}")
    
    return df

def preparar_datos_lstm(df, look_back=60):
    """
    Prepara los datos para LSTM
    
    look_back: cuántas velas hacia atrás usar para predecir (default: 60)
    """
    
    print(f"\n📊 Preparando datos para LSTM (look_back={look_back})...")
    
    # Seleccionar features base
    features = ['open', 'high', 'low', 'close', 'tick_volume', 
                'MA_10', 'MA_30', 'MA_50', 'RSI', 'Volatility', 
                'HL_Range', 'Price_Change', 'Volume_MA']
    
    # Agregar features de oro si están disponibles
    oro_features = correlacion_oro.obtener_features_oro()
    available_oro = [f for f in oro_features if f in df.columns]
    
    if available_oro:
        features.extend(available_oro)
        print(f"🥇 Features de ORO agregadas: {len(available_oro)}")
        print(f"   {', '.join(available_oro)}")
    else:
        print("⚠️ Sin features de ORO (modelo sin correlación con oro)")
    
    # Agregar features de sentimiento si están disponibles
    sentiment_features = ['sent_mean', 'impact_mean', 'sent_balance', 
                         'sent_ma_24h', 'sent_trend']
    
    available_sentiment = [f for f in sentiment_features if f in df.columns]
    
    if available_sentiment:
        features.extend(available_sentiment)
        print(f"📰 Features de noticias agregadas: {len(available_sentiment)}")
        print(f"   {', '.join(available_sentiment)}")
    else:
        print("⚠️ Sin features de sentimiento (modelo básico)")
    
    print(f"\n📋 Total de features: {len(features)}")
    
    # Verificar que las features existen en el DataFrame
    missing_features = [f for f in features if f not in df.columns]
    if missing_features:
        print(f"⚠️ Features faltantes: {missing_features}")
        print(f"📋 Columnas disponibles en DataFrame: {list(df.columns)}")
    
    # Filtrar solo features que existen
    available_features = [f for f in features if f in df.columns]
    
    if len(available_features) == 0:
        print(f"❌ Error: No hay features disponibles")
        print(f"   Features esperadas: {features}")
        print(f"   Columnas en DF: {list(df.columns)}")
        return None, None, None, None, None
    
    print(f"✅ Features disponibles: {len(available_features)}/{len(features)}")
    
    # Verificar que hay datos
    print(f"📊 Registros en DataFrame antes de extraer features: {len(df)}")
    
    data = df[available_features].values
    
    print(f"📊 Datos extraídos: {data.shape}")
    
    if len(data) == 0:
        print(f"❌ Error: DataFrame vacío después de extraer features")
        return None, None, None, None, None
    
    # Normalizar datos (importante para redes neuronales)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    
    # Crear secuencias
    X, y = [], []
    
    for i in range(look_back, len(scaled_data)):
        X.append(scaled_data[i-look_back:i])  # Últimas 'look_back' velas
        y.append(scaled_data[i, 3])  # Predecir 'close' (índice 3)
    
    X, y = np.array(X), np.array(y)
    
    print(f"✅ Forma de X: {X.shape}")
    print(f"✅ Forma de y: {y.shape}")
    
    # Dividir en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False  # shuffle=False para mantener orden temporal
    )
    
    print(f"📚 Datos de entrenamiento: {len(X_train)}")
    print(f"🧪 Datos de prueba: {len(X_test)}")
    
    return X_train, X_test, y_train, y_test, scaler

def crear_modelo_lstm(input_shape):
    """Crea el modelo LSTM"""
    
    print("\n🧠 Construyendo modelo LSTM...")
    
    model = Sequential([
        # Primera capa LSTM
        LSTM(units=100, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        
        # Segunda capa LSTM
        LSTM(units=100, return_sequences=True),
        Dropout(0.2),
        
        # Tercera capa LSTM
        LSTM(units=50, return_sequences=False),
        Dropout(0.2),
        
        # Capas densas
        Dense(units=25),
        Dense(units=1)  # Salida: predicción del precio
    ])
    
    # Compilar modelo
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
    
    print("✅ Modelo creado!")
    model.summary()
    
    return model

def entrenar_modelo(model, X_train, y_train, X_test, y_test):
    """Entrena el modelo"""
    
    print("\n🏋️ Entrenando modelo...")
    print("⏳ Esto puede tardar varios minutos...")
    
    # Early stopping para evitar overfitting
    early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    
    # Entrenar
    history = model.fit(
        X_train, y_train,
        batch_size=32,
        epochs=50,  # Puedes aumentar a 100 si quieres mejor precisión
        validation_data=(X_test, y_test),
        callbacks=[early_stop],
        verbose=1
    )
    
    print("\n✅ Entrenamiento completado!")
    
    return history

def evaluar_modelo(model, X_test, y_test, scaler):
    """Evalúa el modelo"""
    
    print("\n📊 Evaluando modelo...")
    
    # Hacer predicciones
    predictions = model.predict(X_test)
    
    # Desnormalizar para ver valores reales
    # Crear array con forma correcta para inverse_transform
    dummy = np.zeros((len(predictions), scaler.n_features_in_))
    dummy[:, 3] = predictions.flatten()  # Poner predicciones en columna 'close'
    predictions_real = scaler.inverse_transform(dummy)[:, 3]
    
    dummy_test = np.zeros((len(y_test), scaler.n_features_in_))
    dummy_test[:, 3] = y_test
    y_test_real = scaler.inverse_transform(dummy_test)[:, 3]
    
    # Calcular métricas
    mae = np.mean(np.abs(predictions_real - y_test_real))
    rmse = np.sqrt(np.mean((predictions_real - y_test_real)**2))
    
    print(f"✅ MAE (Error Absoluto Medio): {mae:.5f}")
    print(f"✅ RMSE (Raíz del Error Cuadrático): {rmse:.5f}")
    
    # Graficar resultados
    plt.figure(figsize=(15, 6))
    plt.plot(y_test_real, label='Precio Real', color='blue', linewidth=2)
    plt.plot(predictions_real, label='Predicción', color='red', linewidth=2, alpha=0.7)
    plt.title('Predicciones vs Valores Reales', fontsize=16, fontweight='bold')
    plt.xlabel('Tiempo', fontsize=12)
    plt.ylabel('Precio EUR/USD', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('datos/predicciones_vs_real.png', dpi=300)
    print("📊 Gráfico guardado: datos/predicciones_vs_real.png")
    
    return mae, rmse

def guardar_modelo(model, scaler):
    """Guarda el modelo entrenado"""
    
    print("\n💾 Guardando modelo...")
    
    # Crear carpeta
    os.makedirs("modelos", exist_ok=True)
    
    # Guardar modelo
    model.save('modelos/lstm_model.h5')
    
    # Guardar scaler
    with open('modelos/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    print("✅ Modelo guardado en: modelos/lstm_model.h5")
    print("✅ Scaler guardado en: modelos/scaler.pkl")

def main():
    """Función principal"""
    
    print("="*60)
    print("🚀 ENTRENAMIENTO DE MODELO DE PREDICCIÓN")
    print("="*60)
    
    # 1. Cargar datos
    df = cargar_datos()
    if df is None:
        return
    
    print(f"\n📊 Datos cargados: {len(df)} registros")
    print(f"📋 Columnas: {list(df.columns)}")
    
    # 2. Crear features
    df = crear_features(df)
    
    print(f"\n📊 Después de crear features: {len(df)} registros")
    
    if len(df) < 100:
        print(f"❌ Error: Muy pocos datos ({len(df)} registros)")
        print("👉 Se necesitan al menos 100 registros para entrenar")
        print("💡 Ejecuta: python extraer_datos.py con más CANTIDAD_DATOS")
        return
    
    # 3. Preparar datos para LSTM
    result = preparar_datos_lstm(df, look_back=60)
    
    if result[0] is None:
        print("❌ Error al preparar datos")
        return
    
    X_train, X_test, y_train, y_test, scaler = result
    
    # 4. Crear modelo
    model = crear_modelo_lstm(input_shape=(X_train.shape[1], X_train.shape[2]))
    
    # 5. Entrenar modelo
    history = entrenar_modelo(model, X_train, y_train, X_test, y_test)
    
    # 6. Evaluar modelo
    evaluar_modelo(model, X_test, y_test, scaler)
    
    # 7. Guardar modelo
    guardar_modelo(model, scaler)
    
    print("\n" + "="*60)
    print("✅ ENTRENAMIENTO COMPLETADO!")
    print("="*60)
    print("\n💡 RECOMENDACIONES:")
    print("   • Para actualizar noticias: python noticias/obtener_noticias.py")
    print("   • Para predicciones en vivo: python prediccion_en_vivo.py")
    print("   • Para visualizar resultados: python visualizar_resultados.py")

if __name__ == "__main__":
    main()