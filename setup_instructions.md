# Ghost Hire - Quick Setup Guide

## Step-by-Step Setup

### 1. Install Dependencies (Already Done ✅)
```bash
pip install -r requirements.txt
```

### 2. Create MySQL Database

Open MySQL command line:
```bash
mysql -u root -p
```

Create the database:
```sql
CREATE DATABASE ghosthire_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 3. Create .env File

Copy `.env.example` to `.env` and fill in your values:
```bash
copy .env.example .env  # Windows
```

Edit `.env` with your actual values:
- Set your MySQL credentials (DB_USER, DB_PASSWORD)
- Add Google OAuth credentials (get from Google Cloud Console)
- Add SerpAPI key (optional, for reverse image search)

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 6. Add Default Ghost Avatar

Create or download a ghost image and save it as:
```
media/ghost_avatars/1.png
```

You can use any ghost emoji or icon (200x200px recommended).

### 7. Configure WorkOS SSO

1. Go to https://dashboard.workos.com/
2. Select your project
3. Go to "Configuration" → "Redirects"
4. Add redirect URIs:
   - `http://localhost:8000/auth/callback/`
   - `http://127.0.0.1:8000/auth/callback/`
5. Your Client ID and API Key are already in `.env` - you're all set!

### 8. Run the Development Server

```bash
python manage.py runserver
```

### 9. Access the Application

Open your browser and go to:
```
http://localhost:8000
```

### 10. Test the Flow

1. Click "Rise from the Grave" to sign up with Google
2. After OAuth, you'll be redirected to verification page
3. Upload a verification photo
4. Complete your profile setup
5. View your ghost profile!

## Troubleshooting

### MySQL Connection Error
- Make sure MySQL is running
- Check your DB credentials in `.env`
- Verify the database exists: `SHOW DATABASES;` in MySQL

### WorkOS SSO Not Working
- Check your Client ID and API Key in `.env`
- Verify redirect URIs in WorkOS Dashboard
- Make sure you're using the exact URLs (localhost vs 127.0.0.1)
- Check WorkOS logs in the dashboard for error details

### Missing Siamese Model
- The app will work without it (duplicate detection will be skipped)
- If you have the model file, place it in project root as `best_siamese_model.pth`

### Static Files Not Loading
- Make sure you're running the development server
- Check that `static/` directory exists
- Try: `python manage.py collectstatic --noinput`

## Admin Panel

Access the admin panel at:
```
http://localhost:8000/admin/
```

Login with your superuser credentials.

## Next Steps

- Customize the haunted theme colors in `static/css/haunted.css`
- Add more skills in `haunted_profiles/forms.py`
- Implement the SerpAPI integration in `haunted_profiles/utils.py`
- Add the trained Siamese model for face verification

Happy Haunting! 👻
