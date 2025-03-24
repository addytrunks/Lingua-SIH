import pickle
import numpy as np
from js import fetch, window # type: ignore


double_hand_labels_dict = {0: 'A', 1: 'B', 2: 'D', 3: 'E', 4: 'F', 5: 'G', 6: 'H', 7: 'J', 8: 'K', 9: 'M', 10: 'N',
                           11: 'P', 12: 'Q', 13: 'R', 14: 'S', 15: 'T', 16: 'W', 17: 'X', 18: 'Y', 19: 'Z', 20: 'ACCIDENT', 21: 'HELP'}

single_hand_labels_dict = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: '9', 9: 'C', 10: 'I',
                           11: 'L', 12: 'O', 13: 'U', 14: 'V', 15: 'PAIN', 16: 'CALL', 17: 'NEXT', 18: 'BACKSPACE', 19: 'SPACE'}
single_hand_model=None
double_hand_model=None

async def loadIslModel():
    global single_hand_model, double_hand_model
    response = await fetch('/py/isl-alphabet-prediction/single_hand_model_word_seq(scikit-upgraded).p')
    array_buffer = await response.arrayBuffer()
    single_hand_model = pickle.loads(bytes(array_buffer.to_py()))['model']
    response = await fetch('/py/isl-alphabet-prediction/double_hand_model_word(scikit-upgraded).p')
    array_buffer = await response.arrayBuffer()
    double_hand_model = pickle.loads(bytes(array_buffer.to_py()))['model']


def predictIsl(res_data, num_hands):
    min_x = res_data[0][0].x
    min_y = res_data[0][0].y
    aux_data = []
    x_ = []
    y_ = []
    num_hands = len(res_data)
    for hand_landmarks in res_data:
        for hl in hand_landmarks:
            x_.append(hl.x)
            y_.append(hl.y)
        min_x = min(x_)
        min_y = min(y_)
        for hl in hand_landmarks:
            aux_data.append(hl.x - min_x)
            aux_data.append(hl.y - min_y)
    char = ''
    try:
        prediction = (single_hand_model if num_hands == 1 else double_hand_model).predict([np.asarray(aux_data)])
        char = (single_hand_labels_dict if num_hands == 1 else double_hand_labels_dict)[int(
                prediction[0])]
    except ValueError as e:
        print(f"Error during prediction: {e}")
    return char