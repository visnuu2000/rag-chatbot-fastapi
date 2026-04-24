import os
import io
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from rag_engine import get_pdf_text, get_chunks, get_vectorstore, get_answer, debug_pdf

app = FastAPI()
templates = Jinja2Templates(directory="templates")

vectorstore_store = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request,"index.html")

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()
    pdf_file = io.BytesIO(content)

    pdf_file.seek(0)
    debug_info = debug_pdf(pdf_file)

    pdf_file.seek(0)
    raw_text = get_pdf_text(pdf_file)

    if len(raw_text) < 50:
        return JSONResponse(
            {"error": "Could not read text from this PDF. Try a different file."},
            status_code=400
        )

    chunks = get_chunks(raw_text)
    vectorstore_store["vs"] = get_vectorstore(chunks)

    return JSONResponse({
        "message": f"PDF loaded! {len(chunks)} chunks indexed. Ask me anything!",
        "debug": debug_info
    })

@app.post("/ask")
async def ask_question(request: Request):
    body = await request.json()
    question = body.get("question", "").strip()

    if not question:
        return JSONResponse({"error": "Empty question."}, status_code=400)

    if "vs" not in vectorstore_store:
        return JSONResponse({"error": "No PDF uploaded yet."}, status_code=400)

    answer = get_answer(vectorstore_store["vs"], question)
    return JSONResponse({"answer": answer})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)