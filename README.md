# 👻 Ghost Hire - Haunted Hiring Platform

Where Dead Careers Come to Life! A spooky-themed hiring platform for self-taught developers to prove their skills without degrees.

## 🎃 Features

- **Google OAuth Authentication**: Sign up with your Google account
- **AI-Powered Verification**: Photo verification with fraud detection using:
  - Reverse image search (SerpAPI)
  - Siamese neural network for duplicate face detection
- **Haunted Profile System**: Create your ghost profile with skills, bio, and custom avatar
- **Spooky UI**: Neon purple and green theme with horror-inspired animations
- **Secure**: Private verification photos, public ghost avatars

## 🛠️ Tech Stack

- **Backend**: Django 4.2
- **Database**: MySQL 8.x
- **Authentication**: WorkOS SSO
- **AI/ML**: PyTorch + torchvision (Siamese Network)
- **Image Processing**: Pillow
- **API**: SerpAPI for reverse image search
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## 📦 Installation

### 1. Prerequisites

- Python 3.9+
- MySQL 8.x
- pip

### 2. Clone and Setup

```bash
cd ghosthire
pip install -r requirements.txt
