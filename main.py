from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Any
import base64
from docx import Document
from io import BytesIO

app = FastAPI()

class DocxFile(BaseModel):
    file: str

def read_docx(file: BytesIO) -> str:
    document = Document(file)
    doc_text = ""
    for para in document.paragraphs:
        doc_text += para.text + "\n"
    return doc_text

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/extract-text/")
async def extract_text(docx_file: DocxFile) -> Any:
    try:
        file_content = base64.b64decode(docx_file.file)
        file_stream = BytesIO(file_content)
        content = read_docx(file_stream)
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
