from flask import Flask, request, send_file
from gradio_client import Client
import io
from PIL import Image

app = Flask(__name__)

client = Client("https://cloudtheboi-stabilityai-stable-diffusion-xl-base-1-0.hf.space/")

@app.route('/')
def index():
    return '''
        <form action="/generate" method="post">
            <label for="text">Enter Text:</label>
            <input type="text" id="text" name="text">
            <input type="submit" value="Generate Image">
        </form>
    '''

@app.route('/generate', methods=['POST'])
def generate():
    text_input = request.form['text']
    result = client.predict(text_input, api_name="/predict")
    image_bytes = result.encode()
    image = Image.open(io.BytesIO(image_bytes))
    byte_io = io.BytesIO()
    image.save(byte_io, 'PNG')
    byte_io.seek(0)
    return send_file(byte_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
