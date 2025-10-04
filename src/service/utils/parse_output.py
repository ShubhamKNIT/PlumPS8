import time, json, re

def parse_ai_response(response_text: str) -> dict:
    """Parse AI response, extracting JSON from markdown blocks if needed."""
    if not isinstance(response_text, str):
        return response_text
    
    # Try direct JSON parsing
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass
    
    # Extract from markdown blocks
    for pattern in [r'```json\s*([\s\S]*?)\s*```', r'```\s*([\s\S]*?)\s*```']:
        for match in re.findall(pattern, response_text, re.IGNORECASE):
            try:
                clean = match.strip()
                if clean.startswith('{') and clean.endswith('}'):
                    return json.loads(clean)
            except json.JSONDecodeError:
                continue
    
    return {"raw_output": response_text, "note": "Output was not in JSON format"}

def process_response(processor_func, input_data, additional_info=None):
    """Common processing logic for all endpoints."""
    start_time = time.time()
    try:
        result = parse_ai_response(processor_func(input_data))
        if additional_info:
            result["additional_info"] = additional_info
        return {
            "success": True,
            "data": result,
            "processing_time": time.time() - start_time
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "processing_time": time.time() - start_time
        }