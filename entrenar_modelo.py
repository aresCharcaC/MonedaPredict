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

# Configurar estilo de gráficos
sns.set_style("darkgrid")
plt.rcParams['figure.figsize'] = (15, 8)

def cargar_datos(filename="datos/eurusd_datos.csv"):
    """Carga los datos desde el CSV"""
    
    print("📂 Cargando datos...")
    
    if not os.path.exists(filename):
        print(f"❌ Error: No se encuentra el archivo {filename}")
        print("👉 Primero ejecuta: extraer_datos.py")
        return None
    
    df = pd.read_csv(filename)
    print(f"✅ Datos cargados: {len(df)} registros")
    
    return df

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
    
    # Seleccionar features
    features = ['open', 'high', 'low', 'close', 'tick_volume', 
                'MA_10', 'MA_30', 'MA_50', 'RSI', 'Volatility', 
                'HL_Range', 'Price_Change', 'Volume_MA']
    
    data = df[features].values
    
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
    
    # 2. Crear features
    df = crear_features(df)
    
    # 3. Preparar datos para LSTM
    X_train, X_test, y_train, y_test, scaler = preparar_datos_lstm(df, look_back=60)
    
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
    print("👉 Ahora ejecuta: prediccion_en_vivo.py")

if __name__ == "__main__":
    main()