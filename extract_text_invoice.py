from google import genai
from examples import get_examples

def get_structured_invoice(query_invoice: str) -> str:
    client = genai.Client()

    examples = get_examples()

    query_output = ""

    content = f"""
        Given the sample input with output.
        For the query input, find the query output.
        {examples}
        
        Query Input:
        {query_invoice}

        Query Output:
        {query_output}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite", contents=content
    )
    # print(response.text)
    return response.text

if __name__ == "__main__":

    query_input = ""

    with open("parsed_img/medbill20_clean_lines.txt", "r", encoding="utf-8") as f:
        query_input = f.read()

    query_output = get_structured_invoice(query_input)
    print(query_output)