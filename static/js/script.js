/* ============================================
   STATE
============================================ */
let experienceCount = 0;
let educationCount = 0;

const SECTIONS = ['personal', 'summary', 'skills', 'experience', 'education', 'certifications', 'projects', 'additional'];

const SECTION_NAMES = {
    personal: 'Personal Information',
    summary: 'Professional Summary',
    skills: 'Skills',
    experience: 'Work Experience',
    education: 'Education',
    certifications: 'Certifications',
    projects: 'Projects',
    additional: 'Additional Information'
};

/* ============================================
   SIDEBAR NAVIGATION
============================================ */
function showSection(sectionId) {
    // Hide all panels
    document.querySelectorAll('.section-panel').forEach(p => p.classList.remove('active'));
    // Deactivate all nav items
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

    // Show target panel
    const panel = document.getElementById('section-' + sectionId);
    if (panel) panel.classList.add('active');

    // Activate nav item
    const navItem = document.querySelector(`.nav-item[data-section="${sectionId}"]`);
    if (navItem) navItem.classList.add('active');

    // Update topbar subtitle
    const subtitle = document.getElementById('currentSectionName');
    if (subtitle) subtitle.textContent = SECTION_NAMES[sectionId] || sectionId;

    // Scroll main content to top
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Close mobile sidebar if open
    closeMobileSidebar();
}

/* ============================================
   MOBILE SIDEBAR TOGGLE
============================================ */
function toggleMobileSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    sidebar.classList.toggle('open');
    overlay.classList.toggle('open');
}

function closeMobileSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    sidebar.classList.remove('open');
    overlay.classList.remove('open');
}

/* ============================================
   PROGRESS TRACKING
============================================ */
function updateProgress() {
    const form = document.getElementById('resumeForm');
    if (!form) return;

    let filledSections = 0;

    // personal – check name + email
    const name = form.querySelector('#full_name')?.value?.trim();
    const email = form.querySelector('#email')?.value?.trim();
    if (name && email) {
        markSection('personal', true);
        filledSections++;
    } else {
        markSection('personal', false);
    }

    // summary
    const summary = form.querySelector('#summary')?.value?.trim();
    if (summary) { markSection('summary', true); filledSections++; }
    else markSection('summary', false);

    // skills
    const skills = form.querySelector('#skills')?.value?.trim();
    if (skills) { markSection('skills', true); filledSections++; }
    else markSection('skills', false);

    // experience – at least one filled title
    const expTitles = form.querySelectorAll('[name^="experience_"][name$="_title"]');
    const hasExp = [...expTitles].some(i => i.value.trim());
    if (hasExp) { markSection('experience', true); filledSections++; }
    else markSection('experience', false);

    // education – at least one filled degree
    const eduDegrees = form.querySelectorAll('[name^="education_"][name$="_degree"]');
    const hasEdu = [...eduDegrees].some(i => i.value.trim());
    if (hasEdu) { markSection('education', true); filledSections++; }
    else markSection('education', false);

    // certifications (optional)
    const certs = form.querySelector('#certifications')?.value?.trim();
    if (certs) { markSection('certifications', true); filledSections++; }
    else markSection('certifications', false);

    // projects (optional)
    const projects = form.querySelector('#projects')?.value?.trim();
    if (projects) { markSection('projects', true); filledSections++; }
    else markSection('projects', false);

    // additional (optional)
    const additional = form.querySelector('#additional')?.value?.trim();
    if (additional) { markSection('additional', true); filledSections++; }
    else markSection('additional', false);

    const pct = Math.round((filledSections / SECTIONS.length) * 100);
    const bar = document.getElementById('progressBar');
    const pctEl = document.getElementById('progressPercent');
    if (bar) bar.style.width = pct + '%';
    if (pctEl) pctEl.textContent = pct + '%';
}

function markSection(sectionId, done) {
    const check = document.getElementById('check-' + sectionId);
    if (!check) return;
    if (done) check.classList.add('done');
    else check.classList.remove('done');
}

/* ============================================
   LOCALSTORAGE AUTO-SAVE
============================================ */
function saveField(e) {
    const el = e.target;
    if (el.name) {
        localStorage.setItem('rf_' + el.name, el.value);
        updateProgress();
    }
}

function loadSavedFields() {
    const form = document.getElementById('resumeForm');
    if (!form) return;

    const staticInputs = form.querySelectorAll('input:not([type=hidden]), textarea');
    staticInputs.forEach(el => {
        const saved = localStorage.getItem('rf_' + el.name);
        if (saved !== null && !el.value) {
            el.value = saved;
        }
    });
}

/* ============================================
   EXPERIENCE ENTRIES
============================================ */
function addExperience() {
    const container = document.getElementById('experienceContainer');
    const idx = experienceCount;

    const card = document.createElement('div');
    card.className = 'entry-card';
    card.id = `experience-${idx}`;

    // Try to load saved data
    const savedTitle = localStorage.getItem(`rf_experience_${idx}_title`) || '';
    const savedCompany = localStorage.getItem(`rf_experience_${idx}_company`) || '';
    const savedDates = localStorage.getItem(`rf_experience_${idx}_dates`) || '';
    const savedDesc = localStorage.getItem(`rf_experience_${idx}_description`) || '';

    card.innerHTML = `
        <div class="entry-card-header">
            <div class="entry-card-label">
                <span class="entry-card-num">${idx + 1}</span>
                Work Experience
            </div>
            <button type="button" class="btn-remove" onclick="removeExperience(${idx})">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                Remove
            </button>
        </div>
        <div class="entry-grid">
            <div class="form-group full-width">
                <label for="experience_${idx}_title">Job Title <span class="required">*</span></label>
                <input type="text"
                       id="experience_${idx}_title"
                       name="experience_${idx}_title"
                       required
                       placeholder="Senior Software Engineer"
                       value="${escapeHtml(savedTitle)}">
            </div>
            <div class="form-group">
                <label for="experience_${idx}_company">Company <span class="required">*</span></label>
                <input type="text"
                       id="experience_${idx}_company"
                       name="experience_${idx}_company"
                       required
                       placeholder="Tech Corp Inc."
                       value="${escapeHtml(savedCompany)}">
            </div>
            <div class="form-group">
                <label for="experience_${idx}_dates">Dates <span class="required">*</span></label>
                <input type="text"
                       id="experience_${idx}_dates"
                       name="experience_${idx}_dates"
                       required
                       placeholder="Jan 2020 – Present"
                       value="${escapeHtml(savedDates)}">
            </div>
            <div class="form-group full-width">
                <label for="experience_${idx}_description">Achievements &amp; Responsibilities</label>
                <textarea id="experience_${idx}_description"
                          name="experience_${idx}_description"
                          rows="5"
                          placeholder="• Led development of microservices architecture serving 1M+ daily users&#10;• Reduced API latency by 40% through query optimization and Redis caching&#10;• Mentored a team of 5 junior engineers and ran weekly code reviews">${escapeHtml(savedDesc)}</textarea>
            </div>
        </div>
    `;

    container.appendChild(card);
    experienceCount++;
    updateExperienceCount();
    attachDynamicListeners(card);
    updateProgress();
}

function removeExperience(idx) {
    const item = document.getElementById(`experience-${idx}`);
    if (item) {
        item.style.opacity = '0';
        item.style.transform = 'scale(0.96)';
        item.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
        setTimeout(() => {
            item.remove();
            updateExperienceCount();
            refreshExperienceNumbers();
            updateProgress();
        }, 200);
    }
}

function updateExperienceCount() {
    const items = document.querySelectorAll('.entry-card[id^="experience-"]');
    document.getElementById('experience_count').value = items.length;
}

function refreshExperienceNumbers() {
    document.querySelectorAll('.entry-card[id^="experience-"]').forEach((card, i) => {
        const numEl = card.querySelector('.entry-card-num');
        if (numEl) numEl.textContent = i + 1;
    });
}

/* ============================================
   EDUCATION ENTRIES
============================================ */
function addEducation() {
    const container = document.getElementById('educationContainer');
    const idx = educationCount;

    const card = document.createElement('div');
    card.className = 'entry-card';
    card.id = `education-${idx}`;

    const savedDegree = localStorage.getItem(`rf_education_${idx}_degree`) || '';
    const savedSchool = localStorage.getItem(`rf_education_${idx}_school`) || '';
    const savedYear = localStorage.getItem(`rf_education_${idx}_year`) || '';
    const savedDetails = localStorage.getItem(`rf_education_${idx}_details`) || '';

    card.innerHTML = `
        <div class="entry-card-header">
            <div class="entry-card-label">
                <span class="entry-card-num">${idx + 1}</span>
                Education
            </div>
            <button type="button" class="btn-remove" onclick="removeEducation(${idx})">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                Remove
            </button>
        </div>
        <div class="entry-grid">
            <div class="form-group full-width">
                <label for="education_${idx}_degree">Degree <span class="required">*</span></label>
                <input type="text"
                       id="education_${idx}_degree"
                       name="education_${idx}_degree"
                       required
                       placeholder="Bachelor of Science in Computer Science"
                       value="${escapeHtml(savedDegree)}">
            </div>
            <div class="form-group">
                <label for="education_${idx}_school">School / University <span class="required">*</span></label>
                <input type="text"
                       id="education_${idx}_school"
                       name="education_${idx}_school"
                       required
                       placeholder="Stanford University"
                       value="${escapeHtml(savedSchool)}">
            </div>
            <div class="form-group">
                <label for="education_${idx}_year">Graduation Year</label>
                <input type="text"
                       id="education_${idx}_year"
                       name="education_${idx}_year"
                       placeholder="2022"
                       value="${escapeHtml(savedYear)}">
            </div>
            <div class="form-group full-width">
                <label for="education_${idx}_details">Additional Details</label>
                <textarea id="education_${idx}_details"
                          name="education_${idx}_details"
                          rows="2"
                          placeholder="GPA: 3.9 / 4.0 · Dean's List · Relevant Coursework: Algorithms, ML, Distributed Systems">${escapeHtml(savedDetails)}</textarea>
            </div>
        </div>
    `;

    container.appendChild(card);
    educationCount++;
    updateEducationCount();
    attachDynamicListeners(card);
    updateProgress();
}

function removeEducation(idx) {
    const item = document.getElementById(`education-${idx}`);
    if (item) {
        item.style.opacity = '0';
        item.style.transform = 'scale(0.96)';
        item.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
        setTimeout(() => {
            item.remove();
            updateEducationCount();
            refreshEducationNumbers();
            updateProgress();
        }, 200);
    }
}

function updateEducationCount() {
    const items = document.querySelectorAll('.entry-card[id^="education-"]');
    document.getElementById('education_count').value = items.length;
}

function refreshEducationNumbers() {
    document.querySelectorAll('.entry-card[id^="education-"]').forEach((card, i) => {
        const numEl = card.querySelector('.entry-card-num');
        if (numEl) numEl.textContent = i + 1;
    });
}

/* ============================================
   ATTACH AUTO-SAVE TO DYNAMIC INPUTS
============================================ */
function attachDynamicListeners(container) {
    container.querySelectorAll('input, textarea').forEach(el => {
        el.addEventListener('input', saveField);
    });
}

/* ============================================
   TOAST NOTIFICATIONS
============================================ */
function showToast(msg, duration = 3000) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), duration);
}

/* ============================================
   UTILITY
============================================ */
function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/"/g, '&quot;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

/* ============================================
   FORM SUBMISSION
============================================ */
function handleSubmit(e) {
    const form = document.getElementById('resumeForm');
    const name = form.querySelector('#full_name')?.value?.trim();
    const email = form.querySelector('#email')?.value?.trim();

    if (!name || !email) {
        e.preventDefault();
        showToast('⚠️ Please fill in at least your name and email before generating.');
        showSection('personal');
        return;
    }

    updateExperienceCount();
    updateEducationCount();

    const btn = document.getElementById('generateBtn');
    if (btn) {
        btn.disabled = true;
        btn.classList.add('loading');
        btn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="2" x2="12" y2="6"/><line x1="12" y1="18" x2="12" y2="22"/><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"/><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"/><line x1="2" y1="12" x2="6" y2="12"/><line x1="18" y1="12" x2="22" y2="12"/><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"/><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"/></svg>
            Generating PDF…
        `;

        // Re-enable after a few seconds in case of error
        setTimeout(() => {
            btn.disabled = false;
            btn.classList.remove('loading');
            btn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
                Generate Resume PDF
            `;
        }, 8000);
    }
}

/* ============================================
   CLEAR FORM
============================================ */
function clearForm() {
    if (confirm('Reset all form data? This cannot be undone.')) {
        // Clear rf_ keys only
        Object.keys(localStorage).forEach(k => {
            if (k.startsWith('rf_')) localStorage.removeItem(k);
        });
        location.reload();
    }
}

/* ============================================
   INIT
============================================ */
document.addEventListener('DOMContentLoaded', function () {
    // Start on personal section
    showSection('personal');

    // Add default entries
    addExperience();
    addEducation();

    // Load saved static fields
    loadSavedFields();

    // Auto-save for static inputs
    document.querySelectorAll('#resumeForm input:not([type=hidden]), #resumeForm textarea').forEach(el => {
        el.addEventListener('input', saveField);
    });

    // Update progress based on loaded data
    updateProgress();

    // Form submit handler
    const form = document.getElementById('resumeForm');
    if (form) form.addEventListener('submit', handleSubmit);
});