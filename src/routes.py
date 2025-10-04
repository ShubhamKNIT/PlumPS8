from service.extract_invoice import text_to_structured_invoice, image_to_structured_invoice
from service.utils.parse_output import process_response
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
import tempfile, os

class TextInvoiceRequest(BaseModel):
    raw_text: str
    additional_info: Optional[str] = None

router = APIRouter()

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
        from service.utils.prompts import get_examples
        return get_examples()
    except Exception as e:
        return {"error": str(e)}