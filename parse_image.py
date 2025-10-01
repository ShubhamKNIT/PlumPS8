from langchain.schema import HumanMessage
from chat_model import chat
import os

def parse_invoice(image_path: str) -> str:
    if os.path.exists(image_path) is False:
        print(f"Image path {image_path} does not exist.")
        return None
    
    prompt = (
        "You are an invoice parser. Extract billing details from \
         this image. Also identify currency, mention input source for token as image"
    )
    
    messages = [
        HumanMessage(content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": f"{image_path}"}
        ])
    ]

    # response = chat.invoke(messages)
    response = chat.invoke_model(messages)
    return response.content

# if __name__ == "__main__":
#     extracted_text = parse_invoice("img/medbill1.png")
#     with io.open("parsed_img/medbill1.txt", "w", encoding="utf-8") as f:
#         f.write(extracted_text)
#         f.write("Source: image")
#     print(extracted_text)
    # BILL_PATH = "img"
    # RESULT_PATH = "parsed_img"
    # os.makedirs(RESULT_PATH, exist_ok=True)

    # img_li = os.listdir(BILL_PATH)
    # for img_path in img_li:
    #     text_op_path = '.'.join([img_path.split('.')[0], "txt"])
    #     print(text_op_path)

    #     extracted_text = parse_invoice(f"img/{img_path}")
    #     with io.open(f"{RESULT_PATH}/{text_op_path}", "w", encoding="utf-8") as f:
    #         f.write(extracted_text)
    #     print(extracted_text)
