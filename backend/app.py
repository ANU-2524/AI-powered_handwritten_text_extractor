from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from ocr_model import extract_text_from_image, extract_text_from_pdf

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:500", "https://ai-powered-handwritten-text-extract.vercel.app"]}})


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/extract", methods=["POST"])
def extract_text():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)

    try:
        if filename.lower().endswith('.pdf'):
            extracted_text = extract_text_from_pdf(filename)
        else:
            extracted_text = extract_text_from_image(filename)
        if not extracted_text.strip():
            raise ValueError("Empty OCR result")
        return jsonify({"text": extracted_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(filename)

if __name__ == "__main__":
    # ✅ This allows Render to bind to the correct port and host
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
