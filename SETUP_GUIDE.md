# Setup & Deployment Guide

## Local Development Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Web browser (Chrome, Firefox, Safari, or Edge)

### Installation Steps

1. **Navigate to the project directory**:
   ```bash
   cd ats-resume-generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install Flask reportlab
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```
   
   Or use the start script:
   ```bash
   ./start.sh
   ```

4. **Access the application**:
   Open your browser and go to:
   ```
   http://localhost:5000
   ```

### File Structure
```
ats-resume-generator/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── USAGE_GUIDE.md           # Detailed usage instructions
├── start.sh                 # Quick start script
├── test_resume.py           # Test script
├── sample_resume.pdf        # Example output
├── templates/
│   └── index.html          # Main HTML template
└── static/
    ├── css/
    │   └── style.css       # Stylesheet
    └── js/
        └── script.js       # JavaScript for form management
```

## Production Deployment

### Option 1: Deploy to Heroku

1. **Install Heroku CLI**:
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Create a Heroku app**:
   ```bash
   heroku create your-app-name
   ```

3. **Add a Procfile**:
   Create a file named `Procfile` with:
   ```
   web: python app.py
   ```

4. **Deploy**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

### Option 2: Deploy to PythonAnywhere

1. **Sign up** at [PythonAnywhere](https://www.pythonanywhere.com)

2. **Upload files** via the Files tab

3. **Create a new web app** with Flask

4. **Configure WSGI**:
   Edit `/var/www/your_username_pythonanywhere_com_wsgi.py`:
   ```python
   import sys
   path = '/home/your_username/ats-resume-generator'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

5. **Reload** the web app

### Option 3: Deploy to AWS EC2

1. **Launch an EC2 instance** (Ubuntu recommended)

2. **SSH into your instance**:
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install Python and dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

4. **Upload your application files**

5. **Install requirements**:
   ```bash
   pip3 install -r requirements.txt
   ```

6. **Run with Gunicorn** (production WSGI server):
   ```bash
   pip3 install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

7. **Setup Nginx** as reverse proxy (optional but recommended)

### Option 4: Deploy with Docker

1. **Create a Dockerfile**:
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 5000
   
   CMD ["python", "app.py"]
   ```

2. **Build the image**:
   ```bash
   docker build -t ats-resume-generator .
   ```

3. **Run the container**:
   ```bash
   docker run -p 5000:5000 ats-resume-generator
   ```

## Environment Configuration

### Production Settings

For production, modify `app.py`:

```python
if __name__ == '__main__':
    # Development
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    # Production
    # app.run(debug=False, host='0.0.0.0', port=5000)
```

### Environment Variables

Create a `.env` file for sensitive configuration:
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
PORT=5000
```

Load in `app.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
```

## Security Considerations

1. **HTTPS**: Always use HTTPS in production
2. **Input Validation**: The app includes basic validation
3. **File Upload Limits**: Configure max file sizes if adding upload features
4. **CSRF Protection**: Add Flask-WTF for form protection
5. **Rate Limiting**: Implement rate limiting for API endpoints

## Performance Optimization

### 1. Caching
Add Flask-Caching:
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

### 2. Database (Optional)
For storing resumes, add SQLAlchemy:
```python
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resumes.db'
db = SQLAlchemy(app)
```

### 3. CDN for Static Files
Serve CSS/JS from a CDN in production

## Monitoring & Logging

### Application Logs
Add logging to `app.py`:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Error Tracking
Integrate Sentry:
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()]
)
```

## Backup & Maintenance

### Backup Strategy
1. Regular backups of user data (if storing)
2. Database backups (if using)
3. Code repository on GitHub/GitLab

### Updates
1. Keep dependencies updated:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. Monitor for security vulnerabilities:
   ```bash
   pip install safety
   safety check
   ```

## Testing

### Run Test Suite
```bash
python test_resume.py
```

### Manual Testing Checklist
- [ ] Form submission with all fields
- [ ] Form submission with minimal fields
- [ ] PDF generation and download
- [ ] Multiple experience entries
- [ ] Multiple education entries
- [ ] Special characters in text
- [ ] Very long text in fields
- [ ] Mobile responsiveness
- [ ] Cross-browser compatibility

## Troubleshooting

### Common Issues

**Port Already in Use**:
```bash
# Change port in app.py or kill existing process
lsof -ti:5000 | xargs kill -9
```

**Module Not Found**:
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

**PDF Not Generating**:
- Check ReportLab installation
- Verify file permissions
- Check application logs

**Static Files Not Loading**:
- Verify static folder structure
- Check Flask static_url_path configuration
- Clear browser cache

## Scaling

For high traffic:

1. **Load Balancing**: Use multiple application instances
2. **Database**: Move to PostgreSQL/MySQL
3. **File Storage**: Use S3 for PDF storage
4. **Queue System**: Add Celery for async PDF generation
5. **Caching**: Implement Redis caching

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support & Resources

- **Documentation**: README.md, USAGE_GUIDE.md
- **Flask Docs**: https://flask.palletsprojects.com/
- **ReportLab Docs**: https://www.reportlab.com/docs/
- **Python Docs**: https://docs.python.org/3/

## License

This project is open source and available for personal and commercial use.

---

**Need Help?**
- Review error logs: `tail -f application.log`
- Check Flask documentation
- Test with sample data first
- Contact the development team

**Version**: 1.0.0  
**Last Updated**: January 2026