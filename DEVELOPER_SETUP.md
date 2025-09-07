# 🚀 Developer Setup Guide - TourInsight

This guide will help your friend set up the TourInsight project locally for development.

## 📋 Prerequisites

Before starting, make sure you have:

- **Python 3.8+** installed
- **Git** installed
- **pip** (Python package installer)
- **Code editor** (VS Code, PyCharm, etc.)

### Windows-Specific Notes:
- **Command Prompt**: Use Command Prompt or PowerShell
- **Python**: Make sure Python is added to PATH during installation
- **Git**: Download from [git-scm.com](https://git-scm.com/download/win)
- **VS Code**: Recommended editor with Python extension

## 🔧 Step-by-Step Setup

### 1. Clone the Repository

**For Windows users:**
```cmd
# Navigate to your desired directory (Desktop is perfect!)
cd %USERPROFILE%\Desktop

# Clone the repository
git clone https://github.com/Hamza-spc/RateWebsite.git
cd RateWebsite
```

**For macOS/Linux users:**
```bash
# Navigate to your desired directory (Desktop is perfect!)
cd ~/Desktop

# Clone the repository
git clone https://github.com/Hamza-spc/RateWebsite.git
cd RateWebsite
```

**Note:** Your friend can clone the project anywhere they want:
- **Windows**: `%USERPROFILE%\Desktop` or `C:\Users\[username]\Desktop`
- **macOS/Linux**: `~/Desktop` or `~/Documents` or `~/Projects`

### 2. Create Virtual Environment

**For Windows users:**
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**For macOS/Linux users:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

```bash
# Copy environment template
cp env_example.txt .env

# Edit the .env file with your settings
# For basic development, you can leave most fields empty
```

**Minimum .env configuration for development:**

```env
# Django Secret Key (generate a new one)
SECRET_KEY=django-insecure-your-secret-key-here

# Debug mode (keep True for development)
DEBUG=True

# Database (SQLite is fine for development)
# No additional DB config needed for SQLite

# Google OAuth (optional - leave empty if not needed)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
```

### 5. Database Setup

```bash
# Run migrations to create database tables
python manage.py migrate

# Create a superuser (admin account)
python manage.py createsuperuser
# Follow prompts to create admin username, email, and password
```

### 6. Load Sample Data (Optional)

```bash
# Add some sample venues for testing
python manage.py shell
```

In the Python shell:

```python
from venues.models import Category, Venue

# Create categories
categories = [
    'Hotels', 'Restaurants', 'Cafes', 'Amusement Parks',
    'Museums', 'Shopping Centers', 'Beaches', 'Mountains'
]

for cat_name in categories:
    Category.objects.get_or_create(name=cat_name)

# Create sample venues
sample_venues = [
    {
        'name': 'Grand Hotel Paris',
        'category': 'Hotels',
        'description': 'Luxury hotel in the heart of Paris',
        'address': '123 Champs-Élysées, Paris',
        'city': 'Paris',
        'country': 'France',
        'phone': '+33 1 23 45 67 89',
        'email': 'info@grandhotelparis.com',
        'website': 'https://grandhotelparis.com',
        'price_range_min': 200.00,
        'price_range_max': 500.00,
        'currency': 'EUR',
        'is_active': True,
        'is_featured': True
    },
    {
        'name': 'Bella Vista Restaurant',
        'category': 'Restaurants',
        'description': 'Fine dining with panoramic city views',
        'address': '456 Main Street, New York',
        'city': 'New York',
        'country': 'USA',
        'phone': '+1 555 123 4567',
        'email': 'reservations@bellavista.com',
        'website': 'https://bellavista.com',
        'price_range_min': 50.00,
        'price_range_max': 150.00,
        'currency': 'USD',
        'is_active': True,
        'is_featured': True
    },
    {
        'name': 'Coffee Corner',
        'category': 'Cafes',
        'description': 'Cozy coffee shop with artisanal brews',
        'address': '789 Oak Avenue, London',
        'city': 'London',
        'country': 'UK',
        'phone': '+44 20 7123 4567',
        'email': 'hello@coffeecorner.co.uk',
        'website': 'https://coffeecorner.co.uk',
        'price_range_min': 5.00,
        'price_range_max': 25.00,
        'currency': 'GBP',
        'is_active': True,
        'is_featured': False
    }
]

for venue_data in sample_venues:
    category = Category.objects.get(name=venue_data['category'])
    venue_data['category'] = category
    Venue.objects.get_or_create(
        name=venue_data['name'],
        defaults=venue_data
    )

print("Sample data created successfully!")
exit()
```

### 7. Start Development Server

```bash
python manage.py runserver
```

### 8. Access the Application

Open your browser and go to:

- **Main site**: http://127.0.0.1:8000
- **Admin panel**: http://127.0.0.1:8000/admin/
- **Admin dashboard**: http://127.0.0.1:8000/admin-dashboard/

## 🎯 What Your Friend Can Do Now

### **Immediate Testing:**

1. **Browse venues** on the homepage
2. **Search for venues** using the search bar
3. **View venue details** by clicking on any venue
4. **Create user account** at `/accounts/signup/`
5. **Rate venues** (requires login)
6. **Access admin panel** with superuser account

### **Development Features:**

1. **Add new venues** via admin dashboard
2. **Manage categories** and venue information
3. **View user ratings** and reviews
4. **Test the star rating system**
5. **Customize templates** and styling

## 🔧 Development Workflow

### **Making Changes:**

1. **Edit code** in your preferred editor
2. **Test changes** by refreshing the browser
3. **Commit changes** to Git:
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```

### **Database Changes:**

If you modify models:

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### **Static Files:**

If you add CSS/JS/images:

```bash
# Collect static files
python manage.py collectstatic
```

## 🐛 Troubleshooting

### **Common Issues:**

**1. Port already in use:**

```bash
# Use different port
python manage.py runserver 8001
```

**2. Database errors:**

```bash
# Reset database (development only)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

**3. Import errors:**

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

**4. Permission errors:**

```bash
# Fix file permissions (macOS/Linux)
chmod +x manage.py
```

## 📁 Project Structure Overview

```
TourInsight/
├── accounts/                 # User authentication
├── venues/                   # Main app (venues, ratings, reviews)
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Django forms
│   ├── urls.py              # URL patterns
│   └── templates/           # HTML templates
├── templates/               # Base templates
├── static/                  # Static files (CSS, JS, images)
├── tour_insight_system/     # Project settings
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## 🎨 Customization Guide

### **Adding New Features:**

1. **Create new models** in `venues/models.py`
2. **Add views** in `venues/views.py`
3. **Create templates** in `venues/templates/`
4. **Update URLs** in `venues/urls.py`

### **Styling Changes:**

- **CSS**: Edit templates or add to `static/` folder
- **Tailwind**: Already included via CDN
- **Custom styles**: Add to template `<style>` blocks

### **Database Changes:**

- **New fields**: Add to models, create migrations
- **New models**: Create in models.py, migrate
- **Relationships**: Use ForeignKey, ManyToMany, etc.

## 🚀 Next Steps

Once set up, your friend can:

1. **Explore the codebase** to understand the structure
2. **Add new features** like user profiles, favorites, etc.
3. **Improve the UI** with custom styling
4. **Add new venue types** or categories
5. **Implement advanced search** filters
6. **Add image uploads** for venues
7. **Create mobile app** using the same backend

## 📞 Support

If your friend encounters issues:

1. **Check this guide** first
2. **Read the README.md** for additional info
3. **Check Django documentation** for specific features
4. **Create GitHub issues** for bugs or questions

---

**Happy coding!** 🎉 Your friend is now ready to contribute to the TourInsight project!
