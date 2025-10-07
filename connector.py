from fastapi import FastAPI, UploadFile, HTTPException
import httpx
import uvicorn
import os
import logging

app = FastAPI()

OCR_URL = os.getenv("OCR_URL", "http://paddleocr:8866")
LLM_API = os.getenv("LLM_API", "http://ollama:11434")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/parse-receipt")
async def parse_receipt(file: UploadFile):
    try:
        img_bytes = await file.read()
        async with httpx.AsyncClient() as client:
            ocr_resp = await client.post(f"{OCR_URL}/ocr", files={"image": ("file", img_bytes, file.content_type)})
            ocr_resp.raise_for_status()
            ocr_json = ocr_resp.json()
        
        prompt = f"""
You are a document parser. Given this OCR output with layout, extract:
- vendor
- date
- invoice number
- line items (description, qty, unit_price, total)
- total invoice sum
Return as JSON.
OCR_OUTPUT: {ocr_json}
"""
        async with httpx.AsyncClient() as client:
            llm_resp = await client.post(f"{LLM_API}/v1/chat/completions", json={"model": "mistral-7b-instruct", "messages": [{"role":"user","content":prompt}]})
            llm_resp.raise_for_status()
            return llm_resp.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=f"Service error: {e.response.text}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/summarize")
async def summarize(body: dict):
    try:
        text = body.get("text")
        if not text:
            raise HTTPException(status_code=400, detail="Missing 'text' in request body")
        
        prompt = f"Summarize the following document (and tag topics):\n\n{text}"
        async with httpx.AsyncClient() as client:
            llm_resp = await client.post(f"{LLM_API}/v1/chat/completions", json={"model":"mistral-7b-instruct","messages":[{"role":"user","content":prompt}]})
            llm_resp.raise_for_status()
            return llm_resp.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=f"Service error: {e.response.text}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
