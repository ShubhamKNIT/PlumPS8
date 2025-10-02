from google import genai

def invoke_model(content):
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=content
    )
    # print(response.text)
    return response.text

if __name__ == "__main__":
    sample_input = ""
    sample_output = ""
    query_input = ""
    query_output = ""

    with open("parsed_img/medbill1_clean_lines.txt", "r", encoding="utf-8") as f:
        sample_input = f.read()

    with open("parsed_output/medbill1_op.txt", "r", encoding="utf-8") as f:
        sample_output = f.read()

    with open("parsed_img/medbill13_clean_lines.txt", "r", encoding="utf-8") as f:
        query_input = f.read()

    prompt = f"""
                Given the sample input with output. 
                Find the query output. 
                extracted_data for output can be dynamic with query.
                Sample Input: \n
                {sample_input} \n
                Sample Output: \n
                {sample_output} \n

                Query Input: \n
                {query_input} \n
                Query Output: \n
                {query_output}
              """
    
    query_output = invoke_model(prompt)
    print(query_output)