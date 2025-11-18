# 🚀 Ghost Hire - Quick Start

## Prerequisites Check

Before starting, make sure you have:
- ✅ Python 3.9+ installed
- ✅ MySQL 8.x installed and running
- ✅ pip installed

## 5-Minute Setup

### Step 1: Create Database (2 minutes)

Open Command Prompt and run:
```bash
mysql -u root -p
```

Enter your MySQL password, then:
```sql
CREATE DATABASE ghosthire_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### Step 2: Configure Environment (1 minute)

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Open `.env` in a text editor and update:
   ```env
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   ```

   (You already have WorkOS credentials in the file - great! Leave SerpAPI for now)

### Step 3: Run Migrations (1 minute)

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Admin User (1 minute)

```bash
python manage.py createsuperuser
```

Enter:
- Email: your@email.com
- Username: admin
- Password: (your choice)

### Step 5: Start Server

```bash
python manage.py runserver
```

### Step 6: Visit the Site

Open your browser:
```
http://localhost:8000
```

## 🎉 You're Done!

The basic site is now running. You'll see:
- ✅ Homepage with "Rise from the Grave" button
- ✅ Haunted theme with neon effects
- ✅ Spooky animations

## ✅ WorkOS SSO Ready!

Your `.env` file already has WorkOS credentials configured! The "Rise from the Grave" button should work.

**WorkOS Configuration:**
- Client ID: `client_01K9KSPA3JEWWA2R99437QVPEQ`
- API Key: Already configured
- Redirect URI: `http://localhost:8000/auth/callback/`

Make sure this redirect URI is added in your WorkOS Dashboard under "Redirects".

## 🔧 Testing the Full Flow

1. Click "Rise from the Grave" on homepage
2. WorkOS will handle the authentication
3. After login, you'll be redirected to verification page
4. Upload a photo to verify
5. Complete your profile setup
6. View your haunted profile!

## 📝 Optional Enhancements

### Add Default Ghost Avatar

Create or download a ghost image (200x200px) and save as:
```
media/ghost_avatars/1.png
```

### Add Siamese Model (for face verification)

If you have the trained model file:
```
Place: best_siamese_model.pth in project root
```

### Add SerpAPI Key (for reverse image search)

Sign up at https://serpapi.com/ and add key to `.env`:
```env
SERPAPI_KEY=your_key_here
```

## 🆘 Troubleshooting

### "No module named 'MySQLdb'"
```bash
pip install mysqlclient
```

### "Access denied for user"
Check your MySQL password in `.env`

### "Can't connect to MySQL server"
Make sure MySQL is running:
```bash
# Windows
net start MySQL80
```

### Static files not loading
```bash
python manage.py collectstatic --noinput
```

## 📚 Full Documentation

For complete setup and deployment guide, see:
- `README.md` - Full documentation
- `setup_instructions.md` - Detailed setup
- `PROJECT_SUMMARY.md` - What's been built

## 🎃 Happy Haunting!

Your Ghost Hire platform is ready to haunt the tech industry! 👻
