from typing import Dict, Any, List
from fastapi import UploadFile
import re
import io
import os

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
try:
    import spacy
    _NLP = spacy.load("en_core_web_md")
    SPACY_AVAILABLE = True
except Exception:
    _NLP = None
    SPACY_AVAILABLE = False


DEGREE_KEYWORDS = [
    "bachelor", "master", "phd", "b.sc", "m.sc", "b.tech", "m.tech",
    "b.e.", "m.e.", "mba", "bachelors", "masters", "doctorate"
]

DATE_PATTERN = r"((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}|\d{4})"



def extract_text_from_pdf(content: bytes) -> str:
    """Extract text from PDF using PyMuPDF"""
    if not PYMUPDF_AVAILABLE:
        return "PDF parsing not available - PyMuPDF not installed"
    
    try:
        doc = fitz.open(stream=content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        return f"Error parsing PDF: {str(e)}"


def extract_name_by_font_from_pdf(content: bytes) -> str:
    """Use PyMuPDF text dict to get the largest-font text near the top, which is usually the name."""
    if not PYMUPDF_AVAILABLE:
        return ""
    try:
        doc = fitz.open(stream=content, filetype="pdf")
        best = (0.0, "")  # (size, text)
        pages_to_scan = min(2, doc.page_count)
        for i in range(pages_to_scan):
            p = doc.load_page(i)
            d = p.get_text("dict")
            for block in d.get("blocks", []):
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        txt = span.get("text", "").strip()
                        size = float(span.get("size", 0))
                        if txt and size > best[0] and 2 <= len(txt) <= 60:
                            best = (size, txt)
        doc.close()
        candidate = best[1]
        # If the largest text is multi-word and looks like a name, accept
        return candidate if _looks_like_name(candidate) else ""
    except Exception:
        return ""


def extract_text_from_docx(content: bytes) -> str:
    """Extract text from DOCX using python-docx"""
    if not DOCX_AVAILABLE:
        return "DOCX parsing not available - python-docx not installed"
    
    try:
        doc = Document(io.BytesIO(content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"Error parsing DOCX: {str(e)}"


def extract_email(text: str) -> str:
    """Extract email from text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group(0) if match else ""


def extract_phone(text: str) -> str:
    """Extract phone number from text"""
    phone_patterns = [
        r'\+?\d{1,3}[\s-]?\(?\d{2,4}\)?[\s-]?\d{3,4}[\s-]?\d{3,4}',  # International/India like +91 98908 12345
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US formats
        r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
    ]
    
    for pattern in phone_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return ""


BLACKLIST_TOKENS = {
    'resume', 'cv', 'curriculum', 'vitae', 'portfolio', 'streamlit', 'github', 'linkedin', 'email', 'phone'
}
TECH_TOKENS = {
    'python','java','javascript','typescript','react','node','aws','azure','gcp','sql','mysql','postgres',
    'mongodb','docker','kubernetes','tensorflow','pytorch','ml','ai','nlp','devops','engineer','developer',
    'data','science','datascientist','frontend','backend','fullstack','resume','cv'
}


def _looks_like_name(line: str) -> bool:
    parts = [p for p in re.split(r"\s+", line.strip()) if p]
    if not (2 <= len(parts) <= 5):
        return False
    if any(tok.lower() in BLACKLIST_TOKENS or tok.lower() in TECH_TOKENS for tok in parts):
        return False
    # Require at least one capitalized token
    caps = sum(1 for p in parts if re.match(r"^[A-Z][a-zA-Z\-\.]+$", p))
    return caps >= 1 and all(re.match(r"^[A-Za-z\-\.]+$", p) for p in parts)


def extract_name(text: str) -> str:
    """Extract name from text using header heuristics."""
    lines = [ln.strip() for ln in (text or '').split('\n') if ln.strip()]
    for line in lines[:15]:
        if _looks_like_name(line) and 2 <= len(line) <= 60:
            return line
    return ""


def guess_name_from_text(text: str) -> str:
    # Find adjacent capitalized tokens anywhere in first lines
    lines = [ln.strip() for ln in (text or '').split('\n') if ln.strip()]
    for line in lines[:30]:
        tokens = [t for t in re.split(r"\s+", line) if t]
        for i in range(len(tokens) - 1):
            pair = f"{tokens[i]} {tokens[i+1]}"
            if _looks_like_name(pair):
                return pair
    return ""


def _sanitize_name(raw: str) -> str:
    if not raw:
        return ""
    tokens = [t for t in re.split(r"\s+", raw) if t]
    clean = []
    for t in tokens:
        t2 = re.sub(r"[^A-Za-z\-]", "", t)
        if not t2:
            continue
        low = t2.lower()
        if low in BLACKLIST_TOKENS or low in TECH_TOKENS:
            continue
        clean.append(t2.capitalize())
    if len(clean) < 2:
        return ""
    return " ".join(clean[:4])


def extract_linkedin(text: str) -> str:
    """Extract LinkedIn profile, with or without protocol."""
    patterns = [
        r'https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9\-_/]+',
        r'(?<!\w)(?:www\.)?linkedin\.com/in/[A-Za-z0-9\-_/]+',
        r'(?<!\w)linkedin\.com/in/[A-Za-z0-9\-_/]+'
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            url = m.group(0)
            if not url.startswith('http'):
                url = 'https://' + url.lstrip()
            return url
    return ""


def extract_github(text: str) -> str:
    """Extract GitHub URL with or without protocol."""
    patterns = [
        r'https?://(?:www\.)?github\.com/[A-Za-z0-9\-_/]+',
        r'(?<!\w)(?:www\.)?github\.com/[A-Za-z0-9\-_/]+'
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            url = m.group(0)
            if not url.startswith('http'):
                url = 'https://' + url
            return url
    return ""


def extract_skills(text: str) -> List[str]:
    """Extract skills from text (basic keyword matching)"""
    common_skills = [
        'Python', 'JavaScript', 'Java', 'C++', 'C#', 'React', 'Node.js', 'Angular', 'Vue.js',
        'HTML', 'CSS', 'SQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'AWS', 'Azure', 'Docker',
        'Kubernetes', 'Git', 'Linux', 'Windows', 'Machine Learning', 'AI', 'Data Science',
        'Project Management', 'Agile', 'Scrum', 'Leadership', 'Communication', 'Teamwork'
    ]
    
    found_skills = []
    text_lower = text.lower()
    for skill in common_skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return found_skills


def extract_with_spacy(text: str) -> Dict[str, Any]:
    """Use spaCy NER to improve name/email/org/location extraction."""
    if not SPACY_AVAILABLE or not text or len(text) < 10:
        return {}
    doc = _NLP(text)
    name = ""
    email = extract_email(text)
    phone = extract_phone(text)
    location = ""
    organizations: List[str] = []
    persons: List[str] = []

    for ent in doc.ents:
        if ent.label_ in ("PERSON",) and not persons:
            persons.append(ent.text)
        elif ent.label_ in ("GPE", "LOC") and not location:
            location = ent.text
        elif ent.label_ == "ORG":
            organizations.append(ent.text)

    if persons:
        name = persons[0]

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "location": location,
        "organizations": list(dict.fromkeys(organizations))[:5],
    }


def extract_experience_sections(text: str) -> List[Dict[str, str]]:
    """Extract work experience sections from text"""
    # Look for common section headers
    experience_keywords = ['experience', 'employment', 'work history', 'professional experience']
    education_keywords = ['education', 'academic', 'qualifications', 'degrees']
    
    sections = []
    lines = text.split('\n')
    current_section = None
    
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        
        # Check if this line is a section header
        if any(keyword in line_lower for keyword in experience_keywords):
            if current_section:
                sections.append(current_section)
            current_section = {
                'type': 'experience',
                'title': line.strip(),
                'content': ''
            }
        elif any(keyword in line_lower for keyword in education_keywords):
            if current_section:
                sections.append(current_section)
            current_section = {
                'type': 'education',
                'title': line.strip(),
                'content': ''
            }
        elif current_section:
            current_section['content'] += line + '\n'
    
    if current_section:
        sections.append(current_section)
    
    return sections


async def parse_resume_upload(file: UploadFile) -> Dict[str, Any]:
    """Enhanced resume parser with better extraction capabilities"""
    content = await file.read()
    filename = file.filename or ""
    
    # Extract text based on file type
    if filename.lower().endswith('.pdf'):
        raw_text = extract_text_from_pdf(content)
    elif filename.lower().endswith(('.doc', '.docx')):
        raw_text = extract_text_from_docx(content)
    else:
        raw_text = f"Unsupported file type: {filename}"
    
    # Extract structured information
    ner = extract_with_spacy(raw_text)
    # Try font-based detection first for PDFs
    font_name = extract_name_by_font_from_pdf(content) if filename.lower().endswith('.pdf') else ""
    name = font_name or ner.get("name") or extract_name(raw_text)
    email = ner.get("email") or extract_email(raw_text)
    phone = ner.get("phone") or extract_phone(raw_text)
    location = ner.get("location", "")
    linkedin = extract_linkedin(raw_text)
    github = extract_github(raw_text)
    skills = extract_skills(raw_text)
    sections = extract_experience_sections(raw_text)
    
    # Try to extract summary (usually first paragraph after name)
    summary = ""
    lines = raw_text.split('\n')
    name_found = False
    for line in lines:
        line = line.strip()
        if name_found and line and len(line) > 20:
            summary = line
            break
        if name in line:
            name_found = True
    
    # Additional fallback for bad extractions like common tool names
    lower_name = (name or '').lower().strip()
    if not name or lower_name in BLACKLIST_TOKENS or len(name.split()) == 1:
        # Try from email local part
        if email and '@' in email:
            local = email.split('@', 1)[0]
            local = re.sub(r'[._-]+', ' ', local)
            local = _sanitize_name(local)
            if _looks_like_name(local):
                name = local
        # Try from text bigrams
        if not name:
            cand = guess_name_from_text(raw_text)
            cand = _sanitize_name(cand)
            if cand and _looks_like_name(cand):
                name = cand
        # Try from filename
        if not name and filename:
            base = re.sub(r'\.[A-Za-z0-9]+$', '', filename)
            base = re.sub(r'[._-]+', ' ', base)
            base = _sanitize_name(base)
            if base and _looks_like_name(base):
                name = base

    # Final sanitize
    name = _sanitize_name(name)

    # Convert sections to structured format
    work_experience = []
    education = []
    
    for section in sections:
        if section['type'] == 'experience':
            work_experience.append({
                'title': section['title'],
                'description': section['content'][:200] + '...' if len(section['content']) > 200 else section['content']
            })
        elif section['type'] == 'education':
            # Try to extract degree and year
            degree = next((w for w in DEGREE_KEYWORDS if w in section['content'].lower()), "")
            year_match = re.search(DATE_PATTERN, section['content'], flags=re.IGNORECASE)
            education.append({
                'title': degree.title() or section['title'],
                'description': section['content'][:200] + '...' if len(section['content']) > 200 else section['content'],
                'year': year_match.group(0) if year_match else "",
            })
    
    return {
        "parsed": {
            "personalInfo": {
                "name": name,
                "email": email,
                "phone": phone,
                "location": location,
                "linkedin": linkedin,
                "github": github,
                "website": "",
            },
            "summary": summary,
            "education": education,
            "workExperience": work_experience,
            "projects": [],
            "skills": [{"name": skill, "category": "technical", "proficiency": "intermediate"} for skill in skills],
            "certifications": [],
        },
        "rawText": raw_text,
        "confidence": 0.7 if name and email else 0.3,
    }



def parse_resume_from_path(file_path: str) -> Dict[str, Any]:
    """Synchronous helper to parse a local file path on the server.
    Mirrors parse_resume_upload but reads bytes from disk."""
    if not os.path.isfile(file_path):
        return {"error": f"file not found: {file_path}"}
    try:
        with open(file_path, "rb") as f:
            content = f.read()
    except Exception as e:
        return {"error": f"failed to read file: {e}"}

    lower = file_path.lower()
    if lower.endswith('.pdf'):
        raw_text = extract_text_from_pdf(content)
        font_name = extract_name_by_font_from_pdf(content)
    elif lower.endswith(('.doc', '.docx')):
        raw_text = extract_text_from_docx(content)
        font_name = ""
    else:
        return {"error": f"unsupported file type: {file_path}"}

    ner = extract_with_spacy(raw_text)
    name = font_name or ner.get("name") or extract_name(raw_text)
    email = ner.get("email") or extract_email(raw_text)
    phone = ner.get("phone") or extract_phone(raw_text)
    location = ner.get("location", "")
    if not location:
        # simple fallback for common city,country patterns found in resumes
        city_candidates = re.findall(r"\b([A-Z][a-zA-Z]+,\s*[A-Z][a-zA-Z]+)\b", raw_text)
        if city_candidates:
            location = city_candidates[0]
    linkedin = extract_linkedin(raw_text)
    github = extract_github(raw_text)
    skills = extract_skills(raw_text)
    sections = extract_experience_sections(raw_text)

    # summary heuristic
    summary = ""
    lines_iter = [ln.strip() for ln in raw_text.split('\n') if ln.strip()]
    # pick first non-contact, non-link line after header block
    for ln in lines_iter[:80]:
        if re.search(r"@|linkedin|github|phone|\+\d|mailto|http", ln, flags=re.I):
            continue
        if len(ln) > 20:
            summary = ln
            break

    # sanitize name fallbacks
    lower_name = (name or '').lower().strip()
    if not name or lower_name in BLACKLIST_TOKENS or len(name.split()) == 1:
        if email and '@' in email:
            local = email.split('@', 1)[0]
            local = re.sub(r'[._-]+', ' ', local)
            local = _sanitize_name(local)
            if _looks_like_name(local):
                name = local
        if not name:
            cand = _sanitize_name(guess_name_from_text(raw_text))
            if cand and _looks_like_name(cand):
                name = cand
        if not name:
            base = re.sub(r'\.[A-Za-z0-9]+$', '', os.path.basename(file_path))
            base = _sanitize_name(re.sub(r'[._-]+', ' ', base))
            if base and _looks_like_name(base):
                name = base

    name = _sanitize_name(name)

    work_experience: List[Dict[str,str]] = []
    education: List[Dict[str,str]] = []
    for section in sections:
        if section['type'] == 'experience':
            work_experience.append({
                'title': section['title'],
                'description': section['content'][:200] + '...' if len(section['content']) > 200 else section['content']
            })
        elif section['type'] == 'education':
            degree = next((w for w in DEGREE_KEYWORDS if w in section['content'].lower()), "")
            year_match = re.search(DATE_PATTERN, section['content'], flags=re.IGNORECASE)
            education.append({
                'title': degree.title() or section['title'],
                'description': section['content'][:200] + '...' if len(section['content']) > 200 else section['content'],
                'year': year_match.group(0) if year_match else "",
            })

    return {
        "parsed": {
            "personalInfo": {
                "name": name,
                "email": email,
                "phone": phone,
                "location": location,
                "linkedin": linkedin,
                "github": github,
                "website": "",
            },
            "summary": summary,
            "education": education,
            "workExperience": work_experience,
            "projects": [],
            "skills": [{"name": s, "category": "technical", "proficiency": "intermediate"} for s in skills],
            "certifications": [],
        },
        "rawText": raw_text,
        "confidence": 0.7 if name and email else 0.3,
    }

