# ==========================
# CAMARA
# ==========================

CAMERA_INDEX = 0

# ==========================
# FILTROS
# ==========================

EMA_ALPHA = 0.20

# ==========================
# SERIAL
# ==========================

SERIAL_RATE_HZ = 20

# ==========================
# DETECCION DE GESTOS
# ==========================
#
# Mano izquierda:
#   X -> Base
#   Y -> Codo1
#
# Mano derecha:
#   Y -> Codo2
#   Distancia dedos -> Pinza
#
# Se usan zonas muertas
# para evitar movimientos
# involuntarios.
#
# ==========================

CENTER_X_LOW = 0.40
CENTER_X_HIGH = 0.60

CENTER_Y_LOW = 0.40
CENTER_Y_HIGH = 0.60

# ==========================
# PINZA
# ==========================
#
# Distancia entre pulgar
# e indice.
#
# Mayor que el umbral:
#     abrir
#
# Menor que el umbral:
#     cerrar
#
# ==========================

PINZA_UMBRAL = 0.08

# ==========================
# HOME
# ==========================
#
# Posicion de referencia
# utilizada para sincronizar
# estado interno.
#
# NO se envia automaticamente.
#
# ==========================

HOME_CODO1 = 20
HOME_CODO2 = 140
HOME_PINZA = 135

# ==========================
# BASE
# ==========================
#
# Servo continuo
#
# ==========================

BASE_STOP = 95
BASE_DERECHA = 90
BASE_IZQUIERDA = 100

# ==========================
# CODO 1
# ==========================

CODO1_VERTICAL = 20
CODO1_HORIZONTAL = 110

# ==========================
# CODO 2
# ==========================

CODO2_ADELANTE = 80
CODO2_ATRAS = 140

# ==========================
# PINZA
# ==========================

PINZA_ABIERTA = 100
PINZA_CERRADA = 135