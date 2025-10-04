import os
from service.extractor.extract_img_invoice import process_image_to_lines
from service.extractor.extract_text_invoice import get_structured_invoice

def text_to_structured_invoice(raw_text: str) -> str:
    structured_invoice = get_structured_invoice(raw_text)
    return structured_invoice

def image_to_structured_invoice(image_path: str) -> str:
    process_image_to_lines(image_path)
    
    text_invoice = ""
    with open(f"{os.path.splitext(image_path)[0]}_clean_lines.txt", "r", encoding="utf-8") as f:
        text_invoice = f.read()

    return get_structured_invoice(text_invoice)

# if __name__ == "__main__":
#     image_path = "sample_image.png"
#     output = image_to_structured_invoice(image_path)

#     with open("output.txt", "w", encoding="utf-8") as f:
#         f.write(output)

#     print(output)