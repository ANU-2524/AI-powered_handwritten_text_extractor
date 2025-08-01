import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import cv2
import numpy as np
import os
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def preprocess_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def extract_text_from_image(image_path):
    thresh = preprocess_image(image_path)
    text = pytesseract.image_to_string(thresh, lang='eng')
    return text

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300)
        temp_path = f"temp_page_{i}.png"
        pix.save(temp_path)
        text = extract_text_from_image(temp_path)
        full_text.append(text)
        os.remove(temp_path)
    return "\n\n".join(full_text).strip()
