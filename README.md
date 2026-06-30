# Control de Brazo Robotico por Gestos

Este proyecto permite el control en tiempo real de un brazo robotico fisico (basado en ESP32) mediante gestos de las manos capturados por una camara, utilizando algoritmos de vision artificial.

El codigo esta dividido en dos partes principales: la aplicacion de control en la PC (Python) y el firmware para el microcontrolador (C++).

---

## Estructura del Proyecto

El espacio de trabajo esta organizado de la siguiente manera:

### 1. Controlador de PC (pc_controller/)
Contiene la aplicacion de Python que ejecuta el procesamiento de imagenes, la interfaz grafica y la comunicacion serial.
*   **pc_controller/main.py**: Orquestador principal que captura el video, procesa los gestos, actualiza la interfaz grafica y envia las instrucciones al puerto serial.
*   **pc_controller/config.py**: Configuracion centralizada de parametros (grados de los servos, velocidad serial y umbrales de deteccion).
*   **pc_controller/requirements.txt**: Archivo de dependencias necesarias para el entorno de Python.
*   **pc_controller/models/robot_state.py**: Estructura de datos que almacena el estado dinamico del brazo.
*   **pc_controller/vision/**: Modulos de vision artificial encargados del rastreo de manos (MediaPipe) y la deteccion de gestos.
*   **pc_controller/communication/serial_manager.py**: Gestiona la conexion y envio de datos a traves del puerto USB.
*   **pc_controller/gui/main_window.py**: Diseño de la interfaz grafica desarrollada con CustomTkinter.

### 2. Firmware del Microcontrolador (firmware/)
Proyecto configurado para PlatformIO que se encarga del control de los motores en la placa ESP32.
*   **firmware/platformio.ini**: Configuracion de PlatformIO (placa esp32dev, framework Arduino y dependencia de la libreria ESP32Servo).
*   **firmware/src/main.cpp**: Codigo fuente C++ que recibe las instrucciones seriales y controla los movimientos de los servomotores.

---

## Requisitos e Instalacion

### Requisitos de Python (Controlador de PC)
Se recomienda utilizar un entorno virtual con Python 3.10 o Python 3.11 para evitar conflictos de versiones.

1. Abra una terminal en el directorio raíz del proyecto y entre a la carpeta del controlador:
   ```bash
   cd pc_controller
   ```

2. Cree el entorno virtual:
   ```bash
   python -m venv .venv
   ```

3. Active el entorno virtual:
   * **Windows (PowerShell)**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   * **Windows (CMD)**:
     ```cmd
     .venv\Scripts\activate.bat
     ```
   * **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```

4. Instale las dependencias requeridas:
   ```bash
   pip install -r requirements.txt
   ```

5. Inicie la aplicacion:
   ```bash
   python main.py
   ```

### Requisitos de C++ (Firmware ESP32)
1. Abra la carpeta `firmware/` en VS Code (requiere la extension PlatformIO IDE instalada).
2. PlatformIO descargara de forma automatica la libreria de control de servos.
3. Conecte el ESP32 a la PC por puerto USB.
4. Presione el boton **Build (Verificar ✔️)** para compilar, o **Upload (Subir ➡️)** para cargar el firmware al ESP32.

---

## Mapeo de Gestos

El control de los motores del brazo responde a los movimientos de las muñecas y los dedos frente a la camara:

*   **Mano Izquierda**:
    *   **Eje X**: Controla la base del brazo (Servo continuo: giro izquierda, derecha o parada).
    *   **Eje Y**: Controla el Codo 1 (Servo posicional: movimiento vertical u horizontal).
*   **Mano Derecha**:
    *   **Eje Y**: Controla el Codo 2 (Servo posicional: movimiento adelante o atras).
    *   **Distancia Pulgar-Indice**: Controla la pinza del brazo (Abrir o Cerrar).

---

## Protocolo de Comunicacion

Las instrucciones se transmiten a 115200 baudios en formato ASCII:

*   **Trama Normal**: `B:<base>,C1:<codo1>,C2:<codo2>,P:<pinza>,S:<servos_activos>\n`
*   **Parada de Emergencia**: `B:0,C1:0,C2:0,P:0,S:0\n`
