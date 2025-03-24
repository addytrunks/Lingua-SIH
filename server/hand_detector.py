import cv2
import mediapipe as mp
import time
import math
import numpy as np


class HandDetector():
    def __init__(self, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.hands = mp.solutions.hands.Hands()

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    mp.solutions.drawing_utils.draw_landmarks(img, hand_lms,
                                                              mp.solutions.hands.HAND_CONNECTIONS)

        return img

    def find_position(self, img, handNo=0, draw=True):
        x_l = []
        y_l = []
        bbox = []
        self.lamdmarks = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(hand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                x_l.append(cx)
                y_l.append(cy)
                # print(id, cx, cy)
                self.lamdmarks.append([cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(x_l), max(x_l)
            ymin, ymax = min(y_l), max(y_l)
            bbox = xmin, ymin, xmax, ymax

        return self.lamdmarks, bbox

    def find_distance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lamdmarks[p1]
        x2, y2 = self.lamdmarks[p2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, (cx, cy), [x1, y1, x2, y2, cx, cy]
