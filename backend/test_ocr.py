from PIL import Image
import pytesseract

# Tell pytesseract where the Tesseract executable is
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load image
image_path = "./sample.png"  # Put your handwritten image in the same folder
img = Image.open(image_path)

# Extract text
extracted_text = pytesseract.image_to_string(img, lang='eng')

print("===== Extracted Text =====")
print(extracted_text)
