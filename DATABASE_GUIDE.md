# 🗄️ VenueRate Database Guide

## Overview

Your VenueRate application uses Django's ORM with SQLite (development) and PostgreSQL (production). Here's how to interact with your database effectively.

## 📊 Database Structure

### Models Available:

- **Category**: Venue categories (Hotels, Restaurants, Cafes, Amusement Parks)
- **Venue**: Main venue information
- **VenueImage**: Images for venues
- **Rating**: User ratings and reviews
- **UserProfile**: Extended user information
- **ContactMessage**: Contact form submissions
- **Statistics**: Aggregated statistics

## 🛠️ Ways to Use the Database

### 1. Django Admin Interface (Web-based)

**URL**: http://127.0.0.1:8000/admin/
**Login**: matine@admin.com / wlan24dca7

**Features:**

- Visual interface for all models
- Add, edit, delete records
- Bulk operations
- Image management
- User management

### 2. Django Shell (Command Line)

**Access**: `python manage.py shell`

**Common Commands:**

```python
# Import models
from venues.models import Venue, Category, Rating
from accounts.models import UserProfile

# View all venues
venues = Venue.objects.all()
for venue in venues:
    print(f"{venue.name} - {venue.category.name} - {venue.city}")

# Filter venues
hotels = Venue.objects.filter(category__name='Hotels')
active_venues = Venue.objects.filter(is_active=True)

# Create new venue
new_venue = Venue.objects.create(
    name="New Hotel",
    description="A great hotel",
    category=Category.objects.get(name='Hotels'),
    address="123 Main St",
    city="New York",
    country="USA"
)
```

### 3. Django Management Commands

**Custom commands available:**

- `python manage.py fix_venue_slugs` - Fix empty slugs
- `python manage.py add_sample_images` - Add sample images

### 4. Direct SQL (Advanced)

**Access**: `python manage.py dbshell`

## 📈 Database Operations Guide

### Adding Data

#### 1. Add Categories

```python
# Via Django Shell
from venues.models import Category

categories = [
    'Hotels', 'Restaurants', 'Cafes', 'Amusement Parks',
    'Museums', 'Parks', 'Shopping Centers'
]

for cat_name in categories:
    Category.objects.get_or_create(name=cat_name)
    print(f"Created/Found category: {cat_name}")
```

#### 2. Add Venues

```python
# Via Django Shell
from venues.models import Venue, Category

# Get category
hotel_category = Category.objects.get(name='Hotels')

# Create venue
venue = Venue.objects.create(
    name="Grand Hotel Paris",
    slug="grand-hotel-paris",  # Auto-generated if empty
    description="Luxury hotel in the heart of Paris",
    category=hotel_category,
    address="123 Champs-Élysées",
    city="Paris",
    country="France",
    phone="+33 1 23 45 67 89",
    email="info@grandhotelparis.com",
    website="https://grandhotelparis.com",
    price_range_min=200.00,
    price_range_max=500.00,
    currency="EUR",
    facilities="WiFi, Pool, Spa, Restaurant",
    languages_spoken="French, English, Spanish",
    is_active=True,
    is_featured=True
)
```

#### 3. Add Images

```python
# Via Django Shell
from venues.models import VenueImage
from django.core.files import File

venue = Venue.objects.get(name="Grand Hotel Paris")

# Add image (you need actual image files)
# VenueImage.objects.create(
#     venue=venue,
#     image=File(open('path/to/image.jpg', 'rb')),
#     caption="Hotel exterior",
#     is_primary=True,
#     order=1
# )
```

#### 4. Add Ratings

```python
# Via Django Shell
from venues.models import Rating
from django.contrib.auth.models import User

venue = Venue.objects.get(name="Grand Hotel Paris")
user = User.objects.get(email="matine@admin.com")

rating = Rating.objects.create(
    venue=venue,
    user=user,
    rating=5,
    comment="Excellent hotel with great service!"
)
```

### Querying Data

#### 1. Basic Queries

```python
# All venues
all_venues = Venue.objects.all()

# Active venues only
active_venues = Venue.objects.filter(is_active=True)

# Featured venues
featured_venues = Venue.objects.filter(is_featured=True)

# Venues by category
hotels = Venue.objects.filter(category__name='Hotels')

# Venues by city
paris_venues = Venue.objects.filter(city='Paris')

# High-rated venues (4+ stars)
high_rated = Venue.objects.filter(average_rating__gte=4.0)
```

#### 2. Advanced Queries

```python
# Venues with images
venues_with_images = Venue.objects.filter(images__isnull=False).distinct()

# Most reviewed venues
most_reviewed = Venue.objects.order_by('-total_ratings')[:10]

# Recent venues
recent_venues = Venue.objects.order_by('-created_at')[:5]

# Search by name
search_results = Venue.objects.filter(name__icontains='hotel')

# Price range
budget_venues = Venue.objects.filter(
    price_range_min__lte=100,
    price_range_max__gte=50
)
```

#### 3. Aggregations

```python
from django.db.models import Count, Avg, Max, Min

# Statistics
total_venues = Venue.objects.count()
avg_rating = Venue.objects.aggregate(avg_rating=Avg('average_rating'))
max_price = Venue.objects.aggregate(max_price=Max('price_range_max'))

# Venues by category count
category_counts = Venue.objects.values('category__name').annotate(
    count=Count('id')
).order_by('-count')

# Top rated venues
top_rated = Venue.objects.filter(
    average_rating__gte=4.0
).order_by('-average_rating', '-total_ratings')
```

### Updating Data

#### 1. Update Single Record

```python
# Update venue
venue = Venue.objects.get(name="Grand Hotel Paris")
venue.description = "Updated description"
venue.is_featured = True
venue.save()

# Update rating
rating = Rating.objects.get(id=1)
rating.rating = 4
rating.comment = "Updated review"
rating.save()
```

#### 2. Bulk Updates

```python
# Activate all venues
Venue.objects.update(is_active=True)

# Update all hotel prices
Venue.objects.filter(category__name='Hotels').update(
    currency='USD'
)

# Deactivate old venues
from datetime import datetime, timedelta
old_date = datetime.now() - timedelta(days=365)
Venue.objects.filter(created_at__lt=old_date).update(
    is_active=False
)
```

### Deleting Data

#### 1. Delete Single Record

```python
# Delete venue (cascades to images and ratings)
venue = Venue.objects.get(name="Old Hotel")
venue.delete()

# Delete rating
rating = Rating.objects.get(id=1)
rating.delete()
```

#### 2. Bulk Deletes

```python
# Delete inactive venues
Venue.objects.filter(is_active=False).delete()

# Delete old ratings
from datetime import datetime, timedelta
old_date = datetime.now() - timedelta(days=365)
Rating.objects.filter(created_at__lt=old_date).delete()
```

## 🔧 Database Maintenance

### 1. Backup Database

```bash
# SQLite backup
cp db.sqlite3 db_backup_$(date +%Y%m%d).sqlite3

# PostgreSQL backup (production)
pg_dump -h localhost -U username -d venuerate_db > backup.sql
```

### 2. Reset Database

```bash
# Delete database and recreate
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### 3. Update Statistics

```python
# Update all venue statistics
from venues.models import Venue

for venue in Venue.objects.all():
    venue.update_rating_stats()
    venue.save()
```

## 📊 Useful Queries for Analytics

### 1. Popular Categories

```python
from django.db.models import Count

popular_categories = Venue.objects.values('category__name').annotate(
    venue_count=Count('id')
).order_by('-venue_count')
```

### 2. Revenue Analysis

```python
# Average prices by category
price_analysis = Venue.objects.values('category__name').annotate(
    avg_min_price=Avg('price_range_min'),
    avg_max_price=Avg('price_range_max')
)
```

### 3. User Engagement

```python
# Most active reviewers
active_reviewers = User.objects.annotate(
    review_count=Count('rating')
).order_by('-review_count')[:10]
```

## 🚀 Production Database (PostgreSQL)

### Setup

```bash
# Install PostgreSQL
# Create database
createdb venuerate_db

# Update settings
# Use settings_production.py
python manage.py migrate --settings=venue_rating_system.settings_production
```

### Environment Variables

```bash
# .env file
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://username:password@localhost:5432/venuerate_db
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

## 🎯 Quick Start Commands

```bash
# Start development server
python manage.py runserver

# Access admin
open http://127.0.0.1:8000/admin/

# Open Django shell
python manage.py shell

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (production)
python manage.py collectstatic
```

## 📝 Best Practices

1. **Always use Django ORM** instead of raw SQL
2. **Use transactions** for multiple related operations
3. **Index frequently queried fields**
4. **Backup regularly** before major changes
5. **Use select_related()** and **prefetch_related()** for performance
6. **Validate data** before saving
7. **Use get_or_create()** to avoid duplicates

## 🔍 Debugging

```python
# Enable SQL logging in settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

This guide covers everything you need to effectively use your VenueRate database! 🎉
