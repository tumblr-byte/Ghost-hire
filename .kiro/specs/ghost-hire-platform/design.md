# Ghost Hire Platform - Design Document

## Overview

Ghost Hire is a Django-based web application that provides a haunted-themed hiring platform for self-taught developers. The system uses Google OAuth for authentication, implements AI-powered photo verification to prevent fraud, and features a spooky aesthetic with neon colors and horror-themed terminology.

The application follows Django's MVT (Model-View-Template) architecture and integrates with external services including Google OAuth (via django-allauth), SerpAPI for reverse image search, and PyTorch for face similarity detection using a Siamese neural network.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Browser                        │
│  (HTML/CSS/JS with haunted theme, Google Fonts, animations) │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Django Application                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              ghosthire (Project)                      │  │
│  │  - settings.py (config, allauth, database)           │  │
│  │  - urls.py (URL routing)                             │  │
│  │  - wsgi.py / asgi.py                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         haunted_profiles (App)                        │  │
│  │  - models.py (Custom User model)                     │  │
│  │  - views.py (Page handlers)                          │  │
│  │  - urls.py (App routing)                             │  │
│  │  - utils.py (Verification logic)                     │  │
│  │  - forms.py (Profile setup forms)                    │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────┬──────────────────────┬────────────────────────┘
             │                      │
             ▼                      ▼
┌─────────────────────┐  ┌──────────────────────────────────┐
│   MySQL Database    │  │    External Services             │
│  - ghosthire_db     │  │  - Google OAuth (allauth)        │
│  - User table       │  │  - SerpAPI (reverse search)      │
│  - Media storage    │  │  - PyTorch (Siamese network)     │
└─────────────────────┘  └──────────────────────────────────┘
```

### Technology Stack

- **Backend Framework**: Django 4.x
- **Database**: MySQL 8.x
- **Authentication**: django-allauth with Google OAuth provider
- **Image Processing**: Pillow (PIL)
- **Machine Learning**: PyTorch with torchvision
- **API Integration**: requests library for SerpAPI
- **Frontend**: HTML5, CSS3 with custom animations, vanilla JavaScript
- **Fonts**: Google Fonts (Creepster, Roboto Mono)

## Components and Interfaces

### 1. Custom User Model

**Location**: `haunted_profiles/models.py`

The User model extends Django's AbstractBaseUser and PermissionsMixin to provide custom authentication.

```python
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    # Custom manager for user creation
    pass

class User(AbstractBaseUser, PermissionsMixin):
    google_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    verification_photo = models.ImageField(upload_to='verification_photos/', blank=True)
    ghost_avatar = models.ImageField(upload_to='ghost_avatars/', default='ghost_avatars/1.png')
    is_verified = models.BooleanField(default=False)
    ghost_level = models.IntegerField(default=1)
    skills = models.JSONField(default=list, blank=True)
    bio = models.TextField(blank=True, max_length=500)
    github_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
```

**Key Design Decisions**:
- Use `google_id` as the unique identifier from OAuth
- Store `verification_photo` in a private directory not served publicly
- Store `ghost_avatar` in a public directory with default fallback
- Use JSONField for flexible skills storage (array of strings)
- Auto-generate username in format "ghost_XXXXX" where X is a random digit

### 2. Authentication Flow

**Integration**: django-allauth with Google provider

**Configuration** (`settings.py`):
```python
INSTALLED_APPS = [
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'haunted_profiles',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
SOCIALACCOUNT_AUTO_SIGNUP = True
```

**Custom Adapter** (`haunted_profiles/adapters.py`):
```python
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
import random

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        # Auto-generate ghost username
        user.username = f"ghost_{random.randint(10000, 99999)}"
        user.google_id = sociallogin.account.uid
        user.save()
        return user
```

**Flow**:
1. User clicks "Rise from the Grave" → redirects to `/accounts/google/login/`
2. Google OAuth completes → allauth creates/retrieves user
3. Custom adapter generates username and saves google_id
4. Redirect to verification page if not verified, else to haunted lair

### 3. Photo Verification System

**Location**: `haunted_profiles/utils.py`

#### 3.1 Reverse Image Search

```python
import requests
import os

def check_image_online(image_path):
    """
    Check if image exists online using SerpAPI.
    Returns: (exists_online: bool, sources: list)
    """
    api_key = os.environ.get('SERPAPI_KEY')
    if not api_key:
        # Log warning and skip check
        return False, []
    
    # Upload image to temporary hosting or use base64
    # Call SerpAPI reverse image search
    params = {
        'engine': 'google_reverse_image',
        'image_url': image_url,
        'api_key': api_key
    }
    
    response = requests.get('https://serpapi.com/search', params=params)
    data = response.json()
    
    # Check if similar images found
    if 'image_results' in data and len(data['image_results']) > 0:
        return True, [result['source'] for result in data['image_results'][:3]]
    
    return False, []
```

#### 3.2 Siamese Network Face Comparison

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as T
from PIL import Image

class SiameseNetwork(nn.Module):
    def __init__(self):
        super(SiameseNetwork, self).__init__()
        self.feature_extraction = torch.hub.load(
            "pytorch/vision:v0.10.0", "resnet18", pretrained=True
        )
        self.fc1 = nn.Linear(1000, 512)
        self.fc2 = nn.Linear(512, 256)
        self.dropout = nn.Dropout(p=0.3)
        self.out = nn.Linear(256, 1)

    def forward_once(self, x):
        return self.feature_extraction(x)

    def forward(self, x1, x2):
        out1 = self.forward_once(x1)
        out2 = self.forward_once(x2)
        diff = torch.abs(out1 - out2)
        x = F.relu(self.fc1(diff))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        out = torch.sigmoid(self.out(x))
        return out

# Global model instance
transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor()
])

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = None

def load_siamese_model():
    global model
    if model is None:
        model = SiameseNetwork().to(device)
        model.load_state_dict(torch.load("best_siamese_model.pth", map_location=device))
        model.eval()
    return model

def check_duplicate_face(uploaded_photo_path):
    """
    Compare uploaded photo with all existing users' verification photos.
    Returns: (is_duplicate: bool, matched_username: str or None)
    """
    from haunted_profiles.models import User
    
    model = load_siamese_model()
    uploaded_img = transform(Image.open(uploaded_photo_path).convert("RGB")).unsqueeze(0).to(device)
    
    existing_users = User.objects.filter(is_verified=True).exclude(verification_photo='')
    
    with torch.no_grad():
        for user in existing_users:
            try:
                existing_img_path = user.verification_photo.path
                existing_img = transform(Image.open(existing_img_path).convert("RGB")).unsqueeze(0).to(device)
                
                similarity_score = model(uploaded_img, existing_img).item()
                
                if similarity_score > 0.9:
                    return True, user.username
            except Exception as e:
                # Log error and continue
                continue
    
    return False, None
```

#### 3.3 Verification View Logic

```python
def verify_photo(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('verification_photo')
        
        # Save temporarily
        temp_path = save_temp_file(uploaded_file)
        
        # Step 1: Reverse image search
        exists_online, sources = check_image_online(temp_path)
        if exists_online:
            return render(request, 'verification.html', {
                'error': 'This photo exists online. Upload your real face, ghost.'
            })
        
        # Step 2: Duplicate face check
        is_duplicate, matched_user = check_duplicate_face(temp_path)
        if is_duplicate:
            return render(request, 'verification.html', {
                'error': 'This face already haunts our community. One ghost per person.'
            })
        
        # Step 3: Success - save and verify
        user = request.user
        user.verification_photo = uploaded_file
        user.is_verified = True
        user.save()
        
        messages.success(request, '✅ Verified Ghost! Welcome to the cemetery.')
        return redirect('haunt_setup')
```

### 4. Views and URL Routing

**URL Structure**:
```
/                           → homepage (index.html)
/accounts/google/login/     → Google OAuth (allauth)
/verification/              → verification page (verification.html)
/haunt-setup/               → profile setup (haunt_setup.html)
/profile/                   → user profile (profile.html)
/profile/<username>/        → public profile view
/return-to-shadows/         → logout
```

**Key Views** (`haunted_profiles/views.py`):

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    """Homepage with hero section"""
    return render(request, 'index.html')

@login_required
def verification(request):
    """Photo verification page"""
    if request.user.is_verified:
        return redirect('haunt_setup')
    # Handle verification logic
    return render(request, 'verification.html')

@login_required
def haunt_setup(request):
    """Profile setup page"""
    if not request.user.is_verified:
        return redirect('verification')
    
    if request.method == 'POST':
        # Process form
        user = request.user
        user.skills = request.POST.getlist('skills')
        user.bio = request.POST.get('bio', '')
        user.github_link = request.POST.get('github_link', '')
        
        if 'ghost_avatar' in request.FILES:
            user.ghost_avatar = request.FILES['ghost_avatar']
        
        user.save()
        return redirect('profile')
    
    return render(request, 'haunt_setup.html')

@login_required
def profile(request, username=None):
    """User profile page"""
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    return render(request, 'profile.html', {'profile_user': user})
```

### 5. Forms

**Location**: `haunted_profiles/forms.py`

```python
from django import forms
from .models import User

class ProfileSetupForm(forms.ModelForm):
    SKILL_CHOICES = [
        ('Computer Vision', 'Computer Vision'),
        ('Machine Learning', 'Machine Learning'),
        ('Django/Python', 'Django/Python'),
        ('React/Frontend', 'React/Frontend'),
        ('Game Development', 'Game Development'),
        ('Mobile Apps', 'Mobile Apps'),
        ('DevOps', 'DevOps'),
        ('UI/UX Design', 'UI/UX Design'),
    ]
    
    skills = forms.MultipleChoiceField(
        choices=SKILL_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = User
        fields = ['bio', 'github_link', 'ghost_avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'maxlength': 500, 'rows': 5}),
        }
```

## Data Models

### User Model Schema

```sql
CREATE TABLE haunted_profiles_user (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME(6),
    is_superuser TINYINT(1) NOT NULL,
    google_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    verification_photo VARCHAR(100),
    ghost_avatar VARCHAR(100) NOT NULL DEFAULT 'ghost_avatars/1.png',
    is_verified TINYINT(1) NOT NULL DEFAULT 0,
    ghost_level INT NOT NULL DEFAULT 1,
    skills JSON,
    bio LONGTEXT,
    github_link VARCHAR(200),
    created_at DATETIME(6) NOT NULL,
    is_staff TINYINT(1) NOT NULL DEFAULT 0,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    INDEX idx_google_id (google_id),
    INDEX idx_username (username),
    INDEX idx_is_verified (is_verified)
);
```

### Media File Organization

```
media/
├── verification_photos/     # Private - not served publicly
│   ├── user_123_abc.jpg
│   └── user_456_def.jpg
└── ghost_avatars/           # Public - served via MEDIA_URL
    ├── 1.png               # Default avatar
    ├── user_123_custom.jpg
    └── user_456_custom.png
```

**Settings Configuration**:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Custom file serving to protect verification photos
# In production, use nginx/apache to block /media/verification_photos/
```

## Error Handling

### 1. Authentication Errors

- **Google OAuth Failure**: Redirect to homepage with error message "Failed to enter the crypt. Try again."
- **Missing Google ID**: Log error and create user without google_id (fallback)
- **Duplicate Email**: allauth handles this automatically

### 2. Verification Errors

- **SerpAPI Unavailable**: Log warning, skip reverse image check, proceed to Siamese check
- **SerpAPI Rate Limit**: Display message "Verification temporarily unavailable. Try again in a few minutes."
- **Model File Missing**: Log critical error, display "Verification system offline. Contact support."
- **Image Processing Error**: Display "Invalid image file. Please upload a clear photo of your face."

### 3. Database Errors

- **Connection Failure**: Display generic error page "The cemetery is currently closed. Try again later."
- **Duplicate Username**: Regenerate username with new random number (retry up to 5 times)
- **File Upload Error**: Display "Failed to upload photo. Check file size and format."

### 4. Form Validation Errors

- **Bio Too Long**: Client-side validation + server-side truncation
- **Invalid GitHub URL**: Display "Invalid GitHub link format"
- **No Skills Selected**: Allow empty skills array (optional field)

## Testing Strategy

### 1. Unit Tests

**Location**: `haunted_profiles/tests/`

```python
# test_models.py
- Test User model creation with all fields
- Test username auto-generation uniqueness
- Test default values (ghost_level, is_verified, ghost_avatar)
- Test JSONField skills storage and retrieval

# test_utils.py
- Test check_image_online with mocked SerpAPI responses
- Test check_duplicate_face with sample images
- Test Siamese model loading and inference

# test_views.py
- Test homepage renders correctly
- Test verification page requires login
- Test haunt_setup redirects if not verified
- Test profile page displays user data correctly

# test_forms.py
- Test ProfileSetupForm validation
- Test bio max length enforcement
- Test skills checkbox selection
```

### 2. Integration Tests

```python
# test_auth_flow.py
- Test complete Google OAuth flow (mocked)
- Test user creation on first login
- Test existing user login
- Test redirect logic based on verification status

# test_verification_flow.py
- Test photo upload and reverse search
- Test duplicate face detection
- Test successful verification and redirect
- Test error handling for each rejection case
```

### 3. End-to-End Tests

- Manual testing of complete user journey:
  1. Homepage → Google login
  2. Verification photo upload (test rejection scenarios)
  3. Profile setup form submission
  4. Profile page display
  5. Logout and re-login

### 4. Performance Tests

- Test Siamese network inference time (should be < 2 seconds per comparison)
- Test database query performance with 1000+ users
- Test concurrent verification requests
- Test image upload with various file sizes

### 5. Security Tests

- Verify verification_photos directory is not publicly accessible
- Test SQL injection prevention in forms
- Test CSRF protection on all POST requests
- Test file upload restrictions (size, type)
- Verify OAuth token handling security

## CSS and Frontend Design

### Theme Variables

```css
:root {
    --bg-black: #0a0a0a;
    --neon-purple: #9d4edd;
    --neon-green: #39ff14;
    --text-gray: #e0e0e0;
    --neon-red: #ff0055;
    --font-header: 'Creepster', cursive;
    --font-body: 'Roboto Mono', monospace;
}
```

### Animation Keyframes

```css
@keyframes flicker {
    0%, 18%, 22%, 25%, 53%, 57%, 100% {
        opacity: 1;
        text-shadow: 0 0 10px var(--neon-purple);
    }
    20%, 24%, 55% { opacity: 0.4; }
}

@keyframes glitch {
    0% { transform: translate(0); }
    20% { transform: translate(-2px, 2px); }
    40% { transform: translate(-2px, -2px); }
    60% { transform: translate(2px, 2px); }
    80% { transform: translate(2px, -2px); }
    100% { transform: translate(0); }
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-15px); }
}

@keyframes fog {
    0% { transform: translateX(0) translateY(0); }
    50% { transform: translateX(50px) translateY(-20px); }
    100% { transform: translateX(0) translateY(0); }
}
```

### Component Styles

```css
/* Buttons */
.haunted-button {
    background: var(--neon-purple);
    color: var(--bg-black);
    font-family: var(--font-header);
    padding: 15px 30px;
    border: none;
    cursor: pointer;
    transition: all 0.3s;
}

.haunted-button:hover {
    animation: glitch 0.3s infinite;
    box-shadow: 0 0 5px var(--neon-purple), 
                0 0 10px var(--neon-purple), 
                0 0 20px var(--neon-purple);
}

/* Ghost Avatar */
.ghost-avatar {
    animation: float 3s ease-in-out infinite;
    border-radius: 50%;
    border: 3px solid var(--neon-green);
}

/* Skill Pills */
.skill-pill {
    background: var(--neon-purple);
    color: var(--bg-black);
    padding: 8px 16px;
    border-radius: 20px;
    display: inline-block;
    margin: 5px;
    font-family: var(--font-body);
}

/* Input Focus */
input:focus, textarea:focus {
    outline: none;
    box-shadow: 0 0 5px var(--neon-purple), 
                0 0 10px var(--neon-purple);
}
```

### Template Structure

**Base Template** (`templates/base.html`):
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Ghost Hire{% endblock %}</title>
    <link href="https://fonts.googleapis.com/css2?family=Creepster&family=Roboto+Mono&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/haunted.css' %}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="haunted-nav">
        <img src="{% static 'logo.png' %}" alt="Ghost Hire" class="logo">
        <div class="nav-links">
            {% if user.is_authenticated %}
                <a href="{% url 'profile' %}">Your Ghost</a>
                <a href="{% url 'logout' %}">Return to Shadows</a>
            {% else %}
                <a href="{% url 'socialaccount_signup' %}">Rise from the Grave</a>
            {% endif %}
        </div>
    </nav>
    
    <main>
        {% if messages %}
            <div class="messages">
                {% for message in messages %}
                    <div class="message {{ message.tags }}">{{ message }}</div>
                {% endfor %}
            </div>
        {% endif %}
        
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <p>&copy; 2025 Ghost Hire - Where Dead Careers Come to Life</p>
    </footer>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

## Deployment Considerations

### Environment Variables

```bash
# .env file
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=ghosthire.com,www.ghosthire.com

# Database
DB_NAME=ghosthire_db
DB_USER=ghosthire_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=3306

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret

# SerpAPI
SERPAPI_KEY=your-serpapi-key

# Media/Static
MEDIA_ROOT=/var/www/ghosthire/media
STATIC_ROOT=/var/www/ghosthire/static
```

### Production Settings

- Use gunicorn or uwsgi for WSGI server
- Configure nginx to serve static/media files
- Block public access to `/media/verification_photos/`
- Enable HTTPS with SSL certificate
- Set up database connection pooling
- Configure Redis for session storage (optional)
- Set up Celery for async tasks (SerpAPI calls, Siamese inference)

### Model File Deployment

- Include `best_siamese_model.pth` in deployment package
- Store in project root or dedicated `ml_models/` directory
- Ensure file permissions allow Django process to read
- Consider model versioning for future updates
