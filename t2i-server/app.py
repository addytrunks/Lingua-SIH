import base64
from gradio_client import Client
from PIL import Image
import dotenv
import os
from flask import Flask, request, Response, jsonify
from flask_cors import CORS, cross_origin

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app, cors_allowed_origins="*")

client = Client('black-forest-labs/FLUX.1-schnell')


def generate_image(text):
    result = client.predict(
        prompt=text.lower(),
        seed=0,
        randomize_seed=True,
        width=512,
        height=512,
        num_inference_steps=4,
        api_name='/infer'
    )
    image_path, _ = result
    data = b''
    with open(image_path, mode='rb') as img:
        data = img.read()
    data = base64.b64encode(data).decode('utf-8')
    os.remove(image_path)
    return 'data:image/jpg;base64,'+data


@app.route('/', methods=['POST'])
@cross_origin()
def get_generated_image():
    text = request.json.get('text')
    if text is None:
        return Response(status=400)
    return jsonify({'image_data': generate_image(text)})


if __name__ == '__main__':
    try:
        app.run(host="0.0.0.0", port=5050, debug=True)
    except KeyboardInterrupt:
        app.stop()
        print("Exiting...")
