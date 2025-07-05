from doctr.io import DocumentFile
from doctr.models import ocr_predictor

# Load light OCR model (text detection + recognition)
model = ocr_predictor(pretrained=True)

def extract_text_from_image(image_path):
    """
    Run OCR on image using DocTR.
    """
    doc = DocumentFile.from_images(image_path)
    result = model(doc)

    # Convert result to string
    text = result.render()
    return text
