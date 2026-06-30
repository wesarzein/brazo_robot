import serial
import time


class SerialManager:

    def __init__(self):

        self.serial_port = None

    # ==================================
    # CONEXION
    # ==================================

    def connect(
        self,
        port,
        baudrate=115200
    ):

        self.serial_port = serial.Serial(
            port,
            baudrate,
            timeout=1
        )

        # Esperar reinicio ESP32
        time.sleep(2)

    def disconnect(self):

        if self.serial_port:

            self.serial_port.close()

            self.serial_port = None

    def is_connected(self):

        return (
            self.serial_port is not None
            and self.serial_port.is_open
        )

    # ==================================
    # ENVIO NORMAL
    # ==================================

    def send_state(self, state):

        if not self.is_connected():
            return

        if not state.communication_enabled:
            return

        line = (
            f"B:{state.base},"
            f"C1:{state.codo1},"
            f"C2:{state.codo2},"
            f"P:{state.pinza},"
            f"S:{int(state.servos_enabled)}\n"
        )

        try:

            self.serial_port.write(
                line.encode("utf-8")
            )

        except Exception:
            pass

    # ==================================
    # PARADA DE EMERGENCIA
    # ==================================

    def send_stop(self):

        if not self.is_connected():
            return

        try:

            self.serial_port.write(
                b"B:0,C1:0,C2:0,P:0,S:0\n"
            )

        except Exception:
            pass

    # ==================================
    # SINCRONIZAR HOME
    # ==================================
    #
    # Requiere soporte futuro
    # en el firmware ESP32.
    #
    # HOME:
    # C1 = 20
    # C2 = 140
    # P  = 135
    #
    # ==================================

    def send_sync_home(self):

        if not self.is_connected():
            return

        try:

            self.serial_port.write(
                b"SYNC,C1:20,C2:140,P:135\n"
            )

        except Exception:
            pass