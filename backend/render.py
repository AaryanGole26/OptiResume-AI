from typing import Dict, List
from io import BytesIO
import os
import subprocess
import tempfile
from fastapi.responses import HTMLResponse, StreamingResponse


def format_work_experience(work_experience: List[Dict]) -> str:
    """Format work experience for LaTeX"""
    if not work_experience:
        return ""
    
    latex = "\\section{Work Experience}\n"
    for exp in work_experience:
        title = exp.get('title', 'Position')
        description = exp.get('description', '')
        latex += f"\\textbf{{{title}}}\\\\\n"
        latex += f"{description}\n\n"
    return latex


def format_education(education: List[Dict]) -> str:
    """Format education for LaTeX"""
    if not education:
        return ""
    
    latex = "\\section{Education}\n"
    for edu in education:
        title = edu.get('title', 'Degree')
        description = edu.get('description', '')
        latex += f"\\textbf{{{title}}}\\\\\n"
        latex += f"{description}\n\n"
    return latex


def format_skills(skills: List[Dict]) -> str:
    """Format skills for LaTeX"""
    if not skills:
        return ""
    
    skill_names = [skill.get('name', '') for skill in skills if skill.get('name')]
    if not skill_names:
        return ""
    
    latex = "\\section{Skills}\n"
    latex += ", ".join(skill_names)
    return latex


def format_projects(projects: List[Dict]) -> str:
    """Format projects for LaTeX"""
    if not projects:
        return ""
    
    latex = "\\section{Projects}\n"
    for project in projects:
        name = project.get('name', 'Project')
        description = project.get('description', '')
        latex += f"\\textbf{{{name}}}\\\\\n"
        latex += f"{description}\n\n"
    return latex


def format_certifications(certifications: List[Dict]) -> str:
    """Format certifications for LaTeX"""
    if not certifications:
        return ""
    
    latex = "\\section{Certifications}\n"
    for cert in certifications:
        name = cert.get('name', 'Certification')
        issuer = cert.get('issuer', '')
        date = cert.get('date', '')
        latex += f"\\textbf{{{name}}}"
        if issuer:
            latex += f" - {issuer}"
        if date:
            latex += f" ({date})"
        latex += "\\\\\n"
    return latex


def format_linkedin_url(linkedin: str) -> str:
    """Format LinkedIn URL for LaTeX"""
    if not linkedin:
        return ""
    if linkedin.startswith('http'):
        return f"\\href{{{linkedin}}}{{LinkedIn}}"
    return f"\\href{{https://linkedin.com/in/{linkedin}}}{{LinkedIn}}"


def format_github_url(github: str) -> str:
    """Format GitHub URL for LaTeX"""
    if not github:
        return ""
    if github.startswith('http'):
        return f"\\href{{{github}}}{{GitHub}}"
    return f"\\href{{https://github.com/{github}}}{{GitHub}}"


def format_website_url(website: str) -> str:
    """Format website URL for LaTeX"""
    if not website:
        return ""
    if not website.startswith('http'):
        website = f"https://{website}"
    return f"\\href{{{website}}}{{Website}}"


def substitute_template_variables(template_content: str, data: Dict) -> str:
    """Substitute variables in LaTeX template"""
    p = data.get("personalInfo", {})
    
    # Format URLs
    linkedin_url = format_linkedin_url(p.get("linkedin", ""))
    github_url = format_github_url(p.get("github", ""))
    website_url = format_website_url(p.get("website", ""))
    
    # Basic substitutions
    substitutions = {
        '$name$': p.get("name", "Your Name"),
        '$email$': p.get("email", "your.email@example.com"),
        '$phone$': p.get("phone", "(123) 456-7890"),
        '$location$': p.get("location", "City, State"),
        '$linkedin$': linkedin_url,
        '$github$': github_url,
        '$website$': website_url,
        '$summary$': data.get("summary", "Professional summary goes here."),
    }
    
    # Format individual sections
    work_exp = format_work_experience(data.get("workExperience", []))
    education = format_education(data.get("education", []))
    skills = format_skills(data.get("skills", []))
    projects = format_projects(data.get("projects", []))
    certifications = format_certifications(data.get("certifications", []))
    
    # Add section substitutions
    substitutions.update({
        '$work_experience$': work_exp,
        '$education$': education,
        '$skills$': skills,
        '$projects$': projects,
        '$certifications$': certifications,
    })
    
    # Apply substitutions
    result = template_content
    for placeholder, value in substitutions.items():
        result = result.replace(placeholder, value)
    
    return result


def _html_escape(text: str) -> str:
    return (text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _html_sections_from_data(data: Dict) -> Dict[str, str]:
    work = []
    for exp in data.get("workExperience", []) or []:
        title = _html_escape(exp.get("title") or exp.get("company") or "Experience")
        desc = _html_escape(exp.get("description", ""))
        work.append(f"<div class=\"item\"><div class=\"ititle\"><strong>{title}</strong></div><div class=\"ibody\">{desc}</div></div>")
    education = []
    for edu in data.get("education", []) or []:
        title = _html_escape(edu.get("title") or edu.get("degree") or "Education")
        desc = _html_escape(edu.get("description", ""))
        education.append(f"<div class=\"item\"><div class=\"ititle\"><strong>{title}</strong></div><div class=\"ibody\">{desc}</div></div>")
    skills = []
    for sk in data.get("skills", []) or []:
        name = _html_escape(sk.get("name") if isinstance(sk, dict) else str(sk))
        if name:
            skills.append(f"<span class=\"skill\">{name}</span>")
    projects = []
    for pr in data.get("projects", []) or []:
        name = _html_escape(pr.get("name", "Project"))
        desc = _html_escape(pr.get("description", ""))
        projects.append(f"<div class=\"item\"><div class=\"ititle\"><strong>{name}</strong></div><div class=\"ibody\">{desc}</div></div>")
    certs = []
    for c in data.get("certifications", []) or []:
        nm = _html_escape(c.get("name", "Certification"))
        issuer = _html_escape(c.get("issuer", ""))
        certs.append(f"<div class=\"item\"><div class=\"ititle\"><strong>{nm}</strong></div><div class=\"ibody\">{issuer}</div></div>")
    return {
        "work": "\n".join(work),
        "education": "\n".join(education),
        "skills": "\n".join(skills),
        "projects": "\n".join(projects),
        "certs": "\n".join(certs),
    }


def render_html_from_data(data: Dict, template: str | None = None) -> HTMLResponse:
    """Render HTML preview with themes approximating the LaTeX templates."""
    p = data.get("personalInfo", {})
    name = _html_escape(p.get("name", "Your Name"))
    email = _html_escape(p.get("email", "your.email@example.com"))
    phone = _html_escape(p.get("phone", "(123) 456-7890"))
    location = _html_escape(p.get("location", "City, State"))
    ln_raw = (p.get("linkedin", "") or "").strip()
    gh_raw = (p.get("github", "") or "").strip()
    ws_raw = (p.get("website", "") or "").strip()
    def _ensure_http(u: str) -> str:
        if not u:
            return ""
        if not u.startswith("http"):
            return ("https://" + u).replace("https://https://", "https://")
        return u
    ln = _html_escape(_ensure_http(ln_raw if ln_raw else ""))
    if ln and "linkedin.com" not in ln:
        # allow plain handle like aaryan-gole
        ln = f"https://linkedin.com/in/{_html_escape(ln_raw)}"
    gh = _html_escape(_ensure_http(gh_raw if gh_raw else ""))
    if gh and "github.com" not in gh:
        gh = f"https://github.com/{_html_escape(gh_raw)}"
    ws = _html_escape(_ensure_http(ws_raw))
    ln_html = f'<a href="{ln}" target="_blank" rel="noopener">{ln}</a>' if ln else ""
    gh_html = f'<a href="{gh}" target="_blank" rel="noopener">{gh}</a>' if gh else ""
    ws_html = f'<a href="{ws}" target="_blank" rel="noopener">{ws}</a>' if ws else ""
    summary = _html_escape(data.get("summary", "Professional summary goes here."))

    tname = (template or "billryan_basic").lower()
    sections = _html_sections_from_data(data)

    # Strongly differentiated Modern Executive: two-column with left sidebar
    if "modern_executive" in tname:
        primary = "#1f2937"  # slate-800
        accent = "#4f46e5"   # indigo-600
        html = f"""
<!doctype html>
<html>
  <head>
    <meta charset='utf-8'/>
    <title>Resume - {name}</title>
    <style>
      :root {{ --primary: {primary}; --accent: {accent}; }}
      * {{ box-sizing: border-box; }}
      body {{ margin: 0; font-family: 'Inter','Segoe UI',Tahoma,sans-serif; color: #111827; }}
      .container {{ display: grid; grid-template-columns: 280px 1fr; min-height: 100vh; }}
      .sidebar {{ background: #111827; color: #e5e7eb; padding: 28px 24px; }}
      .avatar {{ width: 88px; height: 88px; border-radius: 50%; background: linear-gradient(135deg, var(--accent), #9333ea); margin-bottom: 16px; }}
      .name {{ color:#fff; font-weight: 800; font-size: 22px; line-height: 1.2; }}
      .role {{ color:#c7d2fe; font-size: 13px; margin-top: 4px; }}
      .side-block {{ margin-top: 22px; }}
      .sb-title {{ font-size: 12px; letter-spacing: .12em; text-transform: uppercase; color:#9ca3af; margin-bottom: 8px; }}
      .contact li {{ list-style: none; margin: 6px 0; font-size: 13px; color:#e5e7eb; }}
      .chip {{ display:inline-block; margin: 4px 6px 0 0; padding: 4px 10px; border-radius: 999px; font-size: 12px; background: #1f2937; border: 1px solid #374151; color:#e5e7eb; }}
      .content {{ padding: 36px 40px; }}
      .hdr {{ border-bottom: 4px solid var(--accent); padding-bottom: 8px; margin-bottom: 16px; }}
      .hdr h1 {{ margin:0; font-size: 34px; font-weight: 900; color: var(--primary); }}
      .hdr .meta {{ color:#4b5563; margin-top: 6px; }}
      h2 {{ margin: 20px 0 8px; font-size: 14px; letter-spacing:.14em; text-transform: uppercase; color: var(--primary); }}
      .item {{ margin:10px 0; }}
      .summary {{ background: #f8fafc; border:1px solid #e5e7eb; padding:14px 16px; border-radius: 8px; }}
      .section-divider {{ height: 1px; background: #e5e7eb; margin: 8px 0 4px; }}
      @media print {{
        .container {{ grid-template-columns: 240px 1fr; }}
        .content {{ padding: 24px 28px; }}
      }}
    </style>
  </head>
  <body>
    <div class='container'>
      <aside class='sidebar'>
        <div class='avatar'></div>
        <div class='name'>{name}</div>
        <div class='role'></div>
        <div class='side-block'>
          <div class='sb-title'>Contact</div>
          <ul class='contact'>
            <li>{email}</li>
            <li>{phone}</li>
            <li>{location}</li>
            {f"<li>{ln_html}</li>" if ln_html else ''}
            {f"<li>{gh_html}</li>" if gh_html else ''}
            {f"<li>{ws_html}</li>" if ws_html else ''}
          </ul>
        </div>
        {f"<div class='side-block'><div class='sb-title'>Skills</div><div>{sections['skills']}</div></div>" if sections['skills'] else ''}
        {f"<div class='side-block'><div class='sb-title'>Certifications</div><div>{sections['certs']}</div></div>" if sections['certs'] else ''}
      </aside>
      <main class='content'>
        <div class='hdr'>
          <h1>{name}</h1>
          <div class='meta'>{email} · {phone} · {location}{' · ' + ln_html if ln_html else ''}{' · ' + gh_html if gh_html else ''}{' · ' + ws_html if ws_html else ''}</div>
        </div>
        <section>
          <h2>Professional Summary</h2>
          <div class='summary'>{summary}</div>
        </section>
        <div class='section-divider'></div>
        {f"<section><h2>Work Experience</h2><div>{sections['work']}</div></section>" if sections['work'] else ''}
        {f"<section><h2>Projects</h2><div>{sections['projects']}</div></section>" if sections['projects'] else ''}
        {f"<section><h2>Education</h2><div>{sections['education']}</div></section>" if sections['education'] else ''}
      </main>
    </div>
  </body>
</html>
"""
        return HTMLResponse(content=html)

    if "billryan_modern" in tname:
        primary = "#2c3e50"
        html = f"""
<!doctype html>
<html>
  <head>
    <meta charset='utf-8'/>
    <title>Resume - {name}</title>
    <style>
      body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px auto; max-width: 820px; color:#333; line-height:1.6; }}
      .head {{ text-align:center; margin-bottom:24px; padding-bottom:16px; border-bottom:2px solid {primary}; }}
      .head h1 {{ margin:0; font-size:40px; font-weight:700; color:{primary}; }}
      .contact {{ color:#555; margin-top:6px; }}
      h2 {{ color:{primary}; margin:28px 0 10px; padding-bottom:6px; border-bottom:1px solid #d0d7de; font-size:16px; letter-spacing:.06em; text-transform:uppercase; }}
      .summary {{ background:#f5f7fb; border:1px solid #e1e6f0; padding:14px 16px; border-radius:10px; }}
      .skills {{ display:flex; flex-wrap:wrap; gap:8px; }}
      .skill {{ background:#ecf0f1; padding:4px 10px; border-radius:14px; font-size:12px; }}
      .item {{ margin:10px 0; }}
      .ititle {{ margin-bottom:4px; }}
    </style>
  </head>
  <body>
    <div class='head'>
      <h1>{name}</h1>
      <div class='contact'>{email} · {phone} · {location}{' · ' + ln_html if ln_html else ''}{' · ' + gh_html if gh_html else ''}{' · ' + ws_html if ws_html else ''}</div>
    </div>
    <h2>Professional Summary</h2>
    <div class='summary'>{summary}</div>
    {f"<h2>Work Experience</h2><div>{sections['work']}</div>" if sections['work'] else ''}
    {f"<h2>Education</h2><div>{sections['education']}</div>" if sections['education'] else ''}
    {f"<h2>Skills</h2><div class='skills'>{sections['skills']}</div>" if sections['skills'] else ''}
    {f"<h2>Projects</h2><div>{sections['projects']}</div>" if sections['projects'] else ''}
    {f"<h2>Certifications</h2><div>{sections['certs']}</div>" if sections['certs'] else ''}
  </body>
</html>
"""
        return HTMLResponse(content=html)

    if "classic_professional" in tname:
        primary = "#0f172a"
        html = f"""
<!doctype html>
<html>
  <head>
    <meta charset='utf-8'/>
    <title>Resume - {name}</title>
    <style>
      body {{ font-family: Georgia, 'Times New Roman', serif; margin: 36px auto; max-width: 820px; color:#222; line-height:1.7; }}
      .head {{ text-align:center; margin-bottom:18px; }}
      .head h1 {{ margin:0 0 4px; font-size:38px; font-weight:700; color:{primary}; }}
      .muted {{ color:#444; }}
      hr {{ border:0; height:1px; background:#cbd5e1; margin:16px 0 10px; }}
      h2 {{ margin:16px 0 8px; font-size:16px; letter-spacing:.04em; text-transform:uppercase; color:{primary}; }}
      .item {{ margin:8px 0; }}
    </style>
  </head>
  <body>
    <div class='head'>
      <h1>{name}</h1>
      <div class='muted'>{email} · {phone} · {location}{' · ' + ln_html if ln_html else ''}{' · ' + gh_html if gh_html else ''}{' · ' + ws_html if ws_html else ''}</div>
      <hr />
    </div>
    <h2>Professional Summary</h2>
    <div>{summary}</div>
    {f"<h2>Work Experience</h2><div>{sections['work']}</div>" if sections['work'] else ''}
    {f"<h2>Education</h2><div>{sections['education']}</div>" if sections['education'] else ''}
    {f"<h2>Skills</h2><div>{sections['skills']}</div>" if sections['skills'] else ''}
    {f"<h2>Projects</h2><div>{sections['projects']}</div>" if sections['projects'] else ''}
    {f"<h2>Certifications</h2><div>{sections['certs']}</div>" if sections['certs'] else ''}
  </body>
</html>
"""
        return HTMLResponse(content=html)

    if "minimal_clean" in tname:
        html = f"""
<!doctype html>
<html>
  <head>
    <meta charset='utf-8'/>
    <title>Resume - {name}</title>
    <style>
      body {{ font-family: 'Inter', 'Segoe UI', Tahoma, sans-serif; margin: 48px auto; max-width: 820px; color:#1f2937; line-height:1.8; }}
      .head h1 {{ margin:0 0 6px; font-size:34px; font-weight:700; }}
      .muted {{ color:#6b7280; }}
      section {{ margin:22px 0; }}
      section h2 {{ margin:0 0 8px; font-size:15px; letter-spacing:.08em; text-transform:uppercase; color:#111827; }}
      .item {{ margin:6px 0; }}
      .skills .skill {{ display:inline-block; margin:2px 6px 2px 0; padding:2px 8px; border:1px solid #e5e7eb; border-radius:12px; font-size:12px; }}
    </style>
  </head>
  <body>
    <div class='head'>
      <h1>{name}</h1>
      <div class='muted'>{email} · {phone} · {location}{' · ' + ln_html if ln_html else ''}{' · ' + gh_html if gh_html else ''}{' · ' + ws_html if ws_html else ''}</div>
    </div>
    <section>
      <h2>Professional Summary</h2>
      <div>{summary}</div>
    </section>
    {f"<section><h2>Work Experience</h2><div>{sections['work']}</div></section>" if sections['work'] else ''}
    {f"<section><h2>Education</h2><div>{sections['education']}</div></section>" if sections['education'] else ''}
    {f"<section class='skills'><h2>Skills</h2><div>{sections['skills']}</div></section>" if sections['skills'] else ''}
    {f"<section><h2>Projects</h2><div>{sections['projects']}</div></section>" if sections['projects'] else ''}
    {f"<section><h2>Certifications</h2><div>{sections['certs']}</div></section>" if sections['certs'] else ''}
  </body>
</html>
"""
        return HTMLResponse(content=html)

    # Template 1 – two-column maroon theme matching provided PDF
    if "template1" in tname:
        primary = "#7a1d12"  # deep maroon
        dark = "#111111"
        light = "#f8f5f2"
        dot = "#b45309"  # amber-brown dots
        html = f"""
<!doctype html>
<html>
  <head>
    <meta charset='utf-8'/>
    <title>Resume - {name}</title>
    <style>
      * {{ box-sizing: border-box; }}
      body {{ margin:0; font-family: Georgia, 'Times New Roman', serif; color:#1f2937; background:{light}; }}
      .header {{ background:{dark}; color:#fff; padding:16px 28px; border-bottom:6px solid {primary}; }}
      .name {{ font-weight:900; font-size:36px; letter-spacing:.02em; }}
      .subtitle {{ margin-top:4px; font-size:14px; opacity:.9; }}
      .contacts {{ margin-top:8px; font-size:12px; opacity:.95; display:flex; flex-wrap:wrap; gap:10px; align-items:center; }}
      .dot::before {{ content:''; display:inline-block; width:6px; height:6px; background:{primary}; border-radius:50%; margin:0 8px; vertical-align:middle; }}
      .wrap {{ max-width:1000px; margin:0 auto; background:#fff; padding:18px 24px 28px; }}
      .grid {{ display:grid; grid-template-columns: 1fr 0.9fr; gap:22px; }}
      h2 {{ margin:16px 0 8px; font-size:16px; letter-spacing:.12em; text-transform:uppercase; color:{primary}; border-bottom:2px solid {primary}; padding-bottom:4px; }}
      .section {{ margin-top:8px; }}
      .item {{ padding:10px 0; border-bottom:1px dotted #cbd5e1; }}
      .item:last-child {{ border-bottom:0; }}
      .role {{ font-weight:700; }}
      .muted {{ color:#6b7280; font-size:12px; }}
      ul.bullets {{ margin:6px 0 0 18px; padding:0; }}
      ul.bullets li {{ margin:2px 0; }}
      .tags {{ display:flex; flex-wrap:wrap; gap:6px; margin-top:6px; }}
      .tag {{ font-size:11px; border:1px solid #d1d5db; padding:2px 8px; border-radius:12px; background:#fafafa; }}
      .lang .dots {{ display:inline-block; margin-left:8px; }}
      .lang .dot {{ display:inline-block; width:8px; height:8px; border-radius:50%; background:#e5e7eb; margin-left:4px; }}
      .lang .dot.fill {{ background:{primary}; }}
      @media print {{ .wrap {{ padding:10px 16px 18px; }} .grid {{ grid-template-columns: 1fr .9fr; gap:18px; }} }}
    </style>
  </head>
  <body>
    <div class='header'>
      <div class='name'>{name}</div>
      <div class='subtitle'></div>
      <div class='contacts'>
        <span>{email}</span><span class='dot'></span>
        <span>{phone}</span><span class='dot'></span>
        <span>{location}</span>
        {f"<span class='dot'></span><span>{ln_html}</span>" if ln_html else ''}
        {f"<span class='dot'></span><span>{gh_html}</span>" if gh_html else ''}
        {f"<span class='dot'></span><span>{ws_html}</span>" if ws_html else ''}
      </div>
    </div>
    <div class='wrap'>
      <div class='grid'>
        <div>
          <h2>Experience</h2>
          <div class='section'>
            {sections['work'] or ''}
          </div>
          <h2>Projects</h2>
          <div class='section'>
            {sections['projects'] or ''}
          </div>
        </div>
        <div>
          <h2>Strengths</h2>
          <div class='section tags'>
            {sections['skills'] or ''}
          </div>
          <h2>Languages</h2>
          <div class='section'>
            <!-- placeholder mapping from skills named like English(4) → 4 dots -->
          </div>
          <h2>Education</h2>
          <div class='section'>
            {sections['education'] or ''}
          </div>
        </div>
      </div>
    </div>
  </body>
</html>
"""
        return HTMLResponse(content=html)

    # Default: billryan_basic-like
    html = f"""
<!doctype html>
<html>
  <head>
    <meta charset='utf-8'/>
    <title>Resume - {name}</title>
    <style>
      body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px auto; max-width: 820px; color:#333; line-height:1.6; }}
      .head {{ text-align:center; }}
      .head h1 {{ margin:0 0 6px; font-size:36px; font-weight:600; color:#223; }}
      .muted {{ color:#666; }}
      .rule {{ border-top:2px solid #2c3e50; margin:22px 0; }}
      h2 {{ margin:18px 0 10px; font-size:16px; letter-spacing:.06em; text-transform:uppercase; color:#2c3e50; }}
      .skills {{ display:flex; flex-wrap:wrap; gap:8px; }}
      .skill {{ background:#eef2f7; padding:4px 10px; border-radius:14px; font-size:12px; }}
      .item {{ margin:10px 0; }}
      .ititle {{ margin-bottom:4px; }}
    </style>
  </head>
  <body>
    <div class='head'>
      <h1>{name}</h1>
      <div class='muted'>{email} · {phone} · {location}{' · ' + ln_html if ln_html else ''}{' · ' + gh_html if gh_html else ''}{' · ' + ws_html if ws_html else ''}</div>
      <div class='rule'></div>
    </div>
    <h2>Professional Summary</h2>
    <div>{summary}</div>
    {f"<h2>Work Experience</h2><div>{sections['work']}</div>" if sections['work'] else ''}
    {f"<h2>Education</h2><div>{sections['education']}</div>" if sections['education'] else ''}
    {f"<h2>Skills</h2><div class='skills'>{sections['skills']}</div>" if sections['skills'] else ''}
    {f"<h2>Projects</h2><div>{sections['projects']}</div>" if sections['projects'] else ''}
    {f"<h2>Certifications</h2><div>{sections['certs']}</div>" if sections['certs'] else ''}
  </body>
</html>
"""
    return HTMLResponse(content=html)


def _find_pdflatex_executable() -> str | None:
    candidates = [
        'pdflatex',
        os.path.expandvars(r"%ProgramFiles%\MiKTeX\miktex\bin\x64\pdflatex.exe"),
        os.path.expandvars(r"%LocalAppData%\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe"),
        os.path.expandvars(r"%ProgramFiles%\MiKTeX 2.9\miktex\bin\x64\pdflatex.exe"),
    ]
    for c in candidates:
        if c and os.path.isfile(c):
            return c
    return None


def render_pdf_from_template(template_name: str, data: Dict) -> StreamingResponse:
    """Render PDF using LaTeX template"""
    try:
        # Find template file
        template_paths = [
            os.path.join(os.path.dirname(__file__), "templates", template_name),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", template_name)
        ]
        
        template_path = None
        for path in template_paths:
            if os.path.exists(path):
                template_path = path
                break
        
        if not template_path:
            # Fallback to placeholder
            return render_pdf_placeholder()
        
        # Read template
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Substitute variables
        latex_content = substitute_template_variables(template_content, data)
        
        # Create temporary files
        with tempfile.TemporaryDirectory() as temp_dir:
            tex_file = os.path.join(temp_dir, "resume.tex")
            pdf_file = os.path.join(temp_dir, "resume.pdf")
            
            # Write LaTeX content
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            # Compile LaTeX to PDF
            try:
                pdflatex = _find_pdflatex_executable() or 'pdflatex'
                args = [
                    pdflatex,
                    '-interaction=nonstopmode',
                    '-halt-on-error',
                    '-output-directory', temp_dir,
                    tex_file,
                ]
                # First pass
                result1 = subprocess.run(args, capture_output=True, text=True, timeout=120)
                # Second pass (often needed for TOC/refs, and also to trigger package auto-install once more)
                result2 = subprocess.run(args, capture_output=True, text=True, timeout=120)

                if os.path.exists(pdf_file) and (result2.returncode == 0 or result1.returncode == 0):
                    with open(pdf_file, 'rb') as f:
                        pdf_content = f.read()
                    return StreamingResponse(
                        BytesIO(pdf_content),
                        media_type="application/pdf",
                        headers={"Content-Disposition": "attachment; filename=resume.pdf"}
                    )
                else:
                    # Fallback to xelatex if pdflatex failed
                    combined_err = (result1.stderr or '') + "\n" + (result2.stderr or '')
                    print(f"LaTeX compilation failed with pdflatex, trying xelatex...\n{combined_err}")

                    xelatex = 'xelatex'
                    # Try common MiKTeX xelatex path as well
                    for candidate in [
                        os.path.expandvars(r"%LocalAppData%\Programs\MiKTeX\miktex\bin\x64\xelatex.exe"),
                        os.path.expandvars(r"%ProgramFiles%\MiKTeX\miktex\bin\x64\xelatex.exe"),
                    ]:
                        if os.path.isfile(candidate):
                            xelatex = candidate
                            break

                    args_xe = [
                        xelatex,
                        '-interaction=nonstopmode',
                        '-halt-on-error',
                        '-output-directory', temp_dir,
                        tex_file,
                    ]
                    try:
                        r1 = subprocess.run(args_xe, capture_output=True, text=True, timeout=120)
                        r2 = subprocess.run(args_xe, capture_output=True, text=True, timeout=120)
                        if os.path.exists(pdf_file) and (r2.returncode == 0 or r1.returncode == 0):
                            with open(pdf_file, 'rb') as f:
                                pdf_content = f.read()
                            return StreamingResponse(
                                BytesIO(pdf_content),
                                media_type="application/pdf",
                                headers={"Content-Disposition": "attachment; filename=resume.pdf"}
                            )
                        else:
                            print(f"XeLaTeX compilation failed as well.\n{(r1.stderr or '')}\n{(r2.stderr or '')}")
                            return render_pdf_placeholder()
                    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                        print(f"XeLaTeX compilation error: {e}")
                        return render_pdf_placeholder()
                    
            except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                print(f"LaTeX compilation error: {e}")
                return render_pdf_placeholder()
                
    except Exception as e:
        print(f"PDF generation error: {e}")
        return render_pdf_placeholder()


def render_pdf_placeholder() -> StreamingResponse:
    """Fallback PDF placeholder when LaTeX is not available"""
    buf = BytesIO()
    buf.write(b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n")
    buf.write(b"2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n")
    buf.write(b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>endobj\n")
    stream = b"BT /F1 24 Tf 72 720 Td (Resume PDF - LaTeX not available) Tj ET"
    buf.write(f"4 0 obj<</Length {len(stream)}>>stream\n".encode("ascii") + stream + b"\nendstream endobj\n")
    buf.write(b"5 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj\n")
    xref_pos = buf.tell()
    xref = b"xref\n0 6\n0000000000 65535 f \n" \
        b"0000000010 00000 n \n0000000060 00000 n \n0000000118 00000 n \n0000000274 00000 n \n0000000395 00000 n \n"
    buf.write(xref)
    buf.write(b"trailer<</Size 6/Root 1 0 R>>\nstartxref\n")
    buf.write(str(xref_pos).encode("ascii") + b"\n%%EOF")
    buf.seek(0)
    return StreamingResponse(buf, media_type="application/pdf")


