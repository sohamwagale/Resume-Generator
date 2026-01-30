// Initialize counters
let experienceCount = 0;
let educationCount = 0;

// Add experience entry
function addExperience() {
    const container = document.getElementById('experienceContainer');
    const experienceItem = document.createElement('div');
    experienceItem.className = 'experience-item';
    experienceItem.id = `experience-${experienceCount}`;
    
    experienceItem.innerHTML = `
        <div class="item-header">
            <span class="item-number">Experience #${experienceCount + 1}</span>
            <button type="button" class="btn-remove" onclick="removeExperience(${experienceCount})">Remove</button>
        </div>
        
        <div class="form-group">
            <label for="experience_${experienceCount}_title">Job Title *</label>
            <input type="text" 
                   id="experience_${experienceCount}_title" 
                   name="experience_${experienceCount}_title" 
                   required 
                   placeholder="Senior Software Engineer">
        </div>
        
        <div class="form-row">
            <div class="form-group">
                <label for="experience_${experienceCount}_company">Company *</label>
                <input type="text" 
                       id="experience_${experienceCount}_company" 
                       name="experience_${experienceCount}_company" 
                       required 
                       placeholder="Tech Corp Inc.">
            </div>
            <div class="form-group">
                <label for="experience_${experienceCount}_dates">Dates *</label>
                <input type="text" 
                       id="experience_${experienceCount}_dates" 
                       name="experience_${experienceCount}_dates" 
                       required 
                       placeholder="Jan 2020 - Present">
            </div>
        </div>
        
        <div class="form-group">
            <label for="experience_${experienceCount}_description">Description & Achievements</label>
            <textarea id="experience_${experienceCount}_description" 
                      name="experience_${experienceCount}_description" 
                      rows="5" 
                      placeholder="• Led development of microservices architecture serving 1M+ users&#10;• Reduced system latency by 40% through optimization&#10;• Mentored team of 5 junior developers"></textarea>
            <small class="form-hint">Use bullet points for achievements (one per line)</small>
        </div>
    `;
    
    container.appendChild(experienceItem);
    experienceCount++;
    updateExperienceCount();
}

// Remove experience entry
function removeExperience(index) {
    const item = document.getElementById(`experience-${index}`);
    if (item) {
        item.remove();
        // Update numbering
        updateExperienceNumbers();
    }
}

// Update experience numbers after removal
function updateExperienceNumbers() {
    const items = document.querySelectorAll('.experience-item');
    items.forEach((item, index) => {
        const numberSpan = item.querySelector('.item-number');
        if (numberSpan) {
            numberSpan.textContent = `Experience #${index + 1}`;
        }
    });
}

// Update experience count
function updateExperienceCount() {
    const items = document.querySelectorAll('.experience-item');
    document.getElementById('experience_count').value = items.length;
}

// Add education entry
function addEducation() {
    const container = document.getElementById('educationContainer');
    const educationItem = document.createElement('div');
    educationItem.className = 'education-item';
    educationItem.id = `education-${educationCount}`;
    
    educationItem.innerHTML = `
        <div class="item-header">
            <span class="item-number">Education #${educationCount + 1}</span>
            <button type="button" class="btn-remove" onclick="removeEducation(${educationCount})">Remove</button>
        </div>
        
        <div class="form-group">
            <label for="education_${educationCount}_degree">Degree *</label>
            <input type="text" 
                   id="education_${educationCount}_degree" 
                   name="education_${educationCount}_degree" 
                   required 
                   placeholder="Bachelor of Science in Computer Science">
        </div>
        
        <div class="form-row">
            <div class="form-group">
                <label for="education_${educationCount}_school">School/University *</label>
                <input type="text" 
                       id="education_${educationCount}_school" 
                       name="education_${educationCount}_school" 
                       required 
                       placeholder="Stanford University">
            </div>
            <div class="form-group">
                <label for="education_${educationCount}_year">Graduation Year</label>
                <input type="text" 
                       id="education_${educationCount}_year" 
                       name="education_${educationCount}_year" 
                       placeholder="2020">
            </div>
        </div>
        
        <div class="form-group">
            <label for="education_${educationCount}_details">Additional Details</label>
            <textarea id="education_${educationCount}_details" 
                      name="education_${educationCount}_details" 
                      rows="2" 
                      placeholder="GPA: 3.8/4.0, Dean's List, Relevant Coursework: Data Structures, Algorithms"></textarea>
        </div>
    `;
    
    container.appendChild(educationItem);
    educationCount++;
    updateEducationCount();
}

// Remove education entry
function removeEducation(index) {
    const item = document.getElementById(`education-${index}`);
    if (item) {
        item.remove();
        // Update numbering
        updateEducationNumbers();
    }
}

// Update education numbers after removal
function updateEducationNumbers() {
    const items = document.querySelectorAll('.education-item');
    items.forEach((item, index) => {
        const numberSpan = item.querySelector('.item-number');
        if (numberSpan) {
            numberSpan.textContent = `Education #${index + 1}`;
        }
    });
}

// Update education count
function updateEducationCount() {
    const items = document.querySelectorAll('.education-item');
    document.getElementById('education_count').value = items.length;
}

// Form submission handling
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('resumeForm');
    
    // Add at least one experience and one education on load
    addExperience();
    addEducation();
    
    form.addEventListener('submit', function(e) {
        const submitBtn = form.querySelector('.btn-submit');
        submitBtn.disabled = true;
        submitBtn.classList.add('loading');
        submitBtn.textContent = 'Generating PDF';
        
        // Update counts before submission
        updateExperienceCount();
        updateEducationCount();
    });
    
    // Auto-save to localStorage (optional feature)
    const inputs = form.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        // Load saved value
        const savedValue = localStorage.getItem(input.name);
        if (savedValue && !input.value) {
            input.value = savedValue;
        }
        
        // Save on change
        input.addEventListener('change', function() {
            localStorage.setItem(input.name, input.value);
        });
    });
});

// Clear form function (optional)
function clearForm() {
    if (confirm('Are you sure you want to clear all form data?')) {
        localStorage.clear();
        location.reload();
    }
}

// Validate form before submission
function validateForm() {
    const form = document.getElementById('resumeForm');
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = 'var(--error)';
            isValid = false;
        } else {
            field.style.borderColor = 'var(--border)';
        }
    });
    
    return isValid;
}