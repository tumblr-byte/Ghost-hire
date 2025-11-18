# GhostHire Deployment Guide

## Docker Deployment

### Prerequisites
- Docker installed
- Docker Compose installed
- `.env` file configured (copy from `.env.example`)

### Development Deployment

1. **Build and run with Docker Compose:**
```bash
docker-compose up --build
```

2. **Access the application:**
- Web: http://localhost:8000
- MySQL: localhost:3306

3. **Stop the containers:**
```bash
docker-compose down
```

4. **Stop and remove volumes (clean slate):**
```bash
docker-compose down -v
```

### Production Deployment

1. **Update your `.env` file for production:**
```env
DEBUG=False
SECRET_KEY=your-secure-random-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_PASSWORD=strong-database-password
WORKOS_REDIRECT_URI=https://yourdomain.com/auth/callback/
```

2. **Build production image:**
```bash
docker build -f Dockerfile.prod -t ghosthire:latest .
```

3. **Run with production settings:**
```bash
docker run -d \
  --name ghosthire \
  -p 8000:8000 \
  --env-file .env \
  ghosthire:latest
```

### Docker Commands Reference

**View logs:**
```bash
docker-compose logs -f web
```

**Run Django commands:**
```bash
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
```

**Access Django shell:**
```bash
docker-compose exec web python manage.py shell
```

**Access MySQL:**
```bash
docker-compose exec db mysql -u root -p ghost
```

### Environment Variables

Required environment variables in `.env`:

- `SECRET_KEY` - Django secret key (generate a new one for production)
- `DEBUG` - Set to False in production
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `DB_NAME` - Database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database host (use 'db' for docker-compose)
- `DB_PORT` - Database port (default: 3306)
- `WORKOS_CLIENT_ID` - WorkOS client ID
- `WORKOS_API_KEY` - WorkOS API key
- `WORKOS_REDIRECT_URI` - WorkOS redirect URI
- `SERPAPI_KEY` - SerpAPI key

### Production Considerations

1. **Use a reverse proxy (nginx/traefik) for:**
   - SSL/TLS termination
   - Static file serving
   - Load balancing

2. **Security:**
   - Never commit `.env` file
   - Use strong passwords
   - Enable HTTPS in production
   - Set `SESSION_COOKIE_SECURE = True` in settings.py
   - Block public access to `/media/verification_photos/`

3. **Database:**
   - Use managed database service or separate DB server
   - Regular backups
   - Connection pooling

4. **Static & Media Files:**
   - Use cloud storage (S3, GCS) for media files
   - Use CDN for static files

5. **Monitoring:**
   - Set up logging
   - Monitor container health
   - Set up alerts

### Cloud Deployment Options

**AWS:**
- ECS/Fargate with RDS MySQL
- Elastic Beanstalk
- EC2 with Docker

**Google Cloud:**
- Cloud Run with Cloud SQL
- GKE (Kubernetes)
- Compute Engine with Docker

**Azure:**
- Container Instances with Azure Database for MySQL
- App Service
- AKS (Kubernetes)

**DigitalOcean:**
- App Platform
- Droplets with Docker

### Troubleshooting

**Container won't start:**
```bash
docker-compose logs web
```

**Database connection issues:**
- Check DB_HOST is set to 'db' in docker-compose
- Ensure database container is healthy
- Verify credentials in .env

**Static files not loading:**
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

**Permission issues:**
```bash
docker-compose exec web chown -R ghosthire:ghosthire /app/media
```
