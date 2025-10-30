# OptiResume — AI-Driven Resume Optimization and Career Enhancement

A full‑stack system to parse resumes, enhance content, and generate polished, ATS‑friendly CVs with selectable templates.

## Demo Capabilities
- BuildCV: Upload PDF/DOCX or Manual Entry, live preview, download PDF (HTML/KaTeX) or LaTeX PDF (when TeX is installed)
- Accurate parsing (PyMuPDF, python‑docx, spaCy + heuristics)
- Rule‑based AI Enhancement: rewrites bullets, synthesizes concise summary, dedupes skills
- Templates: Basic, Modern, Classic Professional, Minimal Clean, Modern Executive, Executive Maroon
- Optional MCP servers: Python stdio and Node proxy (tools usable from Claude Desktop)

## Quickstart
1) Backend
```
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```
2) Frontend
```
cd ai-skill-analyzer-main
npm install
npm run dev
```
3) Node MCP (optional)
```
cd mcp-server
npm install
set FASTAPI_BASE_URL=http://127.0.0.1:8000
npm start
```

## API
- GET `/templates`
- POST `/upload_resume` (multipart file)
- POST `/upload_resume_path` { file_path }
- POST `/generate_resume` { template, data, format: 'html'|'pdf' }

## Notable Paths
- Frontend entry: `ai-skill-analyzer-main/src/pages/BuildCVPage.tsx`
- Backend: `backend/main.py`, `backend/parser.py`, `backend/render.py`
- Templates: `templates/*.tex`
- Node MCP server: `mcp-server/index.js`

## MCP Tools (Node)
- list_templates → lists LaTeX templates
- extract_resume_data → uploads a local file path to FastAPI for parsing
- generate_resume_html → returns HTML preview
- generate_resume → returns HTML or base64 PDF

## Troubleshooting
- LaTeX not available → use HTML/KaTeX print; or install/update MiKTeX and ensure pdflatex/xelatex is on PATH
- 422 on `/upload_resume_path` → ensure JSON body `{ "file_path": "C:\\path\\resume.pdf" }`
- CORS/URL → set `VITE_BACKEND_URL` or ensure backend at `http://localhost:8000`

## Credits
-billryan/resume
-Renovamen/oh-my-cv
-KaTeX/KaTeX

## License
MIT

## Author
GitHub: https://github.com/AaryanGole26
