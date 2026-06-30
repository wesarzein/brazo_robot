import cv2
import mediapipe as mp


class HandTracker:

    def __init__(self):

        self.mp_hands = mp.solutions.hands

        self.mp_draw = (
            mp.solutions.drawing_utils
        )

        self.hands = (
            self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.7
            )
        )

    # ==================================
    # DETECCION
    # ==================================

    def process(self, frame):

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = self.hands.process(rgb)

        left_hand = None
        right_hand = None

        if (
            results.multi_hand_landmarks
            and
            results.multi_handedness
        ):

            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks,
                results.multi_handedness
            ):

                label = (
                    handedness
                    .classification[0]
                    .label
                )

                if label == "Left":

                    left_hand = hand_landmarks

                elif label == "Right":

                    right_hand = hand_landmarks

        return (
            left_hand,
            right_hand,
            results
        )

    # ==================================
    # DIBUJO
    # ==================================

    def draw(
        self,
        frame,
        hand
    ):

        if hand is None:
            return

        self.mp_draw.draw_landmarks(
            frame,
            hand,
            self.mp_hands.HAND_CONNECTIONS
        )