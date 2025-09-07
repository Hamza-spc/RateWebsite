#!/usr/bin/env python3
"""
Test script to verify the new admin interface
"""

import requests
import sys

def test_admin_dashboard():
    """Test if admin dashboard loads"""
    try:
        response = requests.get('http://127.0.0.1:8000/admin-dashboard/')
        if response.status_code == 200:
            print("✅ Admin Dashboard loads successfully")
            return True
        else:
            print(f"❌ Admin Dashboard failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on port 8000")
        return False

def test_hotels_category():
    """Test if hotels category page loads"""
    try:
        response = requests.get('http://127.0.0.1:8000/admin-dashboard/category/hotels/')
        if response.status_code == 200:
            print("✅ Hotels category page loads successfully")
            return True
        else:
            print(f"❌ Hotels category page failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False

def test_restaurants_category():
    """Test if restaurants category page loads"""
    try:
        response = requests.get('http://127.0.0.1:8000/admin-dashboard/category/restaurants/')
        if response.status_code == 200:
            print("✅ Restaurants category page loads successfully")
            return True
        else:
            print(f"❌ Restaurants category page failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False

def test_edit_venues():
    """Test if edit venues page loads"""
    try:
        response = requests.get('http://127.0.0.1:8000/admin-dashboard/category/hotels/edit/')
        if response.status_code == 200:
            print("✅ Edit venues page loads successfully")
            return True
        else:
            print(f"❌ Edit venues page failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False

def test_add_venue():
    """Test if add venue page loads"""
    try:
        response = requests.get('http://127.0.0.1:8000/admin-dashboard/add-venue/')
        if response.status_code == 200:
            print("✅ Add venue page loads successfully")
            return True
        else:
            print(f"❌ Add venue page failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing New Admin Interface")
    print("=" * 50)
    
    tests = [
        ("Admin Dashboard", test_admin_dashboard),
        ("Hotels Category", test_hotels_category),
        ("Restaurants Category", test_restaurants_category),
        ("Edit Venues", test_edit_venues),
        ("Add Venue", test_add_venue),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! New admin interface is working correctly.")
        print("\nAdmin Interface Features:")
        print("1. Category Selection Dashboard")
        print("2. View Places by Category (Database View)")
        print("3. Add New Places")
        print("4. Edit/Delete Places with Bulk Actions")
        print("\nAccess the admin interface at: http://127.0.0.1:8000/admin-dashboard/")
    else:
        print("❌ Some tests failed. Please check the server logs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
