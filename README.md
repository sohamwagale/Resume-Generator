# ATS-Friendly Resume Generator

A Flask web application that converts a comprehensive form into an ATS (Applicant Tracking System) friendly resume PDF.

## Features

- **Comprehensive Form**: Capture all resume sections including personal info, summary, skills, experience, education, certifications, projects, and additional information
- **ATS-Optimized PDF**: Generates clean, text-based PDFs that parse well in Applicant Tracking Systems
- **Dynamic Sections**: Add multiple work experiences and education entries
- **Professional Design**: Modern, user-friendly web interface
- **Auto-Save**: Form data automatically saves to browser localStorage
- **Responsive**: Works on desktop and mobile devices

## What is ATS?

Applicant Tracking Systems (ATS) are software applications that help employers manage job applications. Many companies use ATS to scan and rank resumes before a human ever sees them. This tool creates resumes optimized for ATS by:

- Using standard fonts (Helvetica)
- Clear section headings
- Simple, clean formatting without complex layouts
- Text-based content (no images or graphics)
- Proper PDF structure for text extraction

## Installation

1. **Clone or download** this project

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install Flask reportlab
```

## Usage

1. **Start the Flask server**:
```bash
python app.py
```

2. **Open your browser** and navigate to:
```
http://localhost:5000
```

3. **Fill out the form** with your resume information:
   - Personal Information (name, email, phone, etc.)
   - Professional Summary
   - Skills
   - Work Experience (add multiple positions)
   - Education (add multiple degrees)
   - Certifications (optional)
   - Projects (optional)
   - Additional Information (optional)

4. **Click "Generate Resume PDF"** to download your ATS-friendly resume

## Form Sections Explained

### Personal Information
- **Full Name**: Your complete name as it should appear on the resume
- **Email**: Professional email address
- **Phone**: Contact number with area code
- **Location**: City and state/country
- **LinkedIn**: Your LinkedIn profile URL
- **Website**: Portfolio or personal website

### Professional Summary
A brief 3-4 sentence overview highlighting your:
- Years of experience
- Key skills and expertise
- Notable achievements
- Career objectives

### Skills
List your technical and soft skills. Tips:
- Group skills by category (e.g., "Technical Skills:", "Languages:")
- Use keywords from job descriptions
- Include proficiency levels if relevant

### Work Experience
For each position, include:
- **Job Title**: Your official position
- **Company**: Employer name
- **Dates**: Employment period (e.g., "Jan 2020 - Present")
- **Description**: Bullet points of achievements and responsibilities
  - Start with action verbs
  - Quantify achievements when possible
  - Focus on impact and results

### Education
For each degree:
- **Degree**: Full degree name (e.g., "Bachelor of Science in Computer Science")
- **School**: University or college name
- **Year**: Graduation year
- **Details**: GPA, honors, relevant coursework (optional)

### Certifications
List professional certifications with:
- Certification name
- Issuing organization
- Year obtained

### Projects
Highlight notable projects with:
- Project name
- Brief description
- Technologies used
- Impact/results

### Additional Information
Include relevant information such as:
- Languages spoken
- Publications
- Awards and honors
- Volunteer work
- Professional memberships

## ATS Optimization Tips

1. **Use Keywords**: Include relevant keywords from job descriptions
2. **Standard Formatting**: The generated PDF uses simple, clean formatting
3. **Clear Section Headers**: All sections have clear, standard headings
4. **No Images**: Avoid logos, photos, or graphics (ATS can't read them)
5. **Standard Fonts**: Uses Helvetica, which is universally readable
6. **Bullet Points**: Use bullet points for easy scanning
7. **File Format**: PDF is the recommended format for ATS

## Technical Details

### Technology Stack
- **Backend**: Flask (Python web framework)
- **PDF Generation**: ReportLab library
- **Frontend**: HTML5, CSS3, JavaScript
- **Storage**: Browser localStorage for auto-save

### File Structure
```
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main form template
├── static/
│   ├── css/
│   │   └── style.css     # Stylesheet
│   └── js/
│       └── script.js     # Form management
└── README.md             # Documentation
```

### PDF Structure
The generated PDF includes:
- Clean, single-column layout
- Standard section headings with gray background
- Proper text hierarchy (name > sections > content)
- Consistent spacing and margins
- Professional typography

## Customization

### Modify PDF Styling
Edit the `create_ats_resume()` function in `app.py` to customize:
- Font sizes and styles
- Colors and backgrounds
- Spacing and margins
- Section order

### Change Form Fields
Modify `templates/index.html` to:
- Add new form fields
- Change field labels
- Adjust placeholder text

### Update Styling
Edit `static/css/style.css` to:
- Change color scheme
- Modify layout
- Adjust responsive breakpoints

## Browser Compatibility

- Chrome/Edge: ✓ Fully supported
- Firefox: ✓ Fully supported
- Safari: ✓ Fully supported
- Mobile browsers: ✓ Responsive design

## Troubleshooting

### PDF Not Generating
- Check that all required fields are filled
- Verify Flask server is running
- Check browser console for errors

### Form Data Lost
- Browser localStorage may be cleared
- Try disabling private/incognito mode
- Manually save important data externally

### Styling Issues
- Clear browser cache
- Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
- Check for CSS file loading errors

## Contributing

To improve this application:
1. Add more resume templates
2. Implement PDF preview before download
3. Add export to Word format
4. Include sample content/templates
5. Add resume scoring feature

## License

This project is open source and available for personal and commercial use.

## Support

For issues or questions:
- Check this README first
- Review the code comments
- Test with sample data

## Version History

- **v1.0.0** - Initial release
  - Basic form with all resume sections
  - ATS-optimized PDF generation
  - Responsive design
  - Auto-save functionality

---

**Note**: This tool generates ATS-friendly resumes, but always review and tailor your resume for each specific job application. Include relevant keywords from the job description and quantify your achievements wherever possible.