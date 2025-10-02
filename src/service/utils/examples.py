from random import randint

def load_sample_data(i: int) -> str:
    ip, op = "", ""
    with open(f"parsed_img/medbill{i}_clean_lines.txt", "r", encoding="utf-8") as f:
        ip = f.read()
    
    with open(f"parsed_output/medbill{i}_op.txt", "r", encoding="utf-8") as f:
        op = f.read()

    return ip, op
    
def get_examples() -> str:
    i = randint(1, 10)
    j = randint(11, 20)
    sample_input_1, sample_output_1 = load_sample_data(i)
    sample_input_2, sample_output_2 = load_sample_data(j)

    examples = f"""
        Example 1:
        Input:
        {sample_input_1}
        Output:
        {sample_output_1}

        Example 2:
        Input:
        {sample_input_2}
        Output:
        {sample_output_2}
    """

    return examples