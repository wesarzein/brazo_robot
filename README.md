# Control del brazo y umbrales

Este documento resume solo los gestos usados para mover el brazo robot y los umbrales que ajustan su sensibilidad.

## Requisitos

- Python 3.10 o superior.
- Camara web conectada y disponible.
- ESP32 conectado por USB con el firmware del brazo cargado.
- Permiso para usar el puerto serial del ESP32.
- Dependencias de Python:

```bash
pip install opencv-python mediapipe pillow customtkinter pyserial
```

## Ejecucion

Desde la carpeta del proyecto:

```bash
cd brazo_robot
python main.py
```

Al abrir la interfaz:

1. Selecciona el puerto COM del ESP32.
2. Presiona conectar.
3. Presiona sincronizar HOME si el brazo ya esta en la posicion de referencia.
4. Activa la comunicacion para empezar a enviar comandos.

Si la camara no abre, revisa `CAMERA_INDEX` en `config.py`. El valor por defecto es `0`.

## Controles

| Mano | Gesto / movimiento | Comando |
| --- | --- | --- |
| Izquierda cerrada | Mover muneca a la izquierda (`x < 0.40`) | Base derecha (`base = -1`) |
| Izquierda cerrada | Mover muneca a la derecha (`x > 0.60`) | Base izquierda (`base = 1`) |
| Izquierda abierta | Cualquier movimiento horizontal | Base detenida (`base = 0`) |
| Izquierda | Mover muneca arriba (`y < 0.40`) | Codo 1 positivo (`codo1 = 1`) |
| Izquierda | Mover muneca abajo (`y > 0.60`) | Codo 1 negativo (`codo1 = -1`) |
| Derecha | Mover muneca arriba (`y < 0.40`) | Codo 2 positivo (`codo2 = 1`) |
| Derecha | Mover muneca abajo (`y > 0.60`) | Codo 2 negativo (`codo2 = -1`) |
| Derecha | Separar pulgar e indice (`dist > 0.08`) | Abrir pinza (`pinza = -1`) |
| Derecha | Juntar pulgar e indice (`dist <= 0.08`) | Cerrar pinza (`pinza = 1`) |

## Umbrales

Los umbrales principales estan en `config.py` y se usan desde `vision/gesture_detector.py`.

| Umbral | Valor | Uso |
| --- | --- | --- |
| `CENTER_X_LOW` | `0.40` | Limite izquierdo de la zona muerta horizontal |
| `CENTER_X_HIGH` | `0.60` | Limite derecho de la zona muerta horizontal |
| `CENTER_Y_LOW` | `0.40` | Limite superior de la zona muerta vertical |
| `CENTER_Y_HIGH` | `0.60` | Limite inferior de la zona muerta vertical |
| `PINZA_UMBRAL` | `0.08` | Distancia normalizada entre pulgar e indice para abrir/cerrar la pinza |

## Zona muerta

Si la muneca queda entre `0.40` y `0.60` en el eje usado, el comando enviado es `0` y el servo se detiene. Esto evita movimientos involuntarios cerca del centro de la camara.

## Bloqueo de base

La base solo responde al eje X de la mano izquierda cuando esa mano esta cerrada. Si la mano izquierda esta abierta, el comando de base se fuerza a `0`, aunque la muneca este fuera de la zona muerta.
