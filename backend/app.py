from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = "../uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/extract-text", methods=["POST"])
def extract_text():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image = request.files['image']
    path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(path)

    text = pytesseract.image_to_string(Image.open(path), lang='eng')  # Add 'hin' or other langs later
    return jsonify({"text": text})

if __name__ == "__main__":
    app.run(debug=True)
