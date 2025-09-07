# VenueRate Setup Guide

## 🚀 Quick Start (Development)

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Email: matine@admin.com
# Password: wlan24dca7
```

### 3. Add Sample Data

```bash
# Add sample venues and categories
python manage.py shell
# Run the sample data creation script from the previous setup
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## 🏗️ Production Setup

### 1. PostgreSQL Setup

#### Option A: Using the Setup Script

```bash
python setup_postgresql.py
```

#### Option B: Manual Setup

```bash
# Install PostgreSQL (macOS)
brew install postgresql@15
brew services start postgresql@15

# Create database and user
psql postgres
CREATE USER venuerate_user WITH PASSWORD 'your_secure_password';
CREATE DATABASE venuerate_db OWNER venuerate_user;
GRANT ALL PRIVILEGES ON DATABASE venuerate_db TO venuerate_user;
\q
```

### 2. Environment Configuration

```bash
# Copy environment template
cp env_example.txt .env

# Edit .env with your production values
nano .env
```

### 3. Production Deployment

```bash
# Run migrations
python manage.py migrate --settings=venue_rating_system.settings_production

# Collect static files
python manage.py collectstatic --settings=venue_rating_system.settings_production

# Create superuser
python manage.py createsuperuser --settings=venue_rating_system.settings_production

# Run production server
python manage.py runserver --settings=venue_rating_system.settings_production
```

## 🔧 Adding Venue Images

### Method 1: Through Admin Panel

1. Go to http://127.0.0.1:8000/admin/
2. Login with admin credentials
3. Navigate to Venues > Venues
4. Click on a venue
5. Scroll down to "Venue images" section
6. Add images and set primary image

### Method 2: Using Management Command

```bash
python manage.py add_sample_images --venue-slug sofitel-paris --image-path /path/to/image.jpg
```

### Method 3: Programmatically

```python
from venues.models import Venue, VenueImage
from django.core.files import File

venue = Venue.objects.get(slug='sofitel-paris')
with open('path/to/image.jpg', 'rb') as f:
    VenueImage.objects.create(
        venue=venue,
        image=File(f),
        caption="Beautiful hotel exterior",
        is_primary=True
    )
```

## 🔐 Authentication Setup

### Email/Password Authentication

✅ **Already configured and working!**

- Sign up: http://127.0.0.1:8000/accounts/signup/
- Sign in: http://127.0.0.1:8000/accounts/login/
- Password reset: http://127.0.0.1:8000/accounts/password/reset/

### Google OAuth Setup

1. **Create Google OAuth Credentials**

   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable Google+ API
   - Go to Credentials > Create Credentials > OAuth 2.0 Client ID
   - Set authorized redirect URIs:
     - `http://127.0.0.1:8000/accounts/google/login/callback/` (development)
     - `https://yourdomain.com/accounts/google/login/callback/` (production)

2. **Update Settings**

   ```python
   # In settings.py or settings_production.py
   SOCIALACCOUNT_PROVIDERS = {
       'google': {
           'SCOPE': ['profile', 'email'],
           'AUTH_PARAMS': {'access_type': 'online'},
           'OAUTH_PKCE_ENABLED': True,
           'APP': {
               'client_id': 'your-google-client-id',
               'secret': 'your-google-client-secret',
               'key': ''
           }
       }
   }
   ```

3. **Add to Admin Panel**
   - Go to http://127.0.0.1:8000/admin/
   - Navigate to Social Applications
   - Add new application:
     - Provider: Google
     - Name: Google
     - Client id: Your Google Client ID
     - Secret key: Your Google Client Secret
     - Sites: Select your site

## 📱 Features Overview

### For Users

- ✅ Browse venues by category
- ✅ Search venues by location and keywords
- ✅ View detailed venue information
- ✅ Rate and review venues
- ✅ User profiles and authentication
- ✅ Responsive design

### For Admins

- ✅ Admin dashboard with statistics
- ✅ Add/edit/delete venues
- ✅ Manage venue images
- ✅ View user reviews and ratings
- ✅ Contact message management

## 🐛 Troubleshooting

### Authentication Issues

- Check if email verification is disabled in settings
- Ensure allauth is properly configured
- Check browser console for JavaScript errors

### Database Issues

- Ensure PostgreSQL is running
- Check database credentials in .env
- Run migrations: `python manage.py migrate`

### Static Files Issues

- Run: `python manage.py collectstatic`
- Check STATIC_ROOT and STATIC_URL settings
- Ensure static files are served correctly

### Image Upload Issues

- Check MEDIA_ROOT and MEDIA_URL settings
- Ensure media directory has write permissions
- Check file size limits

## 📞 Support

If you encounter any issues:

1. Check the Django logs
2. Verify all environment variables are set
3. Ensure all dependencies are installed
4. Check database connectivity

## 🚀 Deployment Options

### Heroku

1. Install Heroku CLI
2. Create Procfile
3. Configure environment variables
4. Deploy

### DigitalOcean

1. Create droplet
2. Install Docker
3. Use docker-compose
4. Configure domain

### AWS/GCP

1. Use managed services
2. Configure load balancer
3. Set up CDN
4. Configure monitoring

---

**Happy coding! 🎉**
