"""
╔══════════════════════════════════════════════════════════════════╗
║      MONITOR EN VIVO - SISTEMA DE SENTIMIENTOS EUR/USD           ║
╚══════════════════════════════════════════════════════════════════╝

Monitoreo continuo de noticias y generación automática de señales
"""

import time
from datetime import datetime, timedelta
import logging
import signal
import sys
import os

# Importar módulos del sistema
import config_sentimientos as cfg
from generador_señales_sentimientos import GeneradorSeñalesSentimiento

# Configurar logging
logging.basicConfig(
    level=getattr(logging, cfg.NIVEL_LOG),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MonitorSentimientos:
    """
    Monitorea continuamente las noticias y genera señales automáticas
    """
    
    def __init__(self):
        """Inicializa el monitor"""
        self.generador = GeneradorSeñalesSentimiento()
        self.ejecutando = True
        self.señal_anterior = None
        
        # Configurar manejador de señales para detener limpiamente
        signal.signal(signal.SIGINT, self._señal_salida)
        signal.signal(signal.SIGTERM, self._señal_salida)
        
        if cfg.MODO_VERBOSE:
            logger.info("✅ Monitor de sentimientos inicializado")
    
    
    def _señal_salida(self, signum, frame):
        """Manejador para salida limpia"""
        print("\n\n⚠️ Deteniendo monitor...")
        self.ejecutando = False
    
    
    def _detectar_cambio_señal(self, señal_actual: dict) -> bool:
        """
        Detecta si hubo un cambio significativo en la señal
        
        Args:
            señal_actual: Señal actual
        
        Returns:
            True si hay cambio significativo
        """
        if self.señal_anterior is None:
            return True
        
        # Cambio de dirección de señal
        if señal_actual['señal'] != self.señal_anterior['señal']:
            return True
        
        # Cambio significativo en confianza
        cambio_confianza = abs(
            señal_actual['confianza'] - self.señal_anterior['confianza']
        )
        
        if cambio_confianza >= cfg.UMBRAL_CAMBIO_SEÑAL:
            return True
        
        # Cambio en urgencia
        if señal_actual['urgencia'] != self.señal_anterior['urgencia']:
            return True
        
        return False
    
    
    def _generar_alerta(self, señal: dict, tipo_cambio: str):
        """
        Genera una alerta visual cuando hay cambio importante
        
        Args:
            señal: Señal actual
            tipo_cambio: Tipo de cambio detectado
        """
        if not cfg.ALERTAS_ACTIVADAS:
            return
        
        print("\n" + "🔔"*35)
        print("🚨 ALERTA DE CAMBIO DE SEÑAL 🚨")
        print("🔔"*35)
        
        print(f"\n⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Tipo de cambio: {tipo_cambio}")
        
        if self.señal_anterior:
            print(f"\n📉 Señal anterior: {self.señal_anterior['señal']} ({self.señal_anterior['confianza']:.1f}%)")
        
        print(f"📈 Señal nueva:    {señal['señal']} ({señal['confianza']:.1f}%)")
        print(f"🎯 Urgencia:       {señal['urgencia']}")
        print(f"📰 Noticias:       {señal['total_noticias']}")
        
        print("\n" + "🔔"*35 + "\n")
    
    
    def _mostrar_estado_actual(self, señal: dict, ciclo: int):
        """
        Muestra el estado actual del monitoreo
        
        Args:
            señal: Señal actual
            ciclo: Número de ciclo
        """
        hora = datetime.now().strftime('%H:%M:%S')
        
        # Símbolos
        simbolos_señal = {
            'COMPRA': '📈',
            'VENTA': '📉',
            'ESPERA': '⏸️'
        }
        
        simbolos_urgencia = {
            'ALTA': '🔴',
            'MEDIA': '🟡',
            'BAJA': '🟢'
        }
        
        print(f"\n[{hora}] Ciclo #{ciclo} | " + 
              f"{simbolos_señal.get(señal['señal'], '⚪')} {señal['señal']} | " +
              f"Confianza: {señal['confianza']:.1f}% | " +
              f"Urgencia: {simbolos_urgencia[señal['urgencia']]} {señal['urgencia']} | " +
              f"Noticias: {señal['total_noticias']}")
    
    
    def _esperar_siguiente_ciclo(self):
        """Espera hasta el siguiente ciclo de actualización"""
        segundos = cfg.INTERVALO_ACTUALIZACION * 60
        
        if cfg.MODO_VERBOSE:
            print(f"\n⏳ Esperando {cfg.INTERVALO_ACTUALIZACION} minutos hasta próxima actualización...")
        
        # Esperar en intervalos de 1 segundo para poder interrumpir
        for i in range(segundos):
            if not self.ejecutando:
                break
            time.sleep(1)
    
    
    def monitorear_continuo(self):
        """
        Ejecuta el monitoreo continuo de noticias
        """
        print("\n" + "═"*70)
        print("🔴 MONITOR EN VIVO - SISTEMA DE SENTIMIENTOS EUR/USD")
        print("═"*70)
        print(f"\n⚙️  Configuración:")
        print(f"   Intervalo:  {cfg.INTERVALO_ACTUALIZACION} minutos")
        print(f"   Alertas:    {'✅ Activadas' if cfg.ALERTAS_ACTIVADAS else '❌ Desactivadas'}")
        print(f"   Histórico:  {cfg.DIAS_HISTORICO} días")
        print("\n⌨️  Presiona Ctrl+C para detener")
        print("═"*70 + "\n")
        
        ciclo = 0
        
        try:
            while self.ejecutando:
                ciclo += 1
                
                logger.info(f"\n{'─'*70}")
                logger.info(f"🔄 CICLO #{ciclo} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info(f"{'─'*70}")
                
                try:
                    # Generar señal
                    señal = self.generador.generar_señal_completa()
                    
                    # Detectar cambios
                    if self._detectar_cambio_señal(señal):
                        
                        # Determinar tipo de cambio
                        if self.señal_anterior is None:
                            tipo_cambio = "Primera señal"
                        elif señal['señal'] != self.señal_anterior['señal']:
                            tipo_cambio = f"Cambio de {self.señal_anterior['señal']} a {señal['señal']}"
                        elif señal['urgencia'] != self.señal_anterior['urgencia']:
                            tipo_cambio = f"Cambio de urgencia: {self.señal_anterior['urgencia']} → {señal['urgencia']}"
                        else:
                            tipo_cambio = f"Cambio de confianza: {self.señal_anterior['confianza']:.1f}% → {señal['confianza']:.1f}%"
                        
                        # Generar alerta
                        self._generar_alerta(señal, tipo_cambio)
                        
                        # Mostrar señal completa
                        if cfg.MODO_VERBOSE:
                            self.generador.mostrar_señal(señal)
                    
                    # Mostrar estado
                    self._mostrar_estado_actual(señal, ciclo)
                    
                    # Actualizar señal anterior
                    self.señal_anterior = señal.copy()
                
                except Exception as e:
                    logger.error(f"❌ Error en ciclo #{ciclo}: {e}")
                    if cfg.MODO_VERBOSE:
                        import traceback
                        traceback.print_exc()
                
                # Esperar siguiente ciclo
                if self.ejecutando:
                    self._esperar_siguiente_ciclo()
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupción detectada")
        
        finally:
            self._finalizar_monitor()
    
    
    def _finalizar_monitor(self):
        """Finaliza el monitor limpiamente"""
        print("\n" + "═"*70)
        print("🛑 MONITOR DETENIDO")
        print("═"*70)
        
        if self.señal_anterior:
            print(f"\n📊 Última señal registrada:")
            print(f"   Señal:      {self.señal_anterior['señal']}")
            print(f"   Confianza:  {self.señal_anterior['confianza']:.1f}%")
            print(f"   Timestamp:  {self.señal_anterior['timestamp']}")
        
        print(f"\n💾 Datos guardados en:")
        print(f"   {cfg.ARCHIVO_SEÑALES}")
        print(f"   {cfg.ARCHIVO_NOTICIAS_ANALIZADAS}")
        
        print("\n✅ Finalización exitosa")
        print("═"*70 + "\n")
    
    
    def ejecutar_una_vez(self):
        """
        Ejecuta un único ciclo de análisis (modo one-shot)
        """
        print("\n" + "═"*70)
        print("🎯 ANÁLISIS ÚNICO - SISTEMA DE SENTIMIENTOS EUR/USD")
        print("═"*70 + "\n")
        
        try:
            # Generar señal
            señal = self.generador.generar_señal_completa()
            
            # Mostrar señal
            self.generador.mostrar_señal(señal)
            
            print("\n✅ Análisis completado")
        
        except Exception as e:
            logger.error(f"❌ Error en análisis: {e}")
            if cfg.MODO_VERBOSE:
                import traceback
                traceback.print_exc()


# ═══════════════════════════════════════════════════════════════
# 🎯 PUNTO DE ENTRADA
# ═══════════════════════════════════════════════════════════════

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Monitor de Sentimientos EUR/USD',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
    
    # Monitoreo continuo (actualiza cada 30 min por defecto)
    python monitor_sentimientos.py
    
    # Análisis único
    python monitor_sentimientos.py --once
    
    # Monitoreo silencioso (solo alertas)
    python monitor_sentimientos.py --quiet
        """
    )
    
    parser.add_argument(
        '--once',
        action='store_true',
        help='Ejecutar un solo análisis y salir'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Modo silencioso (solo mostrar alertas)'
    )
    
    args = parser.parse_args()
    
    # Ajustar verbosidad
    if args.quiet:
        cfg.MODO_VERBOSE = False
        logging.getLogger().setLevel(logging.WARNING)
    
    # Crear monitor
    monitor = MonitorSentimientos()
    
    # Ejecutar
    if args.once:
        monitor.ejecutar_una_vez()
    else:
        monitor.monitorear_continuo()


if __name__ == "__main__":
    main()
