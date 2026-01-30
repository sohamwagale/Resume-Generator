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
    Professional formatting with clean layout and proper spacing.
    """
    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=0.2*inch,
        bottomMargin=0.2*inch,
        leftMargin=0.6*inch,
        rightMargin=0.6*inch
    )
    
    # Container for PDF elements
    story = []
    
    # Get default styles
    styles = getSampleStyleSheet()
    
    # Professional color scheme
    primary_color = colors.HexColor('#1a1a1a')  # Almost black for text
    accent_color = colors.HexColor('#2c3e50')   # Dark blue-gray for accents
    line_color = colors.HexColor('#333333')     # Dark gray for lines
    
    # Name style - large, bold, centered, uppercase
    name_style = ParagraphStyle(
        'CustomName',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=primary_color,
        spaceAfter=4,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=24,
        letterSpacing=1
    )
    
    # Title/subtitle style (professional headline under name)
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=accent_color,
        alignment=TA_CENTER,
        spaceAfter=8,
        fontName='Helvetica-Bold',
        leading=14
    )
    
    # Contact info style - smaller, centered
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontSize=9.5,
        textColor=primary_color,
        alignment=TA_CENTER,
        spaceAfter=16,
        fontName='Helvetica',
        leading=12
    )
    
    # Section heading style - bold, uppercase, professional spacing
    section_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=primary_color,
        spaceAfter=10,
        spaceBefore=16,
        fontName='Helvetica-Bold',
        borderWidth=0,
        borderPadding=0,
        leading=14,
        letterSpacing=0.5
    )
    
    # Job title style - bold, slightly larger
    job_title_style = ParagraphStyle(
        'JobTitle',
        parent=styles['Normal'],
        fontSize=10.5,
        textColor=primary_color,
        fontName='Helvetica-Bold',
        spaceAfter=2,
        spaceBefore=8,
        leading=13
    )
    
    # Company/location style - regular weight
    company_style = ParagraphStyle(
        'CompanyStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=accent_color,
        fontName='Helvetica',
        spaceAfter=6,
        leading=12
    )
    
    # Date style - for right-aligned dates
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=accent_color,
        fontName='Helvetica',
        alignment=TA_LEFT,
        leading=12
    )
    
    # Normal text style - professional spacing
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=primary_color,
        spaceAfter=10,
        leftIndent=0,
        fontName='Helvetica',
        leading=14,
        alignment=TA_LEFT
    )
    
    # Bullet point style - optimized spacing and indent
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=primary_color,
        spaceAfter=4,
        leftIndent=0.15*inch,
        bulletIndent=0,
        fontName='Helvetica',
        leading=13
    )
    
    # ===== HEADER SECTION =====
    # Name (large, centered, bold, uppercase)
    story.append(Paragraph(data['full_name'].upper(), name_style))
    
    # Professional title/headline
    title_line = data.get('job_title', '')
    if title_line:
        story.append(Paragraph(title_line, subtitle_style))
    
    # Contact Information (single line, pipe-separated)
    contact_parts = []
    if data.get('location'):
        contact_parts.append(data['location'])
    if data.get('email'):
        contact_parts.append(data['email'])
    if data.get('phone'):
        contact_parts.append(data['phone'])
    if data.get('linkedin'):
        contact_parts.append(data['linkedin'])
    if data.get('website'):
        contact_parts.append(data['website'])
    
    if contact_parts:
        contact_line = ' | '.join(contact_parts)
        story.append(Paragraph(contact_line, contact_style))
    
    # Horizontal line separator
    from reportlab.platypus import HRFlowable
    story.append(HRFlowable(width="100%", thickness=1.5, color=line_color, spaceAfter=14, spaceBefore=2))
    
    # ===== PROFESSIONAL SUMMARY =====
    if data.get('summary'):
        story.append(Paragraph('<b>PROFESSIONAL SUMMARY</b>', section_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceAfter=8, spaceBefore=0))
        story.append(Paragraph(data['summary'], normal_style))
    
    # ===== WORK EXPERIENCE =====
    if data.get('experience_count') and int(data['experience_count']) > 0:
        story.append(Paragraph('<b>WORK EXPERIENCE</b>', section_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceAfter=8, spaceBefore=0))
        
        for i in range(int(data['experience_count'])):
            job_title = data.get(f'experience_{i}_title', '')
            company = data.get(f'experience_{i}_company', '')
            dates = data.get(f'experience_{i}_dates', '')
            description = data.get(f'experience_{i}_description', '')
            
            # Job title
            if job_title:
                story.append(Paragraph(f'<b>{job_title}</b>', job_title_style))
            
            # Company and dates on same line - professional alignment
            if company or dates:
                # Create table for perfect alignment
                company_text = company if company else ''
                dates_text = dates if dates else ''
                
                company_dates_data = [[Paragraph(company_text, company_style), 
                                      Paragraph(dates_text, date_style)]]
                company_dates_table = Table(company_dates_data, colWidths=[4.8*inch, 2.2*inch])
                company_dates_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ('TOPPADDING', (0, 0), (-1, -1), 0),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ]))
                story.append(company_dates_table)
            
            # Description with bullet points
            if description:
                desc_lines = description.split('\n')
                for line in desc_lines:
                    line = line.strip()
                    if line:
                        # Clean up existing bullet points
                        if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                            line = line[1:].strip()
                        story.append(Paragraph(f"• {line}", bullet_style))
            
            # Spacing between experience entries
            if i < int(data['experience_count']) - 1:
                story.append(Spacer(1, 0.12*inch))
    
    # ===== EDUCATION =====
    if data.get('education_count') and int(data['education_count']) > 0:
        story.append(Paragraph('<b>EDUCATION</b>', section_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceAfter=8, spaceBefore=0))
        
        for i in range(int(data['education_count'])):
            degree = data.get(f'education_{i}_degree', '')
            school = data.get(f'education_{i}_school', '')
            year = data.get(f'education_{i}_year', '')
            details = data.get(f'education_{i}_details', '')
            
            # Degree name
            if degree:
                story.append(Paragraph(f'<b>{degree}</b>', job_title_style))
            
            # School and year alignment
            if school or year:
                school_text = school if school else ''
                year_text = f"Graduated: {year}" if year else ''
                
                school_year_data = [[Paragraph(school_text, company_style), 
                                    Paragraph(year_text, date_style)]]
                school_year_table = Table(school_year_data, colWidths=[4.8*inch, 2.2*inch])
                school_year_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ('TOPPADDING', (0, 0), (-1, -1), 0),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ]))
                story.append(school_year_table)
            
            # Additional details
            if details:
                story.append(Paragraph(details, normal_style))
            
            # Spacing between education entries
            if i < int(data['education_count']) - 1:
                story.append(Spacer(1, 0.1*inch))
    
    # ===== SKILLS =====
    if data.get('skills'):
        story.append(Paragraph('<b>SKILLS</b>', section_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceAfter=8, spaceBefore=0))
        
        # Handle multi-line skills formatting
        skill_lines = data['skills'].split('\n')
        for line in skill_lines:
            line = line.strip()
            if line:
                # If line already has a colon (like "Technical Skills: Python, Java")
                # display it without bullet, otherwise add bullet
                if ':' in line and not line.startswith('•') and not line.startswith('-'):
                    story.append(Paragraph(f"<b>{line.split(':')[0]}:</b> {':'.join(line.split(':')[1:])}", normal_style))
                else:
                    if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                        line = line[1:].strip()
                    story.append(Paragraph(f"• {line}", bullet_style))
    
    # ===== CERTIFICATIONS =====
    if data.get('certifications'):
        story.append(Paragraph('<b>CERTIFICATIONS</b>', section_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceAfter=8, spaceBefore=0))
        
        cert_lines = data['certifications'].split('\n')
        for line in cert_lines:
            line = line.strip()
            if line:
                if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                    line = line[1:].strip()
                story.append(Paragraph(f"• {line}", bullet_style))
    
    # ===== PROJECTS =====
    if data.get('projects'):
        story.append(Paragraph('<b>PROJECTS</b>', section_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceAfter=8, spaceBefore=0))
        
        project_lines = data['projects'].split('\n')
        for line in project_lines:
            line = line.strip()
            if line:
                if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                    line = line[1:].strip()
                story.append(Paragraph(f"• {line}", bullet_style))
    
    # ===== ADDITIONAL INFORMATION =====
    if data.get('additional'):
        story.append(Paragraph('<b>ADDITIONAL INFORMATION</b>', section_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceAfter=8, spaceBefore=0))
        
        # Check if it's multi-line or single block
        add_lines = data['additional'].split('\n')
        if len(add_lines) > 1:
            for line in add_lines:
                line = line.strip()
                if line:
                    # Format with category labels if present
                    if ':' in line and not line.startswith('•') and not line.startswith('-'):
                        story.append(Paragraph(f"<b>{line.split(':')[0]}:</b> {':'.join(line.split(':')[1:])}", normal_style))
                    else:
                        if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                            line = line[1:].strip()
                        story.append(Paragraph(f"• {line}", bullet_style))
        else:
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