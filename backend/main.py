import uvicorn
import os
from fastapi import FastAPI, UploadFile, Form, Body
from core import parse_resume, extract_job_skills, analyze_skill_match, generate_llm_recommendations, format_for_ui_and_pdf, export_to_pdf, get_description_from_db, calculate_ats_score
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os as _os

from schemas import GenerateResumeRequest
from parser import parse_resume_upload, parse_resume_from_path
from render import render_html_from_data, render_pdf_from_template, render_pdf_placeholder

app = FastAPI()
temp_storage = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080", 
        "http://localhost:5173",
        "https://optiresume-aidrivenresumeoptimizationandcare-production.up.railway.app",
        "*"  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "OptiResume API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.options("/analyze-resume")
async def analyze_resume_options():
    return {"message": "OK"}

@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile, job_role: str = Form(...), job_description: str = Form(None)):
    resume_data = parse_resume(file)
    if not job_description:
        job_description = get_description_from_db(job_role)
    required_skills = extract_job_skills(job_description)
    match_info = analyze_skill_match(resume_data, required_skills)
    
    # Calculate ATS score (independent of skill matching)
    ats_data = calculate_ats_score(resume_data, job_description)
    
    recommendations = generate_llm_recommendations(resume_data, job_description, match_info)
    formatted = format_for_ui_and_pdf(match_info, recommendations, ats_data)
    
    temp_storage["last_result"] = formatted 

    return {
        "result": formatted
    }

@app.options("/export-pdf")
async def export_pdf_options():
    return {"message": "OK"}

@app.get("/export-pdf")
async def export_pdf():
    formatted_data = temp_storage.get("last_result")
    if not formatted_data:
        return {"error": "No analysis result available to export."}

    pdf_path = export_to_pdf(formatted_data)
    return FileResponse(
        path=pdf_path,
        filename="ResumeReport(OptiResume).pdf",
        media_type="application/pdf"
    )

# ---------------- BuildCV endpoints ----------------

@app.get("/templates")
async def list_templates():
    # Look for LaTeX templates in backend/templates and root templates/
    candidates: List[str] = []
    root_templates = _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), "templates")
    backend_templates = _os.path.join(_os.path.dirname(__file__), "templates")
    for d in [backend_templates, root_templates]:
        if _os.path.isdir(d):
            for f in _os.listdir(d):
                if f.endswith(".tex"):
                    candidates.append(f)
    # De-duplicate while preserving order
    seen = set()
    unique = [x for x in candidates if not (x in seen or seen.add(x))]
    return {"templates": unique or ["modern.tex", "classic.tex", "professional.tex"]}


@app.post("/upload_resume")
async def upload_resume(file: UploadFile):
    parsed = await parse_resume_upload(file)
    return JSONResponse(parsed)


@app.post("/upload_resume_path")
async def upload_resume_path(payload: dict = Body(...)):
    """DEV convenience: parse a resume from a local file path on the server machine.
    Expects JSON body: { "file_path": "C:\\path\\to\\resume.pdf" }
    """
    file_path = (payload or {}).get("file_path", "")
    data = parse_resume_from_path(file_path)
    return JSONResponse(data)


@app.post("/generate_resume")
async def generate_resume(req: GenerateResumeRequest):
    fmt = (req.format or "html").lower()
    if fmt == "html":
        return render_html_from_data(req.data.dict(), req.template)
    if fmt == "pdf":
        # Use LaTeX template for PDF generation
        return render_pdf_from_template(req.template, req.data.dict())
    return JSONResponse({"error": "Unsupported format"}, status_code=400)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)