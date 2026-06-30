from dataclasses import dataclass


@dataclass
class RobotState:

    # =====================
    # COMANDOS DE MOVIMIENTO
    # =====================
    #
    # -1 = movimiento negativo
    #  0 = detener
    #  1 = movimiento positivo
    #

    # Base continua
    # -1 = derecha
    #  0 = stop
    #  1 = izquierda
    base: int = 0

    # Codo 1
    # -1 = vertical
    #  0 = stop
    #  1 = horizontal
    codo1: int = 0

    # Codo 2
    # -1 = adelante
    #  0 = stop
    #  1 = atras
    codo2: int = 0

    # Pinza
    # -1 = abrir
    #  0 = stop
    #  1 = cerrar
    pinza: int = 0

    # =====================
    # CONTROL GENERAL
    # =====================

    # Habilita movimiento en ESP32
    servos_enabled: bool = False

    # Habilita envio serial desde la GUI
    communication_enabled: bool = False

    # =====================
    # SINCRONIZACION
    # =====================

    # Indica si la posicion HOME fue
    # sincronizada manualmente
    synced: bool = False

    # =====================
    # METRICAS
    # =====================

    fps: float = 0.0