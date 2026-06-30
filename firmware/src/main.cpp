#include <Arduino.h>
#include <ESP32Servo.h>

Servo base;
Servo codo1;
Servo codo2;
Servo pinza;

// =====================
// PINES
// =====================
const int PIN_BASE  = 17;
const int PIN_CODO1 = 19;
const int PIN_CODO2 = 21;
const int PIN_PINZA = 18;

// =====================
// CALIBRACION REAL
// =====================

// PINZA
const int PINZA_ABIERTA = 100;
const int PINZA_CERRADA = 135;

// CODO 1
const int CODO1_VERTICAL   = 20;
const int CODO1_HORIZONTAL = 110;

// CODO 2
const int CODO2_ADELANTE = 80;
const int CODO2_ATRAS    = 140;

// BASE CONTINUA
const int BASE_DERECHA   = 90;
const int BASE_STOP      = 95;
const int BASE_IZQUIERDA = 100;

// =====================
// POSICIONES LOGICAS
// =====================
//
// IMPORTANTE:
// Estas variables solo sirven para
// limitar movimientos.
//
// NO se escriben al arrancar.
//
int posPinza = PINZA_CERRADA;   // 135
int posCodo1 = CODO1_VERTICAL;  // 20
int posCodo2 = CODO2_ATRAS;     // 140

// =====================
// COMANDOS
// =====================
//
// -1 = sentido negativo
//  0 = parar
// +1 = sentido positivo
//
int cmdBase  = 0;
int cmdCodo1 = 0;
int cmdCodo2 = 0;
int cmdPinza = 0;

bool servosActivos = true;

String trama = "";

unsigned long lastUpdate = 0;

// Declaraciones de funciones para compatibilidad C++ puro (PlatformIO)
void recibirSerial();
void procesarTrama(String data);
void moverServos();

// =====================================================
void setup()
{
    Serial.begin(115200);

    base.setPeriodHertz(50);
    codo1.setPeriodHertz(50);
    codo2.setPeriodHertz(50);
    pinza.setPeriodHertz(50);

    base.attach(PIN_BASE, 500, 2400);
    codo1.attach(PIN_CODO1, 500, 2400);
    codo2.attach(PIN_CODO2, 500, 2400);
    pinza.attach(PIN_PINZA, 500, 2400);

    // NO ENVIAR write()
    // NO MOVER NADA AL ARRANCAR

    Serial.println("BRAZO LISTO");

    Serial.println("Formato:");
    Serial.println("B:0,C1:0,C2:0,P:0,S:1");

    Serial.println("BASE:");
    Serial.println("-1=derecha 0=stop 1=izquierda");

    Serial.println("CODO1:");
    Serial.println("-1=vertical 1=horizontal");

    Serial.println("CODO2:");
    Serial.println("-1=adelante 1=atras");

    Serial.println("PINZA:");
    Serial.println("-1=abrir 1=cerrar");
}

// =====================================================
void loop()
{
    recibirSerial();
    moverServos();
}

// =====================================================
void recibirSerial()
{
    while (Serial.available())
    {
        char c = Serial.read();

        if (c == '\n')
        {
            procesarTrama(trama);
            trama = "";
        }
        else
        {
            trama += c;
        }
    }
}

// =====================================================
void procesarTrama(String data)
{
    int b, c1, c2, p, s;

    int r = sscanf(
        data.c_str(),
        "B:%d,C1:%d,C2:%d,P:%d,S:%d",
        &b,
        &c1,
        &c2,
        &p,
        &s
    );

    if (r != 5)
    {
        Serial.println("ERR TRAMA");
        return;
    }

    cmdBase  = constrain(b, -1, 1);
    cmdCodo1 = constrain(c1, -1, 1);
    cmdCodo2 = constrain(c2, -1, 1);
    cmdPinza = constrain(p, -1, 1);

    servosActivos = (s == 1);
}

// =====================================================
void moverServos()
{
    if (!servosActivos)
    {
        base.write(BASE_STOP);
        return;
    }

    if (millis() - lastUpdate < 20)
        return;

    lastUpdate = millis();

    // =====================
    // BASE CONTINUA
    // =====================

    if (cmdBase == 1)
        base.write(BASE_IZQUIERDA);

    else if (cmdBase == -1)
        base.write(BASE_DERECHA);

    else
        base.write(BASE_STOP);

    // =====================
    // CODO 1
    // =====================

    if (cmdCodo1 == 1)
    {
        if (posCodo1 < CODO1_HORIZONTAL)
        {
            posCodo1++;
            codo1.write(posCodo1);
        }
    }
    else if (cmdCodo1 == -1)
    {
        if (posCodo1 > CODO1_VERTICAL)
        {
            posCodo1--;
            codo1.write(posCodo1);
        }
    }

    // =====================
    // CODO 2
    // =====================

    if (cmdCodo2 == 1)
    {
        if (posCodo2 < CODO2_ATRAS)
        {
            posCodo2++;
            codo2.write(posCodo2);
        }
    }
    else if (cmdCodo2 == -1)
    {
        if (posCodo2 > CODO2_ADELANTE)
        {
            posCodo2--;
            codo2.write(posCodo2);
        }
    }

    // =====================
    // PINZA
    // =====================

    if (cmdPinza == 1)
    {
        if (posPinza < PINZA_CERRADA)
        {
            posPinza++;
            pinza.write(posPinza);
        }
    }
    else if (cmdPinza == -1)
    {
        if (posPinza > PINZA_ABIERTA)
        {
            posPinza--;
            pinza.write(posPinza);
        }
    }
}
