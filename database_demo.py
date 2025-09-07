#!/usr/bin/env python3
"""
Database Demo Script for VenueRate
Shows practical examples of database operations
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'venue_rating_system.settings')
django.setup()

from venues.models import Venue, Category, Rating, VenueImage, Statistics
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Max, Min

def demo_basic_queries():
    """Demonstrate basic database queries"""
    print("🔍 BASIC DATABASE QUERIES")
    print("=" * 50)
    
    # Count records
    print(f"Total Categories: {Category.objects.count()}")
    print(f"Total Venues: {Venue.objects.count()}")
    print(f"Total Ratings: {Rating.objects.count()}")
    print(f"Total Users: {User.objects.count()}")
    
    # List all categories
    print("\n📂 Categories:")
    for category in Category.objects.all():
        venue_count = category.venues.count()
        print(f"  - {category.name}: {venue_count} venues")
    
    # List all venues
    print("\n🏢 Venues:")
    for venue in Venue.objects.all()[:5]:  # Show first 5
        print(f"  - {venue.name} ({venue.category.name}) - {venue.city}")
        print(f"    Rating: {venue.average_rating}/5 ({venue.total_ratings} reviews)")
        print(f"    Active: {venue.is_active}, Featured: {venue.is_featured}")
        print()

def demo_filtering():
    """Demonstrate filtering and searching"""
    print("🔍 FILTERING AND SEARCHING")
    print("=" * 50)
    
    # Filter by category
    hotels = Venue.objects.filter(category__name='Hotels')
    print(f"Hotels found: {hotels.count()}")
    
    # Filter by status
    active_venues = Venue.objects.filter(is_active=True)
    featured_venues = Venue.objects.filter(is_featured=True)
    print(f"Active venues: {active_venues.count()}")
    print(f"Featured venues: {featured_venues.count()}")
    
    # Filter by rating
    high_rated = Venue.objects.filter(average_rating__gte=4.0)
    print(f"High-rated venues (4+ stars): {high_rated.count()}")
    
    # Search by name
    search_term = "hotel"
    search_results = Venue.objects.filter(name__icontains=search_term)
    print(f"Venues containing '{search_term}': {search_results.count()}")
    
    # Filter by city
    cities = Venue.objects.values_list('city', flat=True).distinct()
    print(f"Cities with venues: {list(cities)}")

def demo_aggregations():
    """Demonstrate aggregations and statistics"""
    print("📊 AGGREGATIONS AND STATISTICS")
    print("=" * 50)
    
    # Basic statistics
    stats = Venue.objects.aggregate(
        total_venues=Count('id'),
        avg_rating=Avg('average_rating'),
        max_rating=Max('average_rating'),
        min_rating=Min('average_rating')
    )
    
    print(f"Total Venues: {stats['total_venues']}")
    print(f"Average Rating: {stats['avg_rating']:.2f}")
    print(f"Highest Rating: {stats['max_rating']}")
    print(f"Lowest Rating: {stats['min_rating']}")
    
    # Venues by category
    print("\n📂 Venues by Category:")
    category_stats = Venue.objects.values('category__name').annotate(
        count=Count('id'),
        avg_rating=Avg('average_rating')
    ).order_by('-count')
    
    for stat in category_stats:
        print(f"  - {stat['category__name']}: {stat['count']} venues (avg: {stat['avg_rating']:.1f})")
    
    # Top rated venues
    print("\n⭐ Top Rated Venues:")
    top_rated = Venue.objects.filter(
        average_rating__isnull=False
    ).order_by('-average_rating', '-total_ratings')[:3]
    
    for venue in top_rated:
        print(f"  - {venue.name}: {venue.average_rating}/5 ({venue.total_ratings} reviews)")

def demo_creating_data():
    """Demonstrate creating new data"""
    print("➕ CREATING NEW DATA")
    print("=" * 50)
    
    # Create a new category
    new_category, created = Category.objects.get_or_create(
        name='Museums',
        defaults={'description': 'Museums and cultural attractions'}
    )
    if created:
        print(f"✅ Created new category: {new_category.name}")
    else:
        print(f"ℹ️  Category already exists: {new_category.name}")
    
    # Create a new venue
    try:
        new_venue = Venue.objects.create(
            name="Louvre Museum",
            description="World's largest art museum and historic monument",
            category=new_category,
            address="Rue de Rivoli, 75001 Paris",
            city="Paris",
            country="France",
            phone="+33 1 40 20 50 50",
            email="info@louvre.fr",
            website="https://www.louvre.fr",
            price_range_min=15.00,
            price_range_max=17.00,
            currency="EUR",
            facilities="Audio guides, Gift shop, Restaurant, WiFi",
            languages_spoken="French, English, Spanish, Italian",
            is_active=True,
            is_featured=True
        )
        print(f"✅ Created new venue: {new_venue.name}")
        print(f"   Slug: {new_venue.slug}")
        print(f"   Category: {new_venue.category.name}")
        
    except Exception as e:
        print(f"❌ Error creating venue: {e}")

def demo_updating_data():
    """Demonstrate updating data"""
    print("✏️  UPDATING DATA")
    print("=" * 50)
    
    # Update a venue
    try:
        venue = Venue.objects.filter(name__icontains='louvre').first()
        if venue:
            old_rating = venue.average_rating
            venue.average_rating = 4.8
            venue.total_ratings = 15000
            venue.save()
            print(f"✅ Updated {venue.name}")
            print(f"   Rating: {old_rating} → {venue.average_rating}")
        else:
            print("ℹ️  No Louvre venue found to update")
    except Exception as e:
        print(f"❌ Error updating venue: {e}")
    
    # Bulk update
    updated_count = Venue.objects.filter(is_active=False).update(is_active=True)
    if updated_count > 0:
        print(f"✅ Activated {updated_count} inactive venues")

def demo_relationships():
    """Demonstrate working with relationships"""
    print("🔗 WORKING WITH RELATIONSHIPS")
    print("=" * 50)
    
    # Get venues with their categories
    venues_with_categories = Venue.objects.select_related('category').all()[:3]
    print("Venues with categories:")
    for venue in venues_with_categories:
        print(f"  - {venue.name} → {venue.category.name}")
    
    # Get categories with venue counts
    categories_with_counts = Category.objects.annotate(
        venue_count=Count('venues')
    ).order_by('-venue_count')
    
    print("\nCategories with venue counts:")
    for category in categories_with_counts:
        print(f"  - {category.name}: {category.venue_count} venues")
    
    # Get venues with images
    venues_with_images = Venue.objects.filter(images__isnull=False).distinct()
    print(f"\nVenues with images: {venues_with_images.count()}")

def demo_advanced_queries():
    """Demonstrate advanced queries"""
    print("🚀 ADVANCED QUERIES")
    print("=" * 50)
    
    # Complex filtering
    complex_query = Venue.objects.filter(
        is_active=True,
        average_rating__gte=4.0,
        price_range_max__lte=200
    ).exclude(city='London').order_by('-average_rating')
    
    print(f"Active, high-rated, affordable venues (excluding London): {complex_query.count()}")
    
    # Date-based queries
    from datetime import datetime, timedelta
    recent_venues = Venue.objects.filter(
        created_at__gte=datetime.now() - timedelta(days=30)
    )
    print(f"Venues created in last 30 days: {recent_venues.count()}")
    
    # Text search
    search_terms = ['hotel', 'restaurant', 'cafe']
    for term in search_terms:
        count = Venue.objects.filter(name__icontains=term).count()
        print(f"Venues containing '{term}': {count}")

def demo_database_management():
    """Demonstrate database management tasks"""
    print("🛠️  DATABASE MANAGEMENT")
    print("=" * 50)
    
    # Update statistics
    print("Updating venue statistics...")
    for venue in Venue.objects.all():
        venue.update_rating_stats()
    
    print("✅ Venue statistics updated")
    
    # Check for data integrity
    venues_without_slugs = Venue.objects.filter(slug__isnull=True) | Venue.objects.filter(slug='')
    print(f"Venues without slugs: {venues_without_slugs.count()}")
    
    venues_without_categories = Venue.objects.filter(category__isnull=True)
    print(f"Venues without categories: {venues_without_categories.count()}")
    
    # Clean up inactive venues (just show count, don't actually delete)
    inactive_venues = Venue.objects.filter(is_active=False)
    print(f"Inactive venues: {inactive_venues.count()}")

def main():
    """Run all demonstrations"""
    print("🗄️  VENUERATE DATABASE DEMONSTRATION")
    print("=" * 60)
    print("This script demonstrates various database operations")
    print("You can run individual functions or the entire demo")
    print()
    
    try:
        demo_basic_queries()
        print("\n" + "="*60 + "\n")
        
        demo_filtering()
        print("\n" + "="*60 + "\n")
        
        demo_aggregations()
        print("\n" + "="*60 + "\n")
        
        demo_creating_data()
        print("\n" + "="*60 + "\n")
        
        demo_updating_data()
        print("\n" + "="*60 + "\n")
        
        demo_relationships()
        print("\n" + "="*60 + "\n")
        
        demo_advanced_queries()
        print("\n" + "="*60 + "\n")
        
        demo_database_management()
        
        print("\n🎉 DATABASE DEMONSTRATION COMPLETE!")
        print("\nNext steps:")
        print("1. Run 'python manage.py shell' for interactive database access")
        print("2. Visit http://127.0.0.1:8000/admin/ for web-based management")
        print("3. Check DATABASE_GUIDE.md for detailed documentation")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
