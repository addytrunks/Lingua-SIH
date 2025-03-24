import eventlet
import translations as translator
from flask_cors import cross_origin, CORS
from flask import Flask, jsonify, Response, request
import sys
import asyncio

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/languages')
def get_languages():
    return jsonify(translator.get_languages())


@cross_origin
@app.route('/translate', methods=["POST"])
async def get_translation():
    try:
        lang_code = request.json.get('lang_code')
        text = request.json.get('text')
        if text is None:
            return Response(status=400)
        translated = await translator.get_translation(
            "en" if not lang_code else lang_code, text)
        return jsonify(translated)
    except Exception as ex:
        print("EXP::get_translation")
        print(ex)
        return Response(status=500)


if __name__ == "__main__":
    app.run("0.0.0.0", 5500, debug=True)
