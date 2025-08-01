import pytesseract
import cv2
import os
import json
import csv
from datetime import datetime
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return thresh

def extract_text_from_path(path):
    ext = os.path.splitext(path)[1].lower()

    text = ""

    if ext == ".pdf":
        try:
            images = convert_from_path(path)
            for i, img in enumerate(images):
                temp_path = f"temp_page_{i}.png"
                img.save(temp_path)
                processed_image = preprocess_image(temp_path)
                text += pytesseract.image_to_string(processed_image, lang='eng') + "\n"
                os.remove(temp_path)
        except Exception as e:
            print("PDF conversion error:", e)
    else:
        processed_image = preprocess_image(path)
        text = pytesseract.image_to_string(processed_image, lang='eng')

    save_output(path, text)
    return text

def save_output(img_path, text):
    base_name = os.path.basename(img_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save JSON
    json_data = {
        "filename": base_name,
        "timestamp": timestamp,
        "extracted_text": text
    }
    json_path = f"extracted_data/{base_name}_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)

    # Save CSV
    csv_path = f"extracted_data/extracted_texts.csv"
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["filename", "timestamp", "text"])
        writer.writerow([base_name, timestamp, text])
