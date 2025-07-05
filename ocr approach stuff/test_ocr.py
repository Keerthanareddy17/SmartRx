from ocr_utils import extract_text_from_image

image_path = "/Users/katasanikeerthanareddy/Documents/SmartRx/sample_data/sample2.jpeg"

try:
    text = extract_text_from_image(image_path)
    print("hehe.......here's the extracted text : ")
    print(text)

except Exception as e:
    print(f"[ERROR {e}]")