#!/usr/bin/env python3
"""
Test script to verify resume PDF generation works correctly
"""

from app import create_ats_resume

# Sample resume data
sample_data = {
    'full_name': 'Jane Smith',
    'email': 'jane.smith@email.com',
    'phone': '(555) 123-4567',
    'location': 'San Francisco, CA',
    'linkedin': 'linkedin.com/in/janesmith',
    'website': 'www.janesmith.dev',
    'summary': 'Experienced Full-Stack Developer with 5+ years of expertise in building scalable web applications. Proficient in React, Node.js, and cloud technologies. Track record of delivering high-impact projects and leading development teams.',
    'skills': 'Technical Skills: JavaScript, Python, React, Node.js, AWS, Docker, PostgreSQL\nSoft Skills: Team Leadership, Agile Methodologies, Technical Writing, Problem Solving',
    'experience_count': '2',
    'experience_0_title': 'Senior Software Engineer',
    'experience_0_company': 'Tech Innovations Inc.',
    'experience_0_dates': 'Jan 2021 - Present',
    'experience_0_description': 'Led development of microservices architecture serving 500K+ daily users\nReduced API response time by 45% through optimization and caching strategies\nMentored team of 4 junior developers and conducted code reviews\nImplemented CI/CD pipeline reducing deployment time by 60%',
    'experience_1_title': 'Software Engineer',
    'experience_1_company': 'StartupXYZ',
    'experience_1_dates': 'Jun 2018 - Dec 2020',
    'experience_1_description': 'Built responsive web applications using React and Redux\nDeveloped RESTful APIs with Node.js and Express\nCollaborated with design team to implement pixel-perfect UIs\nImproved test coverage from 40% to 85%',
    'education_count': '1',
    'education_0_degree': 'Bachelor of Science in Computer Science',
    'education_0_school': 'University of California, Berkeley',
    'education_0_year': '2018',
    'education_0_details': 'GPA: 3.8/4.0, Summa Cum Laude, Dean\'s List all semesters',
    'certifications': 'AWS Certified Solutions Architect - Associate (2022)\nGoogle Cloud Professional Developer (2021)',
    'projects': 'E-Commerce Platform - Built full-stack application with 10K+ users using MERN stack\nTask Management App - Open-source project with 500+ GitHub stars',
    'additional': 'Languages: English (Native), Spanish (Fluent), French (Conversational)\nVolunteer: Code Mentor at Girls Who Code, Technical Workshop Instructor'
}

def test_pdf_generation():
    print("Testing PDF generation...")
    print("-" * 50)
    
    try:
        # Generate PDF
        pdf_buffer = create_ats_resume(sample_data)
        
        # Save to file
        with open('/home/claude/test_resume.pdf', 'wb') as f:
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