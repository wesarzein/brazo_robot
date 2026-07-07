import math

from config import (
    CENTER_X_HIGH,
    CENTER_X_LOW,
    CENTER_Y_HIGH,
    CENTER_Y_LOW,
    PINZA_UMBRAL as CONFIG_PINZA_UMBRAL
)


class GestureDetector:

    # ==================================
    # ZONAS MUERTAS
    # ==================================

    X_LOW = CENTER_X_LOW
    X_HIGH = CENTER_X_HIGH

    Y_LOW = CENTER_Y_LOW
    Y_HIGH = CENTER_Y_HIGH

    PINZA_UMBRAL = CONFIG_PINZA_UMBRAL

    # ==================================
    # PROCESAMIENTO
    # ==================================

    def process(
        self,
        left_hand=None,
        right_hand=None
    ):

        state = {
            "base": 0,
            "codo1": 0,
            "codo2": 0,
            "pinza": 0
        }

        # ==========================
        # MANO IZQUIERDA
        # BASE + CODO1
        # ==========================

        if left_hand is not None:

            wrist = left_hand.landmark[0]

            x = wrist.x
            y = wrist.y
            left_hand_closed = self.hand_is_closed(
                left_hand
            )

            # ----------------------
            # BASE
            # ----------------------

            if left_hand_closed:

                state["base"] = self.axis_state(
                    x,
                    self.X_LOW,
                    self.X_HIGH,
                    -1,
                    1
                )

            # ----------------------
            # CODO 1
            # ----------------------

            state["codo1"] = self.axis_state(
                y,
                self.Y_LOW,
                self.Y_HIGH,
                1,
                -1
            )

        # ==========================
        # MANO DERECHA
        # CODO2 + PINZA
        # ==========================

        if right_hand is not None:

            wrist = right_hand.landmark[0]

            y = wrist.y

            # ----------------------
            # CODO2
            # ----------------------

            state["codo2"] = self.axis_state(
                y,
                self.Y_LOW,
                self.Y_HIGH,
                1,
                -1
            )

            # ----------------------
            # PINZA
            # ----------------------

            thumb = right_hand.landmark[4]
            index = right_hand.landmark[8]

            dist = math.sqrt(
                (thumb.x - index.x) ** 2
                +
                (thumb.y - index.y) ** 2
            )

            if dist > self.PINZA_UMBRAL:

                state["pinza"] = -1   # abrir

            else:

                state["pinza"] = 1    # cerrar

        return state

    # ==================================
    # UTILIDAD
    # ==================================

    def hand_is_open(self, hand):

        fingers = [
            (8, 6),
            (12, 10),
            (16, 14),
            (20, 18)
        ]

        count = 0

        for tip, pip in fingers:

            if (
                hand.landmark[tip].y
                <
                hand.landmark[pip].y
            ):
                count += 1

        return count >= 3

    def hand_is_closed(self, hand):

        return not self.hand_is_open(
            hand
        )

    def axis_state(
        self,
        value,
        low,
        high,
        low_state,
        high_state
    ):

        if value < low:
            return low_state

        if value > high:
            return high_state

        return 0
