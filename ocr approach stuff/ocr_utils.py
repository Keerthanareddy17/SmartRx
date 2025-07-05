import easyocr
from PIL import Image
import os

reader = easyocr.Reader(['en'])

def extract_text_from_image(image_path):
    """
    Perform OCR using EasyOCR and return extracted text.
    """
    results = reader.readtext(image_path)
    extracted_text = ""

    for (bbox, text, prob) in results:
        extracted_text += text + "\n"

    return extracted_text