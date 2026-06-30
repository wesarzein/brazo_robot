import time
import cv2

from PIL import Image

from config import *
from models.robot_state import RobotState

from vision.hand_tracker import HandTracker
from vision.gesture_detector import GestureDetector

from communication.serial_manager import SerialManager

from gui.main_window import MainWindow


# ==========================================
# OBJETOS
# ==========================================

state = RobotState()

tracker = HandTracker()

detector = GestureDetector()

serial_manager = SerialManager()

# ==========================================
# CAMARA
# ==========================================

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():

    raise Exception(
        "No se pudo abrir la camara"
    )

# ==========================================
# FPS
# ==========================================

fps_time = time.time()

# ==========================================
# SERIAL RATE
# ==========================================

last_serial_send = 0

SERIAL_INTERVAL = (
    1.0 / SERIAL_RATE_HZ
)

# ==========================================
# GUI
# ==========================================

app = MainWindow()

# ==========================================
# SERIAL
# ==========================================

def connect_serial():

    port = app.get_com_port()

    if not port:
        return

    try:

        serial_manager.connect(
            port
        )

        print(
            f"Conectado a {port}"
        )

    except Exception as e:

        print(
            "Error conexion:",
            e
        )


def disconnect_serial():

    try:

        serial_manager.send_stop()

    except:
        pass

    serial_manager.disconnect()

    print(
        "Serial desconectado"
    )


# ==========================================
# COMUNICACION
# ==========================================

def enable_communication():

    state.communication_enabled = True

    state.servos_enabled = True

    print(
        "Comunicacion activada"
    )


def disable_communication():

    state.communication_enabled = False

    state.servos_enabled = False

    state.base = 0
    state.codo1 = 0
    state.codo2 = 0
    state.pinza = 0

    try:

        serial_manager.send_stop()

    except:
        pass

    print(
        "Comunicacion detenida"
    )


# ==========================================
# HOME
# ==========================================

def sync_home():

    state.synced = True

    try:

        serial_manager.send_sync_home()

    except:
        pass

    print(
        "HOME sincronizado"
    )


# ==========================================
# BOTONES
# ==========================================

app.btn_connect.configure(
    command=connect_serial
)

app.btn_disconnect.configure(
    command=disconnect_serial
)

app.btn_comm_on.configure(
    command=enable_communication
)

app.btn_comm_off.configure(
    command=disable_communication
)

app.btn_sync_home.configure(
    command=sync_home
)

# ==========================================
# LOOP PRINCIPAL
# ==========================================

def update():

    global fps_time
    global last_serial_send

    ret, frame = cap.read()

    if not ret:

        app.after(
            10,
            update
        )

        return

    frame = cv2.flip(
        frame,
        1
    )

    (
        left_hand,
        right_hand,
        results
    ) = tracker.process(frame)

    # ======================================
    # DIBUJAR MANOS
    # ======================================

    if left_hand:

        tracker.draw(
            frame,
            left_hand
        )

    if right_hand:

        tracker.draw(
            frame,
            right_hand
        )

    # ======================================
    # GESTOS
    # ======================================

    data = detector.process(
        left_hand,
        right_hand
    )

    if state.communication_enabled:

        state.base = data["base"]

        state.codo1 = data["codo1"]

        state.codo2 = data["codo2"]

        state.pinza = data["pinza"]

    else:

        state.base = 0

        state.codo1 = 0

        state.codo2 = 0

        state.pinza = 0

    # ======================================
    # FPS
    # ======================================

    now = time.time()

    dt = now - fps_time

    fps_time = now

    if dt > 0:

        state.fps = 1.0 / dt

    # ======================================
    # SERIAL
    # ======================================

    if (
        serial_manager.is_connected()
        and
        state.communication_enabled
        and
        now - last_serial_send
        >= SERIAL_INTERVAL
    ):

        serial_manager.send_state(
            state
        )

        last_serial_send = now

    # ======================================
    # GUI
    # ======================================

    app.update_state(
        state
    )

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    pil_image = Image.fromarray(
        rgb
    )

    app.update_video(
        pil_image
    )

    app.after(
        10,
        update
    )

# ==========================================
# CIERRE
# ==========================================

def on_close():

    try:

        serial_manager.send_stop()

    except:
        pass

    try:

        serial_manager.disconnect()

    except:
        pass

    try:

        cap.release()

    except:
        pass

    app.destroy()

# ==========================================
# START
# ==========================================

app.protocol(
    "WM_DELETE_WINDOW",
    on_close
)

update()

app.mainloop()