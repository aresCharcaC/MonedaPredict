"""
ARCHIVO BONUS: VISUALIZADOR DE RESULTADOS
==========================================
Este script lee los registros y crea gráficos bonitos para tu presentación
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)

def cargar_registros():
    """Carga los registros de señales"""
    
    filename = "registros/señales.csv"
    
    if not os.path.exists(filename):
        print("❌ No hay registros aún")
        print("👉 Primero ejecuta: prediccion_en_vivo.py")
        return None
    
    df = pd.read_csv(filename)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    print(f"✅ Registros cargados: {len(df)} señales")
    
    return df

def crear_dashboard(df):
    """Crea un dashboard completo"""
    
    print("\n📊 Creando dashboard...")
    
    # Crear figura con subplots
    fig = plt.figure(figsize=(18, 12))
    
    # 1. GRÁFICO: Precio actual vs Predicho
    ax1 = plt.subplot(3, 2, 1)
    ax1.plot(df['timestamp'], df['precio_actual'], label='Precio Real', 
             color='blue', linewidth=2, marker='o', markersize=3)
    ax1.plot(df['timestamp'], df['precio_predicho'], label='Precio Predicho', 
             color='red', linewidth=2, linestyle='--', marker='s', markersize=3, alpha=0.7)
    ax1.set_title('💹 Precio Real vs Predicción', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel('Precio EUR/USD')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    # 2. GRÁFICO: Diferencia entre precio real y predicho
    ax2 = plt.subplot(3, 2, 2)
    colores = ['green' if x > 0 else 'red' for x in df['diferencia']]
    ax2.bar(df['timestamp'], df['diferencia'], color=colores, alpha=0.6)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax2.set_title('📊 Error de Predicción', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Tiempo')
    ax2.set_ylabel('Diferencia (Predicho - Real)')
    ax2.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    # 3. GRÁFICO: Distribución de señales
    ax3 = plt.subplot(3, 2, 3)
    conteo_senales = df['senal'].value_counts()
    colores_senal = {'🟢 COMPRAR': 'green', '🔴 VENDER': 'red', '⚪ ESPERAR': 'gray'}
    colores_plot = [colores_senal.get(s, 'blue') for s in conteo_senales.index]
    ax3.bar(conteo_senales.index, conteo_senales.values, color=colores_plot, alpha=0.7)
    ax3.set_title('🎯 Distribución de Señales', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Tipo de Señal')
    ax3.set_ylabel('Cantidad')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Agregar valores encima de las barras
    for i, v in enumerate(conteo_senales.values):
        ax3.text(i, v + 0.5, str(v), ha='center', va='bottom', fontweight='bold')
    
    # 4. GRÁFICO: Confianza de las predicciones
    ax4 = plt.subplot(3, 2, 4)
    ax4.plot(df['timestamp'], df['confianza'], color='purple', 
             linewidth=2, marker='o', markersize=4)
    ax4.axhline(y=50, color='orange', linestyle='--', label='Umbral 50%')
    ax4.fill_between(df['timestamp'], 0, df['confianza'], alpha=0.3, color='purple')
    ax4.set_title('🎲 Nivel de Confianza', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Tiempo')
    ax4.set_ylabel('Confianza (%)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    # 5. GRÁFICO: Porcentaje de cambio esperado
    ax5 = plt.subplot(3, 2, 5)
    ax5.scatter(df['timestamp'], df['porcentaje'], 
                c=df['confianza'], cmap='RdYlGn', s=100, alpha=0.6)
    ax5.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax5.set_title('📈 Cambio Porcentual Predicho', fontsize=14, fontweight='bold')
    ax5.set_xlabel('Tiempo')
    ax5.set_ylabel('Cambio (%)')
    ax5.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.colorbar(ax5.collections[0], ax=ax5, label='Confianza')
    
    # 6. TABLA: Estadísticas resumen
    ax6 = plt.subplot(3, 2, 6)
    ax6.axis('off')
    
    # Calcular estadísticas
    stats = {
        'Total de Señales': len(df),
        'Señales COMPRAR': len(df[df['senal'] == '🟢 COMPRAR']),
        'Señales VENDER': len(df[df['senal'] == '🔴 VENDER']),
        'Señales ESPERAR': len(df[df['senal'] == '⚪ ESPERAR']),
        'Error Promedio': f"{df['diferencia'].abs().mean():.5f}",
        'Error Máximo': f"{df['diferencia'].abs().max():.5f}",
        'Confianza Promedio': f"{df['confianza'].mean():.1f}%",
        'Precio Mín': f"{df['precio_actual'].min():.5f}",
        'Precio Máx': f"{df['precio_actual'].max():.5f}",
    }
    
    # Crear tabla
    tabla_data = [[k, v] for k, v in stats.items()]
    table = ax6.table(cellText=tabla_data, 
                     colLabels=['Métrica', 'Valor'],
                     cellLoc='left',
                     loc='center',
                     colWidths=[0.5, 0.3])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Estilo de la tabla
    for i in range(len(tabla_data) + 1):
        if i == 0:
            table[(i, 0)].set_facecolor('#4CAF50')
            table[(i, 1)].set_facecolor('#4CAF50')
            table[(i, 0)].set_text_props(weight='bold', color='white')
            table[(i, 1)].set_text_props(weight='bold', color='white')
        else:
            if i % 2 == 0:
                table[(i, 0)].set_facecolor('#f0f0f0')
                table[(i, 1)].set_facecolor('#f0f0f0')
    
    ax6.set_title('📊 Estadísticas del Sistema', fontsize=14, 
                  fontweight='bold', pad=20)
    
    # Ajustar layout
    plt.tight_layout()
    
    # Guardar
    plt.savefig('datos/dashboard_completo.png', dpi=300, bbox_inches='tight')
    print("✅ Dashboard guardado: datos/dashboard_completo.png")
    
    # Mostrar
    plt.show()

def estadisticas_detalladas(df):
    """Muestra estadísticas detalladas"""
    
    print("\n" + "="*60)
    print("📊 ESTADÍSTICAS DETALLADAS")
    print("="*60)
    
    print(f"\n📈 Total de registros: {len(df)}")
    print(f"📅 Periodo: {df['timestamp'].min()} a {df['timestamp'].max()}")
    
    print(f"\n💵 PRECIOS:")
    print(f"   Precio mínimo:  {df['precio_actual'].min():.5f}")
    print(f"   Precio máximo:  {df['precio_actual'].max():.5f}")
    print(f"   Precio promedio: {df['precio_actual'].mean():.5f}")
    print(f"   Rango total:    {df['precio_actual'].max() - df['precio_actual'].min():.5f}")
    
    print(f"\n🎯 SEÑALES:")
    for senal, count in df['senal'].value_counts().items():
        porcentaje = (count / len(df)) * 100
        print(f"   {senal}: {count} ({porcentaje:.1f}%)")
    
    print(f"\n📊 PRECISIÓN:")
    error_abs = df['diferencia'].abs()
    print(f"   Error promedio:    {error_abs.mean():.5f}")
    print(f"   Error máximo:      {error_abs.max():.5f}")
    print(f"   Error mínimo:      {error_abs.min():.5f}")
    print(f"   Desviación estándar: {error_abs.std():.5f}")
    
    print(f"\n🎲 CONFIANZA:")
    print(f"   Confianza promedio: {df['confianza'].mean():.1f}%")
    print(f"   Confianza máxima:   {df['confianza'].max():.1f}%")
    print(f"   Confianza mínima:   {df['confianza'].min():.1f}%")
    
    # Análisis de aciertos (simplificado)
    print(f"\n✅ ANÁLISIS DE PREDICCIONES:")
    # Predicción correcta = mismo signo que la diferencia real
    df['prediccion_correcta'] = (
        ((df['diferencia'] > 0) & (df['senal'] == '🟢 COMPRAR')) |
        ((df['diferencia'] < 0) & (df['senal'] == '🔴 VENDER')) |
        (df['senal'] == '⚪ ESPERAR')
    )
    
    aciertos = df['prediccion_correcta'].sum()
    precision = (aciertos / len(df)) * 100
    print(f"   Predicciones correctas: {aciertos}/{len(df)} ({precision:.1f}%)")
    
    print("\n" + "="*60)

def mejores_peores_predicciones(df, n=5):
    """Muestra las mejores y peores predicciones"""
    
    print("\n" + "="*60)
    print(f"🏆 TOP {n} MEJORES PREDICCIONES")
    print("="*60)
    
    # Mejores = menor error absoluto
    mejores = df.nsmallest(n, df['diferencia'].abs())
    
    for i, row in mejores.iterrows():
        print(f"\n{i+1}.")
        print(f"   Tiempo: {row['timestamp']}")
        print(f"   Precio real: {row['precio_actual']:.5f}")
        print(f"   Predicción:  {row['precio_predicho']:.5f}")
        print(f"   Error:       {abs(row['diferencia']):.5f}")
        print(f"   Señal:       {row['senal']}")
    
    print("\n" + "="*60)
    print(f"❌ TOP {n} PEORES PREDICCIONES")
    print("="*60)
    
    # Peores = mayor error absoluto
    peores = df.nlargest(n, df['diferencia'].abs())
    
    for i, row in peores.iterrows():
        print(f"\n{i+1}.")
        print(f"   Tiempo: {row['timestamp']}")
        print(f"   Precio real: {row['precio_actual']:.5f}")
        print(f"   Predicción:  {row['precio_predicho']:.5f}")
        print(f"   Error:       {abs(row['diferencia']):.5f}")
        print(f"   Señal:       {row['senal']}")
    
    print("\n" + "="*60)

def main():
    """Función principal"""
    
    print("="*60)
    print("📊 VISUALIZADOR DE RESULTADOS")
    print("="*60)
    
    # Cargar registros
    df = cargar_registros()
    
    if df is None:
        return
    
    # Mostrar estadísticas
    estadisticas_detalladas(df)
    
    # Mejores y peores predicciones
    mejores_peores_predicciones(df, n=5)
    
    # Crear dashboard visual
    crear_dashboard(df)
    
    print("\n✅ ¡Visualización completada!")
    print("📁 Archivos generados:")
    print("   - datos/dashboard_completo.png")

if __name__ == "__main__":
    main()