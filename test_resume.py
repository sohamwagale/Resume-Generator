#!/usr/bin/env python3
"""
Test script to verify resume PDF generation works correctly
"""

from app import create_ats_resume

# Sample resume data
sample_data = {
    'full_name': 'Soham Wagale',
    'job_title': 'Computer Science Student | Aspiring Software Engineer',
    'email': 'sohamwagale@gmail.com',
    'phone': '+91 9552804518',
    'location': 'Kasaba Bavada, Kolhapur, Maharashtra, India',
    'linkedin': 'linkedin.com/in/soham-wagale',
    'website': 'www.sohamwagale.com',

    'summary': (
        'Motivated Computer Science student with a strong foundation in programming, '
        'data structures, and problem-solving. Experienced in applying theoretical '
        'concepts to practical projects, collaborating in team-based environments, '
        'and continuously learning new technologies. Passionate about building '
        'efficient, scalable software solutions.'
    ),

    'skills': (
        'Technical Skills: Python, C/C++, Java, Data Structures & Algorithms, '
        'Object-Oriented Programming, Operating Systems, DBMS, SQL, Git/GitHub, '
        'HTML, CSS, Command Line, VS Code, IntelliJ\n'
        'Soft Skills: Problem Solving, Analytical Thinking, Team Collaboration, '
        'Communication, Time Management, Adaptability'
    ),

    # Work Experience
    'experience_count': '1',
    'experience_0_title': 'Internship Coordinator',
    'experience_0_company': 'Training and Placement Club, DYPCET',
    'experience_0_dates': 'Jun 2025 - Present',
    'experience_0_description': (
        'Assisted in organizing and conducting campus placement drives\n'
        'Coordinated internship opportunities for the 2027 graduating batch\n'
        'Collaborated with students, faculty, and recruiters to ensure smooth execution'
    ),

    # Education
    'education_count': '1',
    'education_0_degree': 'Bachelor of Technology in Computer Science',
    'education_0_school': 'D. Y. Patil College of Engineering and Technology (DYPCET)',
    'education_0_year': '2027',
    'education_0_details': 'CGPA: 8.6',

    # Certifications
    'certifications': (
        'AWS Certified Cloud Practitioner (Expected 2027)'
    ),

    # Projects
    'projects': (
        'Handwritten Digit Recognizer – Built a machine learning '
        'model to classify handwritten digits using neural networks\n'
        'MediPass – Medical Health Records Management System – Developed a system '
        'to securely manage and access patient medical records'
    ),

    # Additional Information
    'additional': (
        'Languages: English (Fluent), Marathi (Native)'
    )
}


def test_pdf_generation():
    print("Testing PDF generation...")
    print("-" * 50)
    
    try:
        # Generate PDF
        pdf_buffer = create_ats_resume(sample_data)
        
        # Save to file
        with open('test_resume.pdf', 'wb') as f:
            f.write(pdf_buffer.read())
        
        print("✓ PDF generated successfully!")
        print("✓ Saved to: /home/claude/test_resume.pdf")
        print("-" * 50)
        print("Test Summary:")
        print(f"  - Name: {sample_data['full_name']}")
        print(f"  - Email: {sample_data['email']}")
        print(f"  - Experiences: {sample_data['experience_count']}")
        print(f"  - Education: {sample_data['education_count']}")
        print("-" * 50)
        return True
        
    except Exception as e:
        print(f"✗ Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_pdf_generation()
    exit(0 if success else 1)