#!/usr/bin/env python3
"""
Direct database viewer for VenueRate
Shows all data in a readable format
"""

import sqlite3
import os
from datetime import datetime

def connect_to_database():
    """Connect to the SQLite database"""
    db_path = 'db.sqlite3'
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # This allows column access by name
        return conn
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return None

def show_users(conn):
    """Display all users"""
    print("👥 USERS")
    print("=" * 60)
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            u.id, u.username, u.email, u.first_name, u.last_name, 
            u.is_staff, u.is_active, u.date_joined,
            p.is_admin, p.bio, p.location
        FROM auth_user u
        LEFT JOIN venues_userprofile p ON u.id = p.user_id
        ORDER BY u.id
    """)
    
    users = cursor.fetchall()
    
    if not users:
        print("No users found.")
        return
    
    for user in users:
        print(f"ID: {user['id']}")
        print(f"  Username: {user['username']}")
        print(f"  Email: {user['email']}")
        print(f"  Name: {user['first_name']} {user['last_name']}")
        print(f"  Staff: {'Yes' if user['is_staff'] else 'No'}")
        print(f"  Admin: {'Yes' if user['is_admin'] else 'No'}")
        print(f"  Active: {'Yes' if user['is_active'] else 'No'}")
        print(f"  Joined: {user['date_joined']}")
        if user['bio']:
            print(f"  Bio: {user['bio']}")
        if user['location']:
            print(f"  Location: {user['location']}")
        print()

def show_categories(conn):
    """Display all categories"""
    print("📂 CATEGORIES")
    print("=" * 60)
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.*, COUNT(v.id) as venue_count
        FROM venues_category c
        LEFT JOIN venues_venue v ON c.id = v.category_id
        GROUP BY c.id
        ORDER BY c.id
    """)
    
    categories = cursor.fetchall()
    
    for category in categories:
        print(f"ID: {category['id']}")
        print(f"  Name: {category['name']}")
        print(f"  Slug: {category['slug']}")
        print(f"  Description: {category['description']}")
        print(f"  Venues: {category['venue_count']}")
        print(f"  Created: {category['created_at']}")
        print()

def show_venues(conn):
    """Display all venues with details"""
    print("🏢 VENUES")
    print("=" * 60)
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            v.*, c.name as category_name,
            COUNT(r.id) as rating_count,
            AVG(r.rating) as avg_rating
        FROM venues_venue v
        JOIN venues_category c ON v.category_id = c.id
        LEFT JOIN venues_rating r ON v.id = r.venue_id
        GROUP BY v.id
        ORDER BY v.id
    """)
    
    venues = cursor.fetchall()
    
    for venue in venues:
        print(f"ID: {venue['id']}")
        print(f"  Name: {venue['name']}")
        print(f"  Slug: {venue['slug']}")
        print(f"  Category: {venue['category_name']}")
        print(f"  Location: {venue['city']}, {venue['country']}")
        print(f"  Address: {venue['address']}")
        print(f"  Phone: {venue['phone'] or 'N/A'}")
        print(f"  Email: {venue['email'] or 'N/A'}")
        print(f"  Website: {venue['website'] or 'N/A'}")
        print(f"  Price Range: {venue['price_range_min'] or 'N/A'} - {venue['price_range_max'] or 'N/A'} {venue['currency']}")
        print(f"  Rating: {venue['average_rating'] or 0:.1f}/5 ({venue['rating_count']} reviews)")
        print(f"  Active: {'Yes' if venue['is_active'] else 'No'}")
        print(f"  Featured: {'Yes' if venue['is_featured'] else 'No'}")
        print(f"  Created: {venue['created_at']}")
        print(f"  Updated: {venue['updated_at']}")
        print()

def show_ratings(conn):
    """Display all ratings"""
    print("⭐ RATINGS")
    print("=" * 60)
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            r.*, u.username, v.name as venue_name
        FROM venues_rating r
        JOIN auth_user u ON r.user_id = u.id
        JOIN venues_venue v ON r.venue_id = v.id
        ORDER BY r.created_at DESC
    """)
    
    ratings = cursor.fetchall()
    
    if not ratings:
        print("No ratings found.")
        return
    
    for rating in ratings:
        print(f"ID: {rating['id']}")
        print(f"  Venue: {rating['venue_name']}")
        print(f"  User: {rating['username']}")
        print(f"  Rating: {rating['rating']}/5")
        print(f"  Comment: {rating['comment'] or 'No comment'}")
        print(f"  Created: {rating['created_at']}")
        print()

def show_contact_messages(conn):
    """Display contact messages"""
    print("📧 CONTACT MESSAGES")
    print("=" * 60)
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM venues_contactmessage
        ORDER BY created_at DESC
    """)
    
    messages = cursor.fetchall()
    
    if not messages:
        print("No contact messages found.")
        return
    
    for message in messages:
        print(f"ID: {message['id']}")
        print(f"  Name: {message['name']}")
        print(f"  Email: {message['email']}")
        print(f"  Subject: {message['subject']}")
        print(f"  Message: {message['message']}")
        print(f"  Created: {message['created_at']}")
        print(f"  Read: {'Yes' if message['is_read'] else 'No'}")
        print()

def show_database_stats(conn):
    """Show database statistics"""
    print("📊 DATABASE STATISTICS")
    print("=" * 60)
    
    cursor = conn.cursor()
    
    # Count records
    tables = [
        ('Users', 'auth_user'),
        ('Categories', 'venues_category'),
        ('Venues', 'venues_venue'),
        ('Ratings', 'venues_rating'),
        ('Contact Messages', 'venues_contactmessage'),
        ('User Profiles', 'venues_userprofile')
    ]
    
    for table_name, table_id in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_id}")
            count = cursor.fetchone()[0]
            print(f"{table_name}: {count}")
        except:
            print(f"{table_name}: Error accessing table")
    
    print()
    
    # Database file size
    db_size = os.path.getsize('db.sqlite3')
    print(f"Database file size: {db_size:,} bytes ({db_size/1024:.1f} KB)")

def main():
    """Main function"""
    print("🗄️ VENUERATE DATABASE VIEWER")
    print("=" * 80)
    print(f"Database: db.sqlite3")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Connect to database
    conn = connect_to_database()
    if not conn:
        return
    
    try:
        # Show all data
        show_database_stats(conn)
        show_users(conn)
        show_categories(conn)
        show_venues(conn)
        show_ratings(conn)
        show_contact_messages(conn)
        
        print("✅ Database viewing complete!")
        
    except Exception as e:
        print(f"❌ Error viewing database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
