"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║            🚀 EJECUTOR MAESTRO - SISTEMA COMPLETO 🚀                 ║
║                                                                      ║
║  Este archivo ejecuta TODO el proceso automáticamente:              ║
║  1. Descarga datos                                                   ║
║  2. Entrena modelo                                                   ║
║  3. Genera señales en tiempo real                                    ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
from datetime import datetime

# Importar configuración
try:
    import config
except ImportError:
    print("❌ Error: No se encuentra config.py")
    print("👉 Asegúrate de tener config.py en la misma carpeta")
    sys.exit(1)

def limpiar_pantalla():
    """Limpia la pantalla"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_banner():
    """Muestra el banner inicial"""
    print("\n" + "═"*80)
    print("╔══════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                          ║")
    print("║              🤖 SISTEMA DE TRADING CON IA - FOREX 🤖                     ║")
    print("║                                                                          ║")
    print("║                    Proyecto de Minería de Datos                          ║")
    print("║                                                                          ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝")
    print("═"*80 + "\n")

def mostrar_menu():
    """Muestra el menú de opciones"""
    print("\n" + "─"*80)
    print("📋 MENÚ PRINCIPAL")
    print("─"*80)
    print("1️⃣  Configuración actual")
    print("2️⃣  Descargar datos de MT5")
    print("3️⃣  Entrenar modelo")
    print("4️⃣  Generar señales (IQ Option)")
    print("5️⃣  Ver resultados")
    print("6️⃣  Proceso completo (2 → 3 → 4)")
    print("0️⃣  Salir")
    print("─"*80)

def paso_1_configuracion():
    """Muestra la configuración actual"""
    config.mostrar_configuracion()
    
    print("💡 Para cambiar la configuración:")
    print("   1. Abre el archivo: config.py")
    print("   2. Cambia las variables PAR_DIVISAS y TIMEFRAME")
    print("   3. Guarda y vuelve a ejecutar este programa\n")
    
    input("Presiona ENTER para continuar...")

def paso_2_descargar_datos():
    """Descarga datos de MT5"""
    print("\n" + "═"*80)
    print("📥 PASO 1: DESCARGANDO DATOS DE METATRADER 5")
    print("═"*80 + "\n")
    
    print("⚠️  Asegúrate de que MetaTrader5 esté ABIERTO\n")
    input("Presiona ENTER cuando MT5 esté abierto...")
    
    # Ejecutar script de extracción
    print("\n🔄 Descargando datos...\n")
    os.system("python extraer_datos.py")
    
    print("\n✅ Descarga completada!")
    input("\nPresiona ENTER para continuar...")

def paso_3_entrenar_modelo():
    """Entrena el modelo"""
    print("\n" + "═"*80)
    print("🧠 PASO 2: ENTRENANDO MODELO DE IA")
    print("═"*80 + "\n")
    
    print("⏳ Esto puede tardar 10-15 minutos...")
    print("☕ Ve por un café mientras entrena\n")
    
    input("Presiona ENTER para comenzar entrenamiento...")
    
    # Ejecutar entrenamiento
    print("\n🔄 Entrenando...\n")
    os.system("python entrenar_modelo.py")
    
    print("\n✅ Entrenamiento completado!")
    input("\nPresiona ENTER para continuar...")

def paso_4_generar_senales():
    """Genera señales en tiempo real"""
    print("\n" + "═"*80)
    print("🎯 PASO 3: GENERANDO SEÑALES DE TRADING")
    print("═"*80 + "\n")
    
    print("📊 El sistema generará señales cada", config.REVISAR_CADA_MINUTOS, "minutos")
    print("💡 Copia los valores que aparezcan en IQ Option")
    print("⚠️  Para detener: Presiona Ctrl+C\n")
    
    input("Presiona ENTER para comenzar...")
    
    # Ejecutar generador de señales
    print("\n🤖 Sistema activado...\n")
    os.system("python generar_señales_iqoption.py")

def paso_5_ver_resultados():
    """Visualiza los resultados"""
    print("\n" + "═"*80)
    print("📊 VISUALIZANDO RESULTADOS")
    print("═"*80 + "\n")
    
    if not os.path.exists("registros/señales_iqoption.csv"):
        print("❌ No hay señales registradas aún")
        print("👉 Primero ejecuta la opción 4 (Generar señales)\n")
        input("Presiona ENTER para volver...")
        return
    
    print("🔄 Generando gráficos...\n")
    os.system("python visualizar_resultados.py")
    
    print("\n✅ Resultados generados!")
    input("\nPresiona ENTER para continuar...")

def proceso_completo():
    """Ejecuta todo el proceso de una vez"""
    print("\n" + "═"*80)
    print("🚀 PROCESO COMPLETO AUTOMÁTICO")
    print("═"*80 + "\n")
    
    print("Este proceso ejecutará:")
    print("  1️⃣  Descargar datos")
    print("  2️⃣  Entrenar modelo")
    print("  3️⃣  Generar señales\n")
    
    respuesta = input("¿Continuar? (s/n): ").lower()
    
    if respuesta != 's':
        print("❌ Proceso cancelado")
        input("\nPresiona ENTER para volver...")
        return
    
    # Paso 1: Descargar datos
    paso_2_descargar_datos()
    
    # Paso 2: Entrenar modelo
    paso_3_entrenar_modelo()
    
    # Paso 3: Generar señales
    paso_4_generar_senales()

def verificar_archivos():
    """Verifica que todos los archivos necesarios existan"""
    archivos_necesarios = [
        "config.py",
        "extraer_datos.py",
        "entrenar_modelo.py",
        "generar_señales_iqoption.py",
        "visualizar_resultados.py"
    ]
    
    faltantes = []
    for archivo in archivos_necesarios:
        if not os.path.exists(archivo):
            faltantes.append(archivo)
    
    if faltantes:
        print("\n❌ ERROR: Faltan archivos necesarios:")
        for f in faltantes:
            print(f"   - {f}")
        print("\n👉 Descarga todos los archivos del proyecto\n")
        return False
    
    return True

def main():
    """Función principal"""
    
    # Verificar archivos
    if not verificar_archivos():
        input("Presiona ENTER para salir...")
        return
    
    while True:
        limpiar_pantalla()
        mostrar_banner()
        config.mostrar_configuracion()
        mostrar_menu()
        
        opcion = input("\n👉 Selecciona una opción: ").strip()
        
        if opcion == "1":
            paso_1_configuracion()
        elif opcion == "2":
            paso_2_descargar_datos()
        elif opcion == "3":
            paso_3_entrenar_modelo()
        elif opcion == "4":
            paso_4_generar_senales()
        elif opcion == "5":
            paso_5_ver_resultados()
        elif opcion == "6":
            proceso_completo()
        elif opcion == "0":
            print("\n👋 ¡Hasta luego!")
            print("📁 Tus señales están guardadas en: registros/señales_iqoption.csv\n")
            break
        else:
            print("\n❌ Opción inválida")
            input("Presiona ENTER para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Programa interrumpido por el usuario")
        print("📁 Tus datos están guardados\n")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        input("\nPresiona ENTER para salir...")