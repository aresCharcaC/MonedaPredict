"""
VERIFICADOR DE INSTALACIÓN DEL SISTEMA DE ORO
==============================================
Este script verifica que el sistema de correlación con oro esté correctamente instalado
"""

import sys
import os

def verificar_archivos():
    """Verifica que todos los archivos necesarios existan"""
    
    print("="*70)
    print("📋 VERIFICANDO ARCHIVOS...")
    print("="*70 + "\n")
    
    archivos_requeridos = {
        'correlacion_oro.py': 'Módulo de correlación con oro',
        'CORRELACION_ORO_README.md': 'Documentación completa',
        'ejemplo_correlacion_oro.py': 'Script de ejemplo',
        'INSTALACION_ORO.txt': 'Guía de instalación',
        'config.py': 'Configuración del sistema',
        'extraer_datos.py': 'Extracción de datos',
        'entrenar_modelo.py': 'Entrenamiento del modelo',
        'prediccion_en_vivo.py': 'Predicción en vivo'
    }
    
    todos_ok = True
    
    for archivo, descripcion in archivos_requeridos.items():
        existe = os.path.exists(archivo)
        simbolo = "✅" if existe else "❌"
        print(f"{simbolo} {archivo:<30} - {descripcion}")
        
        if not existe:
            todos_ok = False
    
    print("\n" + "="*70)
    if todos_ok:
        print("✅ TODOS LOS ARCHIVOS ENCONTRADOS")
    else:
        print("❌ FALTAN ALGUNOS ARCHIVOS")
    print("="*70 + "\n")
    
    return todos_ok


def verificar_importaciones():
    """Verifica que se puedan importar los módulos necesarios"""
    
    print("="*70)
    print("📦 VERIFICANDO IMPORTACIONES...")
    print("="*70 + "\n")
    
    modulos = [
        ('correlacion_oro', 'Módulo de correlación'),
        ('config', 'Configuración'),
        ('pandas', 'Pandas (análisis de datos)'),
        ('numpy', 'NumPy (cálculos numéricos)'),
        ('scipy', 'SciPy (estadística)'),
        ('matplotlib', 'Matplotlib (gráficos)'),
        ('sklearn', 'Scikit-learn (machine learning)'),
    ]
    
    todos_ok = True
    
    for modulo, descripcion in modulos:
        try:
            __import__(modulo)
            print(f"✅ {modulo:<20} - {descripcion}")
        except ImportError as e:
            print(f"❌ {modulo:<20} - {descripcion}")
            print(f"   Error: {e}")
            todos_ok = False
    
    print("\n" + "="*70)
    if todos_ok:
        print("✅ TODAS LAS IMPORTACIONES EXITOSAS")
    else:
        print("❌ FALTAN ALGUNAS LIBRERÍAS")
        print("\n💡 Instala las librerías faltantes con:")
        print("   pip install pandas numpy scipy matplotlib scikit-learn")
    print("="*70 + "\n")
    
    return todos_ok


def verificar_configuracion():
    """Verifica la configuración del sistema"""
    
    print("="*70)
    print("⚙️ VERIFICANDO CONFIGURACIÓN...")
    print("="*70 + "\n")
    
    try:
        import config
        
        # Verificar variables de oro
        if hasattr(config, 'USAR_CORRELACION_ORO'):
            print(f"✅ USAR_CORRELACION_ORO = {config.USAR_CORRELACION_ORO}")
        else:
            print("❌ USAR_CORRELACION_ORO no encontrada en config.py")
            return False
        
        if hasattr(config, 'VENTANA_CORRELACION_ORO'):
            print(f"✅ VENTANA_CORRELACION_ORO = {config.VENTANA_CORRELACION_ORO}")
        else:
            print("❌ VENTANA_CORRELACION_ORO no encontrada en config.py")
            return False
        
        if hasattr(config, 'PESO_ORO'):
            print(f"✅ PESO_ORO = {config.PESO_ORO}")
        else:
            print("❌ PESO_ORO no encontrada en config.py")
            return False
        
        # Mostrar configuración completa
        print("\n📊 Configuración completa:")
        config.mostrar_configuracion()
        
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar configuración: {e}")
        return False


def verificar_funciones_oro():
    """Verifica que las funciones del módulo de oro funcionen"""
    
    print("="*70)
    print("🔧 VERIFICANDO FUNCIONES DEL MÓDULO DE ORO...")
    print("="*70 + "\n")
    
    try:
        import correlacion_oro
        
        # Verificar funciones principales
        funciones = [
            'calcular_correlacion',
            'crear_features_oro',
            'integrar_oro_a_eurusd',
            'visualizar_correlacion',
            'obtener_features_oro',
            'resumen_correlacion'
        ]
        
        todos_ok = True
        
        for funcion in funciones:
            if hasattr(correlacion_oro, funcion):
                print(f"✅ {funcion}")
            else:
                print(f"❌ {funcion} no encontrada")
                todos_ok = False
        
        # Verificar features de oro
        print("\n📊 Features de oro disponibles:")
        features = correlacion_oro.obtener_features_oro()
        
        if len(features) == 9:
            print(f"✅ {len(features)} features (correcto)")
            for i, feat in enumerate(features, 1):
                print(f"   {i}. {feat}")
        else:
            print(f"⚠️ {len(features)} features (se esperaban 9)")
            todos_ok = False
        
        print("\n" + "="*70)
        if todos_ok:
            print("✅ MÓDULO DE ORO FUNCIONANDO CORRECTAMENTE")
        else:
            print("❌ PROBLEMAS EN EL MÓDULO DE ORO")
        print("="*70 + "\n")
        
        return todos_ok
        
    except Exception as e:
        print(f"❌ Error al verificar módulo de oro: {e}")
        print("="*70 + "\n")
        return False


def verificar_directorios():
    """Verifica que existan los directorios necesarios"""
    
    print("="*70)
    print("📁 VERIFICANDO DIRECTORIOS...")
    print("="*70 + "\n")
    
    directorios = ['datos', 'modelos', 'registros']
    
    todos_ok = True
    
    for directorio in directorios:
        existe = os.path.exists(directorio)
        simbolo = "✅" if existe else "⚠️"
        print(f"{simbolo} {directorio}/")
        
        if not existe:
            print(f"   → Se creará automáticamente al ejecutar scripts")
    
    print("\n" + "="*70)
    print("✅ VERIFICACIÓN DE DIRECTORIOS COMPLETADA")
    print("="*70 + "\n")
    
    return True


def main():
    """Función principal"""
    
    print("\n" + "="*70)
    print("🥇 VERIFICADOR DE INSTALACIÓN - SISTEMA DE CORRELACIÓN CON ORO")
    print("="*70 + "\n")
    
    resultados = []
    
    # 1. Verificar archivos
    resultados.append(("Archivos", verificar_archivos()))
    
    # 2. Verificar importaciones
    resultados.append(("Importaciones", verificar_importaciones()))
    
    # 3. Verificar configuración
    resultados.append(("Configuración", verificar_configuracion()))
    
    # 4. Verificar funciones de oro
    resultados.append(("Módulo de Oro", verificar_funciones_oro()))
    
    # 5. Verificar directorios
    resultados.append(("Directorios", verificar_directorios()))
    
    # Resumen final
    print("="*70)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("="*70 + "\n")
    
    todos_ok = True
    
    for nombre, resultado in resultados:
        simbolo = "✅" if resultado else "❌"
        estado = "OK" if resultado else "FALLÓ"
        print(f"{simbolo} {nombre:<20} - {estado}")
        
        if not resultado:
            todos_ok = False
    
    print("\n" + "="*70)
    
    if todos_ok:
        print("🎉 ¡INSTALACIÓN CORRECTA!")
        print("="*70)
        print("\n✅ El sistema de correlación con oro está listo para usar")
        print("\n📚 Próximos pasos:")
        print("   1. Lee INSTALACION_ORO.txt para guía rápida")
        print("   2. Lee CORRELACION_ORO_README.md para documentación completa")
        print("   3. Ejecuta: python extraer_datos.py (para descargar datos con oro)")
        print("   4. Ejecuta: python ejemplo_correlacion_oro.py (para ver ejemplos)")
        print("\n💡 El sistema está listo para mejorar tus predicciones!")
    else:
        print("⚠️ INSTALACIÓN INCOMPLETA")
        print("="*70)
        print("\n❌ Algunos componentes presentan problemas")
        print("\n🔧 Soluciones:")
        print("   • Verifica que todos los archivos estén presentes")
        print("   • Instala librerías faltantes: pip install -r requirements.txt")
        print("   • Revisa config.py para configuración de oro")
        print("\n📧 Si persisten los problemas, revisa CORRELACION_ORO_README.md")
    
    print("="*70 + "\n")
    
    return 0 if todos_ok else 1


if __name__ == "__main__":
    sys.exit(main())
