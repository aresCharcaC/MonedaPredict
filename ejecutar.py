"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║            🚀 EJECUTOR MAESTRO - SISTEMA COMPLETO 🚀                 ║
║                                                                      ║
║  Sistema Integral de Trading con 3 módulos de IA:                   ║
║  • LSTM: Redes neuronales para predicción de tendencias             ║
║  • KNN: Recomendación por patrones similares                         ║
║  • SENTIMIENTOS: Análisis de noticias financieras                    ║
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
    print("║         🤖 SISTEMA INTEGRAL DE TRADING CON 3 MÓDULOS DE IA 🤖           ║")
    print("║                                                                          ║")
    print("║     📊 LSTM | 🎯 KNN | 📰 SENTIMIENTOS | 🔥 SISTEMA HÍBRIDO             ║")
    print("║                                                                          ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝")
    print("═"*80 + "\n")

def mostrar_menu_principal():
    """Muestra el menú principal de sistemas"""
    print("\n" + "─"*80)
    print("🎯 SELECCIONA EL SISTEMA DE TRADING")
    print("─"*80)
    print("1️⃣  📊 Sistema LSTM (Redes Neuronales)")
    print("2️⃣  🎯 Sistema KNN (Recomendación por Patrones)")
    print("3️⃣  📰 Sistema de Sentimientos (Análisis de Noticias)")
    print("4️⃣  🔥 Sistema Híbrido (LSTM + KNN + Sentimientos)")
    print("5️⃣  ⚙️  Configuración Global")
    print("0️⃣  ❌ Salir")
    print("─"*80)

def mostrar_menu_lstm():
    """Muestra el menú del sistema LSTM"""
    print("\n" + "─"*80)
    print("📊 SISTEMA LSTM - REDES NEURONALES")
    print("─"*80)
    print("1️⃣  Ver configuración LSTM")
    print("2️⃣  Descargar datos de MT5")
    print("3️⃣  Entrenar modelo LSTM")
    print("4️⃣  Predicción en vivo (LSTM)")
    print("5️⃣  Generar señales IQ Option")
    print("6️⃣  Visualizar resultados")
    print("7️⃣  Proceso completo (2 → 3 → 4)")
    print("0️⃣  ← Volver al menú principal")
    print("─"*80)

def mostrar_menu_knn():
    """Muestra el menú del sistema KNN"""
    print("\n" + "─"*80)
    print("🎯 SISTEMA KNN - RECOMENDACIÓN POR PATRONES")
    print("─"*80)
    print("1️⃣  Ver configuración KNN")
    print("2️⃣  Entrenar sistema KNN")
    print("3️⃣  Predicción en vivo (KNN)")
    print("4️⃣  Evaluar rendimiento KNN")
    print("5️⃣  Ver reportes de entrenamiento")
    print("0️⃣  ← Volver al menú principal")
    print("─"*80)

def mostrar_menu_sentimientos():
    """Muestra el menú del sistema de sentimientos"""
    print("\n" + "─"*80)
    print("📰 SISTEMA DE SENTIMIENTOS - ANÁLISIS DE NOTICIAS")
    print("─"*80)
    print("1️⃣  Ver configuración Sentimientos")
    print("2️⃣  Recolectar noticias (una vez)")
    print("3️⃣  Analizar sentimientos")
    print("4️⃣  Generar señal de sentimiento")
    print("5️⃣  Monitor continuo (actualización cada 30 min)")
    print("6️⃣  Visualizar dashboard")
    print("7️⃣  Generar reporte completo")
    print("0️⃣  ← Volver al menú principal")
    print("─"*80)

def mostrar_menu_hibrido():
    """Muestra el menú del sistema híbrido"""
    print("\n" + "─"*80)
    print("🔥 SISTEMA HÍBRIDO - LSTM + KNN + SENTIMIENTOS")
    print("─"*80)
    print("1️⃣  Ver configuración híbrida")
    print("2️⃣  Predicción híbrida en vivo")
    print("3️⃣  Generar señales combinadas")
    print("4️⃣  Comparar sistemas")
    print("5️⃣  Dashboard unificado")
    print("0️⃣  ← Volver al menú principal")
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
    import extraer_datos
    extraer_datos.main()
    
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
    import entrenar_modelo
    entrenar_modelo.main()
    
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
    import generar_señales_iqoption
    generar_señales_iqoption.main()

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
    import visualizar_resultados
    visualizar_resultados.main()
    
    print("\n✅ Resultados generados!")
    input("\nPresiona ENTER para continuar...")

def proceso_completo():
    """Ejecuta todo el proceso de una vez"""
    print("\n" + "═"*80)
    print("🚀 PROCESO COMPLETO AUTOMÁTICO - LSTM")
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

# ═══════════════════════════════════════════════════════════════
# 🎯 FUNCIONES DEL SISTEMA KNN
# ═══════════════════════════════════════════════════════════════

def knn_configuracion():
    """Muestra configuración del sistema KNN"""
    print("\n" + "═"*80)
    print("⚙️  CONFIGURACIÓN DEL SISTEMA KNN")
    print("═"*80 + "\n")
    
    print(f"📊 Sistema de Recomendación K-Nearest Neighbors")
    print(f"   Par:              {config.PAR_DIVISAS}")
    print(f"   K vecinos:        {config.K_VECINOS}")
    print(f"   Horizonte:        {config.HORIZONTE_KNN} velas")
    print(f"   Peso KNN:         {config.PESO_KNN * 100}%")
    print(f"   Estado:           {'✅ Activo' if config.USAR_KNN else '❌ Inactivo'}")
    
    input("\nPresiona ENTER para continuar...")

def knn_entrenar():
    """Entrena el sistema KNN"""
    print("\n" + "═"*80)
    print("🎯 ENTRENANDO SISTEMA KNN")
    print("═"*80 + "\n")
    
    print("⏳ Cargando datos históricos y entrenando KNN...")
    print("⏱️  Tiempo estimado: 2-3 minutos\n")
    
    input("Presiona ENTER para comenzar...")
    
    try:
        import entrenar_knn
        entrenar_knn.main()
        print("\n✅ Sistema KNN entrenado exitosamente!")
    except Exception as e:
        print(f"\n❌ Error entrenando KNN: {e}")
    
    input("\nPresiona ENTER para continuar...")

def knn_prediccion_vivo():
    """Ejecuta predicción en vivo con KNN"""
    print("\n" + "═"*80)
    print("🎯 PREDICCIÓN EN VIVO - SISTEMA KNN")
    print("═"*80 + "\n")
    
    print("📊 Sistema KNN + LSTM combinados")
    print("⚠️  Para detener: Presiona Ctrl+C\n")
    
    input("Presiona ENTER para comenzar...")
    
    try:
        import prediccion_en_vivo
        prediccion_en_vivo.main()
    except KeyboardInterrupt:
        print("\n\n🛑 Predicción detenida por el usuario")

def knn_ver_reportes():
    """Visualiza reportes de KNN"""
    print("\n" + "═"*80)
    print("📊 REPORTES DEL SISTEMA KNN")
    print("═"*80 + "\n")
    
    if not os.path.exists("registros"):
        print("❌ No hay reportes disponibles")
        input("\nPresiona ENTER para continuar...")
        return
    
    # Buscar archivos de reporte
    reportes = [f for f in os.listdir("registros") if f.startswith("reporte_entrenamiento_knn")]
    
    if not reportes:
        print("❌ No se encontraron reportes de KNN")
        print("👉 Primero entrena el sistema KNN (opción 2)\n")
    else:
        print(f"✅ Reportes disponibles: {len(reportes)}\n")
        ultimo = sorted(reportes)[-1]
        print(f"📄 Último reporte: registros/{ultimo}")
        
        # Mostrar contenido
        try:
            with open(f"registros/{ultimo}", 'r', encoding='utf-8') as f:
                print("\n" + "─"*80)
                print(f.read())
                print("─"*80)
        except Exception as e:
            print(f"❌ Error leyendo reporte: {e}")
    
    input("\nPresiona ENTER para continuar...")

# ═══════════════════════════════════════════════════════════════
# 📰 FUNCIONES DEL SISTEMA DE SENTIMIENTOS
# ═══════════════════════════════════════════════════════════════

def sentimientos_configuracion():
    """Muestra configuración del sistema de sentimientos"""
    print("\n" + "═"*80)
    print("⚙️  CONFIGURACIÓN DEL SISTEMA DE SENTIMIENTOS")
    print("═"*80 + "\n")
    
    try:
        sys.path.insert(0, 'Sistema de rsentimientos')
        import config_sentimientos
        config_sentimientos.mostrar_configuracion()
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'Sistema de rsentimientos' in sys.path:
            sys.path.remove('Sistema de rsentimientos')
    
    input("\nPresiona ENTER para continuar...")

def sentimientos_recolectar():
    """Recolecta noticias"""
    print("\n" + "═"*80)
    print("📰 RECOLECTANDO NOTICIAS")
    print("═"*80 + "\n")
    
    try:
        sys.path.insert(0, 'Sistema de rsentimientos')
        from recolector_noticias import RecolectorNoticias
        
        recolector = RecolectorNoticias()
        df = recolector.recolectar_noticias()
        recolector.mostrar_resumen(df)
        
        print("\n✅ Recolección completada!")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'Sistema de rsentimientos' in sys.path:
            sys.path.remove('Sistema de rsentimientos')
    
    input("\nPresiona ENTER para continuar...")

def sentimientos_analizar():
    """Analiza sentimientos de noticias"""
    print("\n" + "═"*80)
    print("🧠 ANALIZANDO SENTIMIENTOS")
    print("═"*80 + "\n")
    
    try:
        sys.path.insert(0, 'Sistema de rsentimientos')
        from recolector_noticias import RecolectorNoticias
        from analizador_sentimientos import AnalizadorSentimientos
        
        print("📥 Recolectando noticias...")
        recolector = RecolectorNoticias()
        df_noticias = recolector.recolectar_noticias()
        
        print("\n🧠 Analizando sentimientos...")
        analizador = AnalizadorSentimientos()
        df_analizado = analizador.analizar_lote_noticias(df_noticias)
        analizador.mostrar_resumen_sentimientos(df_analizado)
        
        print("\n✅ Análisis completado!")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'Sistema de rsentimientos' in sys.path:
            sys.path.remove('Sistema de rsentimientos')
    
    input("\nPresiona ENTER para continuar...")

def sentimientos_generar_senal():
    """Genera señal de trading basada en sentimientos"""
    print("\n" + "═"*80)
    print("🎯 GENERANDO SEÑAL DE SENTIMIENTO")
    print("═"*80 + "\n")
    
    try:
        sys.path.insert(0, 'Sistema de rsentimientos')
        from generador_señales_sentimientos import GeneradorSeñalesSentimiento
        
        generador = GeneradorSeñalesSentimiento()
        señal = generador.generar_señal_completa()
        generador.mostrar_señal(señal)
        
        print("\n✅ Señal generada!")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'Sistema de rsentimientos' in sys.path:
            sys.path.remove('Sistema de rsentimientos')
    
    input("\nPresiona ENTER para continuar...")

def sentimientos_monitor():
    """Ejecuta monitor continuo de sentimientos"""
    print("\n" + "═"*80)
    print("🔴 MONITOR CONTINUO DE SENTIMIENTOS")
    print("═"*80 + "\n")
    
    print("⚠️  El sistema se actualizará cada 30 minutos")
    print("⚠️  Para detener: Presiona Ctrl+C\n")
    
    input("Presiona ENTER para comenzar...")
    
    try:
        # Cambiar al directorio del sistema de sentimientos
        os.chdir('Sistema de rsentimientos')
        os.system('python monitor_sentimientos.py')
    except KeyboardInterrupt:
        print("\n\n🛑 Monitor detenido por el usuario")
    finally:
        os.chdir('..')

def sentimientos_dashboard():
    """Genera dashboard de visualización"""
    print("\n" + "═"*80)
    print("📊 DASHBOARD DE SENTIMIENTOS")
    print("═"*80 + "\n")
    
    dias = input("¿Cuántos días visualizar? (default: 7): ").strip()
    dias = int(dias) if dias.isdigit() else 7
    
    try:
        os.chdir('Sistema de rsentimientos')
        os.system(f'python visualizador_sentimientos.py --tipo todo --dias {dias}')
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        os.chdir('..')
    
    input("\nPresiona ENTER para continuar...")

def sentimientos_reporte():
    """Genera reporte completo"""
    print("\n" + "═"*80)
    print("📄 GENERANDO REPORTE COMPLETO")
    print("═"*80 + "\n")
    
    dias = input("¿Cuántos días incluir? (default: 7): ").strip()
    dias = int(dias) if dias.isdigit() else 7
    
    try:
        os.chdir('Sistema de rsentimientos')
        os.system(f'python visualizador_sentimientos.py --tipo reporte --dias {dias}')
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        os.chdir('..')
    
    input("\nPresiona ENTER para continuar...")

# ═══════════════════════════════════════════════════════════════
# 🔥 FUNCIONES DEL SISTEMA HÍBRIDO
# ═══════════════════════════════════════════════════════════════

def hibrido_configuracion():
    """Muestra configuración del sistema híbrido"""
    print("\n" + "═"*80)
    print("⚙️  CONFIGURACIÓN DEL SISTEMA HÍBRIDO")
    print("═"*80 + "\n")
    
    config.mostrar_configuracion()
    
    input("\nPresiona ENTER para continuar...")

def hibrido_prediccion():
    """Ejecuta predicción híbrida en vivo"""
    print("\n" + "═"*80)
    print("🔥 PREDICCIÓN HÍBRIDA EN VIVO")
    print("═"*80 + "\n")
    
    print("📊 Combinando:")
    print("   • LSTM (Redes Neuronales)")
    print("   • KNN (Patrones Similares)")
    print("   • Sentimientos (Noticias)\n")
    
    print("⚠️  Para detener: Presiona Ctrl+C\n")
    
    input("Presiona ENTER para comenzar...")
    
    try:
        import prediccion_en_vivo
        prediccion_en_vivo.main()
    except KeyboardInterrupt:
        print("\n\n🛑 Predicción detenida por el usuario")

def hibrido_señales():
    """Genera señales combinadas"""
    print("\n" + "═"*80)
    print("🎯 GENERANDO SEÑALES COMBINADAS")
    print("═"*80 + "\n")
    
    print("📊 Generando señales con los 3 sistemas...")
    print("⚠️  Para detener: Presiona Ctrl+C\n")
    
    input("Presiona ENTER para comenzar...")
    
    try:
        import generar_señales_iqoption
        generar_señales_iqoption.main()
    except KeyboardInterrupt:
        print("\n\n🛑 Generación detenida por el usuario")

def hibrido_comparar():
    """Compara rendimiento de los 3 sistemas"""
    print("\n" + "═"*80)
    print("📊 COMPARACIÓN DE SISTEMAS")
    print("═"*80 + "\n")
    
    print("Comparando rendimiento de:")
    print("   1. LSTM solo")
    print("   2. KNN solo")
    print("   3. Sentimientos solo")
    print("   4. Combinación híbrida\n")
    
    # Mostrar estadísticas si existen
    if os.path.exists("registros/señales_iqoption.csv"):
        import pandas as pd
        df = pd.read_csv("registros/señales_iqoption.csv")
        print(f"📊 Total señales generadas: {len(df)}")
        print(f"📅 Período: {df['timestamp'].min()} - {df['timestamp'].max()}\n")
    else:
        print("❌ No hay datos de señales aún\n")
    
    input("Presiona ENTER para continuar...")

def hibrido_dashboard():
    """Genera dashboard unificado"""
    print("\n" + "═"*80)
    print("📊 DASHBOARD UNIFICADO")
    print("═"*80 + "\n")
    
    try:
        import visualizar_resultados
        visualizar_resultados.main()
        print("\n✅ Dashboard generado!")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    input("\nPresiona ENTER para continuar...")

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

def menu_lstm():
    """Menú del sistema LSTM"""
    while True:
        limpiar_pantalla()
        mostrar_banner()
        mostrar_menu_lstm()
        
        opcion = input("\n👉 Selecciona una opción: ").strip()
        
        if opcion == "1":
            paso_1_configuracion()
        elif opcion == "2":
            paso_2_descargar_datos()
        elif opcion == "3":
            paso_3_entrenar_modelo()
        elif opcion == "4":
            knn_prediccion_vivo()
        elif opcion == "5":
            paso_4_generar_senales()
        elif opcion == "6":
            paso_5_ver_resultados()
        elif opcion == "7":
            proceso_completo()
        elif opcion == "0":
            break
        else:
            print("\n❌ Opción inválida")
            input("Presiona ENTER para continuar...")

def menu_knn():
    """Menú del sistema KNN"""
    while True:
        limpiar_pantalla()
        mostrar_banner()
        mostrar_menu_knn()
        
        opcion = input("\n👉 Selecciona una opción: ").strip()
        
        if opcion == "1":
            knn_configuracion()
        elif opcion == "2":
            knn_entrenar()
        elif opcion == "3":
            knn_prediccion_vivo()
        elif opcion == "4":
            knn_entrenar()  # Evaluar rendimiento está en entrenar
        elif opcion == "5":
            knn_ver_reportes()
        elif opcion == "0":
            break
        else:
            print("\n❌ Opción inválida")
            input("Presiona ENTER para continuar...")

def menu_sentimientos():
    """Menú del sistema de sentimientos"""
    while True:
        limpiar_pantalla()
        mostrar_banner()
        mostrar_menu_sentimientos()
        
        opcion = input("\n👉 Selecciona una opción: ").strip()
        
        if opcion == "1":
            sentimientos_configuracion()
        elif opcion == "2":
            sentimientos_recolectar()
        elif opcion == "3":
            sentimientos_analizar()
        elif opcion == "4":
            sentimientos_generar_senal()
        elif opcion == "5":
            sentimientos_monitor()
        elif opcion == "6":
            sentimientos_dashboard()
        elif opcion == "7":
            sentimientos_reporte()
        elif opcion == "0":
            break
        else:
            print("\n❌ Opción inválida")
            input("Presiona ENTER para continuar...")

def menu_hibrido():
    """Menú del sistema híbrido"""
    while True:
        limpiar_pantalla()
        mostrar_banner()
        mostrar_menu_hibrido()
        
        opcion = input("\n👉 Selecciona una opción: ").strip()
        
        if opcion == "1":
            hibrido_configuracion()
        elif opcion == "2":
            hibrido_prediccion()
        elif opcion == "3":
            hibrido_señales()
        elif opcion == "4":
            hibrido_comparar()
        elif opcion == "5":
            hibrido_dashboard()
        elif opcion == "0":
            break
        else:
            print("\n❌ Opción inválida")
            input("Presiona ENTER para continuar...")

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
        mostrar_menu_principal()
        
        opcion = input("\n👉 Selecciona un sistema: ").strip()
        
        if opcion == "1":
            menu_lstm()
        elif opcion == "2":
            menu_knn()
        elif opcion == "3":
            menu_sentimientos()
        elif opcion == "4":
            menu_hibrido()
        elif opcion == "5":
            paso_1_configuracion()
        elif opcion == "0":
            print("\n" + "═"*80)
            print("👋 ¡Gracias por usar el Sistema Integral de Trading!")
            print("═"*80)
            print("\n📁 Tus datos están guardados en:")
            print("   • registros/señales_iqoption.csv (Señales IQ Option)")
            print("   • datos/ (Datos históricos)")
            print("   • modelos/ (Modelos entrenados)")
            print("   • Sistema de rsentimientos/datos_sentimientos/ (Análisis de noticias)")
            print("\n✅ Sistema cerrado correctamente\n")
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