import base64
import numpy as np
import cv2
import traceback
import eventlet

from hand_detector import HandDetector


class CalculatorButton:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (225, 225, 225), cv2.FILLED)
        cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 50), cv2.FONT_HERSHEY_PLAIN,
                    2, (50, 50, 50), 2)

    def is_clicked(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            return True
        return False


CAPTURE_WIDTH = 1280
CAPTURE_HEIGHT = 720
BUTTON_LIST_VALUES = [['7', '8', '9', '*', 'CLR'],
                      ['4', '5', '6', '-', 'BKS'],
                      ['1', '2', '3', '+'],
                      ['0', '/', '.', '=']]
video_captures = {}
calculator_button_state = {}
calculator_context = {}
detector = HandDetector()


def generate_default_calculator_context():
    return {'equation': '', 'delay_counter': 0, 'button_list': list(), 'quit': False}


def generate_init_button_state():
    l = []
    for y, row in enumerate(BUTTON_LIST_VALUES):
        for x, val in enumerate(row):
            xpos = x * 100 + x*20 + 50
            ypos = y * 100 + y*20 + 50

            l.append(
                CalculatorButton((xpos, ypos), 100, 100, val))
    return l


def generate_videofeed(sid, socketio):
    def run():
        vs = video_captures[sid]
        try:
            while sid in calculator_context and not calculator_context[sid]['quit']:
                ok, frame = vs.read()
                if not ok:
                    continue
                frame = cv2.flip(frame, 1)
                frame = detector.find_hands(frame)
                landmarks, bbox = detector.find_position(frame)
                # cv2.rectangle(frame, (800, 70), (800 + 400, 70 + 100),
                #               (225, 225, 225), cv2.FILLED)

                # cv2.rectangle(frame, (800, 70), (800 + 400, 70 + 100),
                #               (50, 50, 50), 3)
                for button in calculator_button_state[sid]:
                    button.draw(frame)

                if len(landmarks) > 0:
                    length, cpt, _ = detector.find_distance(8, 12, frame)
                    x, y = cpt  # landmarks[8]

                    # If clicked check which button and perform action
                    # if length < 40 and calculator_context[sid]['delay_counter'] == 0:
                    if length < 40:
                        for button in calculator_button_state[sid]:
                            if button.is_clicked(x, y):
                                value = button.value
                                if value == '=':
                                    calculator_context[sid]['equation'] = str(
                                        eval(calculator_context[sid]['equation']))
                                elif value == 'CLR':
                                    calculator_context[sid]['equation'] = ''
                                elif value == 'BKS':
                                    calculator_context[sid]['equation'] = calculator_context[sid]['equation'][:-1]
                                else:
                                    calculator_context[sid]['equation'] += value
                                # calculator_context[sid]['delay_counter'] = 1

                    # if calculator_context[sid]['delay_counter'] != 0:
                    #     calculator_context[sid]['delay_counter'] += 1
                    #     if calculator_context[sid]['delay_counter'] > 10:
                    #         calculator_context[sid]['delay_counter'] = 0

                # cv2.putText(frame, calculator_context[sid]['equation'], (10, 450), cv2.FONT_HERSHEY_PLAIN,
                #             3, (0, 255, 0), 3)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = base64.b64encode(buffer).decode('utf-8')
                socketio.emit('gesture_calculator video feed',
                              "data:image/jpeg;base64,"+frame)
                socketio.emit('gesture_calculator state',
                              calculator_context[sid])
                eventlet.sleep(0.1)

            video_captures[sid].release()
            del video_captures[sid]
            del calculator_context[sid]
            del calculator_button_state[sid]
        except Exception:
            print("==", traceback.format_exc())
    socketio.start_background_task(run)


def calculator_init(sid, video_capture):
    video_capture.set(3, CAPTURE_WIDTH)
    video_capture.set(4, CAPTURE_HEIGHT)
    video_captures[sid] = video_capture
    calculator_context[sid] = generate_default_calculator_context()
    calculator_button_state[sid] = generate_init_button_state()


def calculator_remove(sid):
    if sid in calculator_context:
        calculator_context[sid]['quit'] = True
