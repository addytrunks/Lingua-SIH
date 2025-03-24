import base64
import numpy as np
import cv2
import traceback
# from auto_suggest import get_suggestions
import mediapipe as mp
import pickle
import eventlet

video_captures = {}
video_predictions_context = {}
DEFAULT_PREDICTIONS_CONTEXT = {'str': '', 'pts': [
], 'count': -1, 'prev_char': "", 'ten_prev_char': [" " for _ in range(10)], 'quit': False}

single_hand_model_dict = pickle.load(
    open('./data/isl_predictor_saved_models/single_hand_model_word_seq.p', 'rb'))
print(single_hand_model_dict)
single_hand_model = single_hand_model_dict['model']

double_hand_model_dict = pickle.load(
    open('./data/isl_predictor_saved_models/double_hand_model_word.p', 'rb'))
double_hand_model = double_hand_model_dict['model']
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True,
                       min_detection_confidence=0.3, max_num_hands=2)

double_hand_labels_dict = {0: 'A', 1: 'B', 2: 'D', 3: 'E', 4: 'F', 5: 'G', 6: 'H', 7: 'J', 8: 'K', 9: 'M', 10: 'N',
                           11: 'P', 12: 'Q', 13: 'R', 14: 'S', 15: 'T', 16: 'W', 17: 'X', 18: 'Y', 19: 'Z', 20: 'ACCIDENT', 21: 'HELP'}

single_hand_labels_dict = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: '9', 9: 'C', 10: 'I',
                           11: 'L', 12: 'O', 13: 'U', 14: 'V', 15: 'PAIN', 16: 'CALL', 17: 'NEXT', 18: 'BACKSPACE', 19: 'SPACE'}


def predict(test_image, sid):
    frame = test_image
    char = ''

    data_aux = []
    x_ = []
    y_ = []

    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        num_hands = len(results.multi_hand_landmarks)

        for hand_landmarks in results.multi_hand_landmarks:

            # Collect landmark coordinates
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            # Normalize landmarks
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        x1 = int(min(x_) * W) - 10
        y1 = int(min(y_) * H) - 10
        x2 = int(max(x_) * W) - 10
        y2 = int(max(y_) * H) - 10

        # Check if it's a single hand or double hand and predict accordingly
        try:
            if num_hands == 1:
                # Single hand prediction
                prediction = single_hand_model.predict([np.asarray(data_aux)])
                predicted_character = single_hand_labels_dict[int(
                    prediction[0])]
            else:
                # Double hand prediction
                prediction = double_hand_model.predict([np.asarray(data_aux)])
                predicted_character = double_hand_labels_dict[int(
                    prediction[0])]

            # Draw bounding box and predicted character
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 64, 43), 3,
                        cv2.LINE_AA)
            char = predicted_character

        except ValueError as e:
            print(f"Error during prediction: {e}")

        if char == "SPACE":
            char = " "

        if char == "NEXT" and video_predictions_context[sid]['prev_char'] != "NEXT":
            if video_predictions_context[sid]['ten_prev_char'][(video_predictions_context[sid]['count']-2) % 10] != "NEXT":
                prev_char = video_predictions_context[sid]['ten_prev_char'][(
                    video_predictions_context[sid]['count']-2) % 10]
                if prev_char == "BACKSPACE":
                    video_predictions_context[sid]['str'] = video_predictions_context[sid]['str'][0:-1]
                elif '0' <= prev_char and prev_char <= '9':
                    if len(video_predictions_context[sid]['word_suggestions']) != 0:
                        select_predictions_suggestion(
                            sid, video_predictions_context[sid]['word_suggestions'][int(prev_char)])
                else:
                    if video_predictions_context[sid]['ten_prev_char'][(video_predictions_context[sid]['count'] - 2) % 10] != "BACKSPACE":
                        video_predictions_context[sid]['str'] = video_predictions_context[sid]['str'] + prev_char
            else:
                if video_predictions_context[sid]['ten_prev_char'][(video_predictions_context[sid]['count'] - 0) % 10] != "BACKSPACE":
                    video_predictions_context[sid]['str'] = video_predictions_context[sid]['str'] + \
                        video_predictions_context[sid]['ten_prev_char'][(
                            video_predictions_context[sid]['count'] - 0) % 10]
        if char == " " and (len(video_predictions_context[sid]['str']) != 0 and video_predictions_context[sid]['str'][-1] != " "):
            video_predictions_context[sid]['str'] = video_predictions_context[sid]['str'] + " "
        video_predictions_context[sid]['prev_char'] = char
        video_predictions_context[sid]['count'] += 1
        video_predictions_context[sid]['ten_prev_char'][video_predictions_context[sid]
                                                        ['count'] % 10] = char
    word_suggestions = []
    word = ""
    if len(video_predictions_context[sid]['str'].strip()) != 0:
        st = video_predictions_context[sid]['str'].rfind(" ")
        ed = len(video_predictions_context[sid]['str'])
        word = video_predictions_context[sid]['str'][st+1:ed]
        word = word
        if len(word.strip()) != 0:
            word_suggestions.extend(get_suggestions(word.lower()))
    video_predictions_context[sid].update(
        {'ch': str(char), 'word': word, 'word_suggestions': word_suggestions})
    return frame


def predict_landmarks(landmarks):
    char = ''
    min_x = landmarks[0][0]['x']
    min_y = landmarks[0][0]['y']
    aux_data = []
    x_ = []
    y_ = []
    num_hands = len(landmarks)
    for hand_landmarks in landmarks:
        for hl in hand_landmarks:
            x_.append(hl['x'])
            y_.append(hl['y'])
        min_x = min(x_)
        min_y = min(y_)
        for hl in hand_landmarks:
            aux_data.append(hl['x'] - min_x)
            aux_data.append(hl['y'] - min_y)
    char = ''
    try:
        prediction = (single_hand_model if num_hands ==
                      1 else double_hand_model).predict([np.asarray(aux_data)])
        char = (single_hand_labels_dict if num_hands == 1 else double_hand_labels_dict)[int(
            prediction[0])]
    except ValueError as e:
        print(f"Error during prediction: {e}")
    return char


def call_predictions_action(action, sid):
    match action:
        case 'backspace':
            video_predictions_context[sid]['str'] = video_predictions_context[sid]['str'][:-1]
        case 'next':
            video_predictions_context[sid]['str'] = video_predictions_context[sid]['str'] + \
                video_predictions_context[sid]['ch']
        case 'space':
            video_predictions_context[sid]['str'] += '  '
        case 'clear':
            video_predictions_context[sid] = DEFAULT_PREDICTIONS_CONTEXT.copy()
        case _:
            pass


def select_predictions_suggestion(sid, suggestion):
    curr_str = video_predictions_context[sid]['str'].split(' ')
    curr_word = video_predictions_context[sid]['word']
    out_str = ''
    if curr_str[-1].lower() == curr_word.lower():
        out_str += ' '.join(curr_str[:-1])
    video_predictions_context[sid]['word'] = suggestion.upper()
    video_predictions_context[sid][
        'str'] = f'{out_str}{"" if len(out_str)==0 or out_str[-1]==" " else " "}{suggestion.upper()} '


def select_context_predictions_suggestion(context, suggestion):
    curr_str = context['str'].split(' ')
    curr_word = context['word']
    out_str = ''
    if curr_str[-1].lower() == curr_word.lower():
        out_str += ' '.join(curr_str[:-1])
    context['word'] = suggestion.upper()
    context[
        'str'] = f'{out_str}{"" if len(out_str)==0 or out_str[-1]==" " else " "}{suggestion.upper()} '


def generate_frame(sid, frame):
    if sid not in video_predictions_context or video_predictions_context[sid]['quit']:
        return [frame, video_predictions_context[sid]]
    frame = predict(frame, sid)
    return (
        frame,
        video_predictions_context[sid]
    )


def generate_videofeed(sid, socketio):
    def run():
        vs = video_captures[sid]
        try:
            while sid in video_predictions_context and not video_predictions_context[sid]['quit']:
                ok, frame = vs.read()
                if not ok:
                    continue
                frame = predict(frame, sid)
                ret, buffer = cv2.imencode('.jpg', frame)
                img = base64.b64encode(buffer).decode('utf-8')
                socketio.emit('video feed', "data:image/jpeg;base64,"+img)
                socketio.emit('predictions', video_predictions_context[sid])
                eventlet.sleep(0.1)
            video_captures[sid].release()
            del video_captures[sid]
            del video_predictions_context[sid]
        except Exception:
            print("==", traceback.format_exc())
    socketio.start_background_task(run)


def predictions_init(sid, video_capture):
    video_captures[sid] = video_capture
    video_predictions_context[sid] = DEFAULT_PREDICTIONS_CONTEXT.copy()


def predictions_remove(sid):
    if sid in video_predictions_context:
        video_predictions_context[sid]['quit'] = True
