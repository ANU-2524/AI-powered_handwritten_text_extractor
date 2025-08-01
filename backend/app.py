from flask import Flask, request, jsonify
import os
from ocr_model import extract_text_from_path
from PIL import Image
import io
import tempfile
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
EXTRACTED_FOLDER = 'extracted_data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACTED_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type'}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        extracted_text = extract_text_from_path(filepath)

        if not extracted_text.strip():
            return jsonify({'error': 'No text found'}), 400

        return jsonify({'extracted_text': extracted_text})

    except Exception as e:
        print("OCR Error:", e)
        return jsonify({'error': 'Error extracting text. Please make sure you are uploading a clear image or valid PDF.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
