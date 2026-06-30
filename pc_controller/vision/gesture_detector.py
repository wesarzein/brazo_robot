import math


class GestureDetector:

    # ==================================
    # ZONAS MUERTAS
    # ==================================

    X_LOW = 0.40
    X_HIGH = 0.60

    Y_LOW = 0.40
    Y_HIGH = 0.60

    PINZA_UMBRAL = 0.08

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

            # ----------------------
            # BASE
            # ----------------------

            if x < self.X_LOW:

                state["base"] = -1

            elif x > self.X_HIGH:

                state["base"] = 1

            else:

                state["base"] = 0

            # ----------------------
            # CODO 1
            # ----------------------

            if y < self.Y_LOW:

                state["codo1"] = 1

            elif y > self.Y_HIGH:

                state["codo1"] = -1

            else:

                state["codo1"] = 0

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

            if y < self.Y_LOW:

                state["codo2"] = 1

            elif y > self.Y_HIGH:

                state["codo2"] = -1

            else:

                state["codo2"] = 0

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