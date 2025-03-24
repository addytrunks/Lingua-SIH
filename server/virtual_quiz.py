import base64
import cv2
import csv
from hand_detector import HandDetector
import cvzone
import time
import traceback
import eventlet


class QuizItem():
    def __init__(self, data):
        self.question = data[0]
        self.choices = data[1:5]
        self.answer = int(data[5])

        self.userAns = None

    def update(self, cursor, bboxs, frame):
        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x+1
                cv2.rectangle(frame, (x1, y1), (x2, y2),
                              (255, 43, 64), cv2.FILLED)


QUIZ_QUESTIONS_PATH = "./data/virtual_quiz_questions.csv"
CAPTURE_WIDTH = 1280
CAPTURE_HEIGHT = 720
video_captures = {}
quiz_context = {}
quiz_state = {}
detector = HandDetector()


def generate_default_quiz_state():
    return {'q_no': 0, 'quit': False}


def generate_default_quiz_context():
    l = []
    with open(QUIZ_QUESTIONS_PATH, newline='\n') as f:
        reader = csv.reader(f)
        questions = list(reader)[1:]
    for q in questions:
        l.append(QuizItem(q))
    return l


def generate_videofeed(sid, socketio):
    def run():
        vs = video_captures[sid]
        try:
            while sid in quiz_state and not quiz_state[sid]['quit']:
                ok, frame = vs.read()
                if not ok:
                    continue
                frame = cv2.flip(frame, 1)
                frame = detector.find_hands(frame)
                landmarks, bbox = detector.find_position(frame)
                if quiz_state[sid]['q_no'] < len(quiz_context[sid]):
                    mcq = quiz_context[sid][quiz_state[sid]['q_no']]
                    bboxes = []
                    frame, bbox = cvzone.putTextRect(
                        frame, mcq.question, [100, 100], 2, 2, colorT=(0, 0, 0), colorR=(248, 248, 248), colorB=(255, 43, 64), offset=50, border=5)
                    for i, choice in enumerate(mcq.choices):
                        frame, i_bbox = cvzone.putTextRect(frame, choice, [
                            100 if i % 2 == 0 else 400, 400 if i > 1 else 250], 2, 2, colorT=(0, 0, 0), colorR=(248, 248, 248), colorB=(255, 43, 64), offset=50, border=5)
                        bboxes.append(i_bbox)

                    if len(landmarks) > 0:
                        cursor = landmarks[8]
                        length, cpt, _ = detector.find_distance(8, 12, frame)
                        print(length)
                        if length < 50:
                            mcq.update(cpt, bboxes, frame)
                            if mcq.userAns is not None:
                                time.sleep(0.3)
                                quiz_state[sid]['q_no'] += 1
                else:
                    score = 0
                    for mcq in quiz_context[sid]:
                        if mcq.answer == mcq.userAns:
                            score += 1
                    score = round((score / len(quiz_context[sid])) * 100, 2)
                    frame, _ = cvzone.putTextRect(frame, "Quiz Completed", [
                        250, 300], 2, 2, colorT=(0, 0, 0), colorR=(248, 248, 248), colorB=(255, 43, 64), offset=50, border=5)
                    frame, _ = cvzone.putTextRect(frame, f'Your Score: {score}%', [
                        700, 300], 2, 2, colorT=((0, 0, 0) if score < 95 else (255, 255, 255)), colorR=((248, 248, 248) if score < 95 else (0, 178, 0)), colorB=((255, 43, 64) if score < 95 else (0, 178, 0)), offset=50, border=5)
                barValue = 150 + \
                    (950 // len(quiz_context[sid])) * quiz_state[sid]['q_no']
                cv2.rectangle(frame, (150, 600), (barValue, 650),
                              (0, 178, 0), cv2.FILLED)
                cv2.rectangle(frame, (150, 600), (1100, 650), (255, 43, 64), 5)
                frame, _ = cvzone.putTextRect(
                    frame, f'{round((quiz_state[sid]["q_no"] / len(quiz_context[sid])) * 100)}%', [1130, 635], 2, 2, colorT=(255, 43, 64), colorR=(248, 248, 248), offset=16)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = base64.b64encode(buffer).decode('utf-8')
                socketio.emit('virtual_quiz video feed',
                              "data:image/jpeg;base64,"+frame)
                socketio.emit('virtual_quiz state',
                              quiz_state[sid])
                eventlet.sleep(0.1)

            video_captures[sid].release()
            del video_captures[sid]
            del quiz_state[sid]
            del quiz_context[sid]
        except Exception:
            print("==", traceback.format_exc())
    socketio.start_background_task(run)


def quiz_init(sid, video_capture):
    video_capture.set(3, CAPTURE_WIDTH)
    video_capture.set(4, CAPTURE_HEIGHT)
    video_captures[sid] = video_capture
    quiz_state[sid] = generate_default_quiz_state()
    quiz_context[sid] = generate_default_quiz_context()


def quiz_remove(sid):
    if sid in quiz_state:
        quiz_state[sid]['quit'] = True
