import eventlet
from text_isl_preprocessing import RailwaysAnnouncementPreprocessor
from sigml_isl_preprocessing import load_sigml_data
from isl_text_preprocessor import ISLTextPreprocessor
from lf_csv_helper import LfCsvHelper
import landmark_detector as lmd
import speech2text as s2t
import text_summarization as summarizer
import isl_predictor as predictor
import ssl
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit
from flask import Flask, request, Response, jsonify, render_template, send_from_directory
from flask_cors import CORS, cross_origin
import time
from text_to_emoji import TextToEmoji

load_dotenv()

lf_csv_helper = LfCsvHelper()
islTextPreprocessor = ISLTextPreprocessor()
preprocessor_words = {i: lf_csv_helper.get_words_by_category(
    i) for i in lf_csv_helper.get_categories()}
all_preprocessor_words = lf_csv_helper.get_all_words()
preprocessor_words['sigml'] = load_sigml_data()
textToEmoji = TextToEmoji()

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


@cross_origin
@app.route('/api/summarize', methods=['POST'])
def get_summary():
    text = request.json.get('text')
    if text is None:
        return Response(status=400)
    summary = summarizer.get_summarized_text(text)
    return jsonify({'summary': summary})


@cross_origin
@app.route('/api/preprocess-sigml', methods=['POST'])
def api_preprocess_sigml():
    text = request.json.get('text')
    if text is None:
        return Response(status=400)
    result = islTextPreprocessor.preprocess(text, preprocessor_words['sigml'])
    return jsonify({'result': result})


@cross_origin
@app.route('/api/speechttext', methods=['POST'])
def get_speechttext():
    audio = request.json.get('audio')
    if audio is None:
        return Response(status=400)
    text_res = s2t.speech_to_text_translate(audio)
    if 'error' in text_res:
        return Response(status=500)
    return jsonify({'text': text_res})


@cross_origin
@app.route('/api/texttemoji', methods=['POST'])
def get_speechtemoji():
    text = request.json.get('text')
    if text is None:
        return Response(status=400)
    text_res = textToEmoji.generate(text)
    if 'error' in text_res:
        return Response(status=500)
    return jsonify({'text': text_res})


@cross_origin
@app.route('/api/predictisl', methods=["POST"])
def api_predictisl():
    landmarks = request.json.get('landmarks')
    if landmarks is None:
        return Response(status=400)
    result = predictor.predict_landmarks(landmarks)
    if not result:
        return Response(status=500)
    return jsonify({'char': result})


@socketio.on('predict_isl')
def socketid_predictisl(landmarks):
    sid = request.sid
    if not landmarks:
        return

    result = predictor.predict_landmarks(landmarks)
    emit('prediction_feed', result, to=sid)


@socketio.on('request_isl_feed')
def socketid_requestislfeed(sentence, category):
    sid = request.sid
    if not sentence:
        return
    if not category:
        category = 'railway'

    def run(sent):
        sent = sent.lower().replace('.', '')
        words = islTextPreprocessor.preprocess(sent, all_preprocessor_words)
        for img_str in lmd.render_sentence(words):
            socketio.emit(
                'isl_feed', "data:image/jpeg;base64,"+img_str, to=sid)
            eventlet.sleep(0.005)

    socketio.start_background_task(run, sentence)


@socketio.on('connect')
def socketio_onconnect():
    sid = request.sid
    print("Connected: ", sid)


@socketio.on('disconnect')
def socketio_ondisconnect():
    sid = request.sid
    print("Disconnected: ", sid)


# @socketio.on("gesture_calculator video feed start")
# def socketio_videofeed():
#     gesture_calculator.generate_videofeed(request.sid, socketio)


# @socketio.on("virtual_quiz video feed start")
# def socketio_videofeed():
#     virtual_quiz.generate_videofeed(request.sid, socketio)


if __name__ == '__main__':
    try:
        socketio.run(app, host="0.0.0.0", debug=True)
    except KeyboardInterrupt:
        print("Exiting...")
