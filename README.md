# 👻 Ghost Hire - Haunted Hiring Platform

A spooky-themed hiring platform for self-taught developers to prove their skills.

---

## 🎃 Features

- **WorkOS SSO Authentication** - Sign up with Google, Microsoft, GitHub, or any provider
- **AI-Powered Verification** - Photo verification with fraud detection using:
  - Reverse image search (SerpAPI)
  - Siamese neural network for duplicate face detection (see [README_SIAMESE.md](README_SIAMESE.md))
  - Note: Photo verification disabled on Railway deployment (model too large)
- **Haunted Profile System** - Create your ghost profile with skills, bio, and custom avatar
- **Spooky UI** - Neon purple and green theme with horror-inspired animations
- **Secure** - Private verification photos, public ghost avatars

---

## 🛠️ Tech Stack

- **Backend**: Django 4.2
- **Database**: MySQL 8.x
- **Authentication**: WorkOS SSO
- **AI/ML**: PyTorch + torchvision (Siamese Network)
- **Image Processing**: Pillow
- **API**: SerpAPI for reverse image search
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

---

## 📦 Installation

### 1. Prerequisites

- Python 3.9+
- MySQL 8.x
- pip

### 2. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/tumblr-byte/Ghost-hire.git

# Navigate to project directory
cd ghosthire

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Then edit `.env` with your credentials:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=ghost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306

# WorkOS Authentication
WORKOS_CLIENT_ID=client_your_client_id_here
WORKOS_API_KEY=sk_test_your_api_key_here
WORKOS_REDIRECT_URI=http://localhost:8000/auth/callback/

# SerpAPI
SERPAPI_KEY=your_serpapi_key_here
```

### 4. Database Setup

```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE ghost CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Add Default Ghost Avatar

Place a default ghost avatar image at:

```
media/ghost_avatars/1.png
```

### 7. Add Siamese Model (Optional)

If you have the trained Siamese model, place it at:

```
best_siamese_model.pth
```

If not available, the system will skip duplicate face detection.

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit: **http://localhost:8000**

---

## 🔑 WorkOS SSO Setup

1. Go to [WorkOS Dashboard](https://dashboard.workos.com/)
2. Create a new project or select existing
3. Enable **AuthKit** (User Management)
4. Go to **Configuration** → **Redirects** and add:
   - `http://localhost:8000/auth/callback/`
   - `http://127.0.0.1:8000/auth/callback/`
5. Go to **API Keys** and copy your credentials
6. Add them to `.env`:

```env
WORKOS_CLIENT_ID=client_your_client_id_here
WORKOS_API_KEY=sk_test_your_api_key_here
WORKOS_REDIRECT_URI=http://localhost:8000/auth/callback/
```

For detailed setup instructions, see [WORKOS_TROUBLESHOOTING.md](WORKOS_TROUBLESHOOTING.md)

---

## 🔮 SerpAPI Setup

1. Sign up at [SerpAPI](https://serpapi.com/)
2. Get your API key from the dashboard
3. Add to `.env` file:

```env
SERPAPI_KEY=your_serpapi_key_here
```

---

## � Railway Dpeployment

### Quick Deploy to Railway

1. **Push your code to GitHub**
2. **Connect to Railway**:
   - Go to [Railway.app](https://railway.app/)
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your Ghost-hire repository
3. **Add MySQL Database**:
   - Click "New" → "Database" → "Add MySQL"
4. **Configure Environment Variables** in Railway dashboard
5. **Deploy!** Railway will automatically deploy your app

For detailed Railway deployment instructions, see [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)

### Alternative: Docker Deployment

If you prefer Docker, see [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📁 Project Structure

```
ghosthire/
├── ghosthire/              # Project settings
│   ├── settings.py         # Django configuration
│   ├── urls.py             # Main URL routing
│   └── wsgi.py             # WSGI application
├── haunted_profiles/       # Main app
│   ├── models.py           # User & data models
│   ├── views.py            # View logic
│   ├── auth_views.py       # WorkOS authentication
│   ├── forms.py            # Django forms
│   ├── utils.py            # Verification logic
│   ├── portfolio_analyzer.py  # GitHub analysis
│   ├── career_assessor.py  # AI career assessment
│   └── urls.py             # App URL routing
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── index.html          # Landing page
│   ├── verification.html   # Photo verification
│   ├── haunt_setup.html    # Profile setup
│   └── haunted_portfolio.html  # Portfolio display
├── static/                 # Static files
│   ├── css/
│   │   └── haunted.css     # Spooky styles
│   └── js/
├── media/                  # User uploads
│   ├── verification_photos/  # Private (blocked)
│   └── ghost_avatars/        # Public
├── Dockerfile              # Development Docker image
├── Dockerfile.prod         # Production Docker image
├── docker-compose.yml      # Docker Compose config
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
└── README.md               # This file
```

---

## 🎨 Haunted Terminology

- **Sign Up** → "Rise from the Grave"
- **Login** → "Enter the Crypt"
- **Dashboard** → "Your Haunted Lair"
- **Profile** → "Your Ghost"
- **Logout** → "Return to Shadows"

---

## 🔒 Security Notes

### Verification Photos

Verification photos are stored in `media/verification_photos/` and should **NEVER** be publicly accessible.

**In Production:**

Configure your web server (nginx/apache) to block access to this directory:

```nginx
# nginx example
location /media/verification_photos/ {
    deny all;
    return 404;
}
```

Only `ghost_avatars` should be publicly served.

### Environment Variables

- Never commit `.env` file (it's in `.gitignore`)
- Use `.env.example` as a template
- Rotate API keys regularly
- Use strong SECRET_KEY in production

---

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Use a strong `SECRET_KEY` (generate new one)
- [ ] Configure MySQL with proper credentials
- [ ] Set up static file serving (`collectstatic`)
- [ ] Block public access to `verification_photos`
- [ ] Use HTTPS (SSL certificate)
- [ ] Set up proper logging
- [ ] Configure backup strategy
- [ ] Set up monitoring

### Static Files

```bash
python manage.py collectstatic
```

### Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test haunted_profiles

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 📚 Documentation

- [Quick Start Guide](QUICKSTART.md)
- [Railway Deployment Guide](RAILWAY_DEPLOYMENT.md) ⭐
- [Deployment Notes](DEPLOYMENT_NOTES.md) - Railway optimizations
- [Deployment Checklist](DEPLOY_CHECKLIST.md)
- [Siamese Network Details](README_SIAMESE.md) - ML implementation
- [WorkOS Setup](WORKOS_TROUBLESHOOTING.md)
- [Docker Deployment](DEPLOYMENT.md) (Alternative)
- [WorkOS Migration](WORKOS_MIGRATION.md)

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is for educational purposes.

---

## 🎃 Happy Haunting!





