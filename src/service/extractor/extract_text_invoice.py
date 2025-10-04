from google import genai
from google.genai import types
from service.utils.prompts import get_examples, get_system_prompt
from service.utils.parse_output import parse_ai_response

def get_structured_invoice(query_invoice: str) -> str:
    client = genai.Client()

    examples = get_examples()
    
    system_prompt = get_system_prompt()

    content = f"""
        {examples}

        Extract structured medical billing information from the following text. Follow the system instructions exactly and ensure all financial data is captured accurately.

        Query Input:
        {query_invoice}

        JSON Output:
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.1,
            max_output_tokens=2048,
        ),
        contents=content
    )
    return response.text

# if __name__ == "__main__":
#     # Test with sample data
#     query_input = ""
    
#     with open("../sample/sample_image_clean_lines.txt", "r", encoding="utf-8") as f:
#         query_input = f.read()
    
#     result = get_structured_invoice(query_input)
#     # print("Raw response:", result)
#     parsed_result = parse_ai_response(result)

#     import json
#     print("Parsed JSON:", json.dumps(parsed_result, indent=2))