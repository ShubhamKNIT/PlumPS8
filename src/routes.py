from service.extract_invoice import text_to_structured_invoice, image_to_structured_invoice
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import tempfile, os, time, json, re
from typing import Optional

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

router = APIRouter()

class TextInvoiceRequest(BaseModel):
    raw_text: str
    additional_info: Optional[str] = None

@router.post("/image")
async def process_image(file: UploadFile = File(...), additional_info: Optional[str] = Form(None)):
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(400, "Only PNG, JPG, and JPEG files are supported")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name
    
    try:
        return process_response(image_to_structured_invoice, temp_path, additional_info)
    finally:
        os.unlink(temp_path)

@router.post("/text")
async def process_text(request: TextInvoiceRequest):
    if not request.raw_text.strip():
        raise HTTPException(400, "raw_text cannot be empty")
    
    input_text = request.raw_text
    if request.additional_info:
        input_text += f"\n\nAdditional Info: {request.additional_info}"
    
    return process_response(text_to_structured_invoice, input_text)

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.get("/examples")
async def examples():
    try:
        from service.utils.examples import get_examples
        return get_examples()
    except Exception as e:
        return {"error": str(e)}

@router.post("/batch")
async def process_batch(files: list[UploadFile] = File(...)):
    start_time = time.time()
    results = []
    
    for file in files:
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            results.append({"filename": file.filename, "success": False, "error": "Unsupported file type"})
            continue
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file.write(await file.read())
            temp_path = temp_file.name
        
        try:
            response = process_response(image_to_structured_invoice, temp_path)
            results.append({
                "filename": file.filename,
                "success": response["success"],
                **({"data": response["data"]} if response["success"] else {"error": response["error"]})
            })
        finally:
            os.unlink(temp_path)
    
    return {
        "success": True,
        "total_files": len(files),
        "processed_files": sum(1 for r in results if r["success"]),
        "failed_files": sum(1 for r in results if not r["success"]),
        "results": results,
        "processing_time": time.time() - start_time
    }