from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import os
from datetime import datetime

app = Flask(__name__)

def create_ats_resume(data):
    """
    Create an ATS-friendly resume PDF from form data.
    ATS systems prefer simple, clean formatting without complex layouts.
    """
    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )
    
    # Container for PDF elements
    story = []
    
    # Get default styles
    styles = getSampleStyleSheet()
    
    # Create custom ATS-friendly styles
    # Name style - larger, bold
    name_style = ParagraphStyle(
        'CustomName',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.black,
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Contact info style
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=12
    )
    
    # Section heading style
    section_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.black,
        spaceAfter=6,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        borderWidth=1,
        borderColor=colors.black,
        borderPadding=3,
        backColor=colors.HexColor('#f0f0f0')
    )
    
    # Job title style
    job_title_style = ParagraphStyle(
        'JobTitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        fontName='Helvetica-Bold',
        spaceAfter=2
    )
    
    # Company/dates style
    company_style = ParagraphStyle(
        'CompanyStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        fontName='Helvetica-Oblique',
        spaceAfter=6
    )
    
    # Normal text style
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        spaceAfter=6,
        leftIndent=0.25*inch
    )
    
    # Bullet point style
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        spaceAfter=4,
        leftIndent=0.5*inch,
        bulletIndent=0.25*inch
    )
    
    # Header: Name
    story.append(Paragraph(data['full_name'], name_style))
    
    # Contact Information
    contact_parts = []
    if data.get('email'):
        contact_parts.append(data['email'])
    if data.get('phone'):
        contact_parts.append(data['phone'])
    if data.get('location'):
        contact_parts.append(data['location'])
    if data.get('linkedin'):
        contact_parts.append(data['linkedin'])
    if data.get('website'):
        contact_parts.append(data['website'])
    
    contact_line = ' | '.join(contact_parts)
    story.append(Paragraph(contact_line, contact_style))
    
    # Professional Summary
    if data.get('summary'):
        story.append(Paragraph('PROFESSIONAL SUMMARY', section_style))
        story.append(Paragraph(data['summary'], normal_style))
    
    # Skills
    if data.get('skills'):
        story.append(Paragraph('SKILLS', section_style))
        story.append(Paragraph(data['skills'], normal_style))
    
    # Work Experience
    if data.get('experience_count'):
        story.append(Paragraph('WORK EXPERIENCE', section_style))
        
        for i in range(int(data['experience_count'])):
            job_title = data.get(f'experience_{i}_title', '')
            company = data.get(f'experience_{i}_company', '')
            dates = data.get(f'experience_{i}_dates', '')
            description = data.get(f'experience_{i}_description', '')
            
            if job_title:
                story.append(Paragraph(job_title, job_title_style))
            
            if company or dates:
                company_line = f"{company}"
                if dates:
                    company_line += f" | {dates}"
                story.append(Paragraph(company_line, company_style))
            
            if description:
                # Split by newlines and create bullet points
                desc_lines = description.split('\n')
                for line in desc_lines:
                    line = line.strip()
                    if line:
                        # Remove bullet point if already present
                        if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                            line = line[1:].strip()
                        story.append(Paragraph(f"• {line}", bullet_style))
            
            story.append(Spacer(1, 0.1*inch))
    
    # Education
    if data.get('education_count'):
        story.append(Paragraph('EDUCATION', section_style))
        
        for i in range(int(data['education_count'])):
            degree = data.get(f'education_{i}_degree', '')
            school = data.get(f'education_{i}_school', '')
            year = data.get(f'education_{i}_year', '')
            details = data.get(f'education_{i}_details', '')
            
            if degree:
                story.append(Paragraph(degree, job_title_style))
            
            if school or year:
                school_line = f"{school}"
                if year:
                    school_line += f" | {year}"
                story.append(Paragraph(school_line, company_style))
            
            if details:
                story.append(Paragraph(details, normal_style))
            
            story.append(Spacer(1, 0.1*inch))
    
    # Certifications
    if data.get('certifications'):
        story.append(Paragraph('CERTIFICATIONS', section_style))
        cert_lines = data['certifications'].split('\n')
        for line in cert_lines:
            line = line.strip()
            if line:
                if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                    line = line[1:].strip()
                story.append(Paragraph(f"• {line}", bullet_style))
    
    # Projects
    if data.get('projects'):
        story.append(Paragraph('PROJECTS', section_style))
        project_lines = data['projects'].split('\n')
        for line in project_lines:
            line = line.strip()
            if line:
                if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                    line = line[1:].strip()
                story.append(Paragraph(f"• {line}", bullet_style))
    
    # Additional Sections
    if data.get('additional'):
        story.append(Paragraph('ADDITIONAL INFORMATION', section_style))
        story.append(Paragraph(data['additional'], normal_style))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_resume():
    # Get form data
    data = request.form.to_dict()
    
    # Create PDF
    pdf_buffer = create_ats_resume(data)
    
    # Generate filename
    filename = f"resume_{data.get('full_name', 'download').replace(' ', '_')}.pdf"
    
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)