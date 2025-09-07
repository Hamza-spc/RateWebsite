#!/usr/bin/env python3
"""
Test script to verify authentication is working
"""

import requests
import sys

def test_homepage():
    """Test if homepage loads"""
    try:
        response = requests.get('http://127.0.0.1:8000/')
        if response.status_code == 200:
            print("✅ Homepage loads successfully")
            return True
        else:
            print(f"❌ Homepage failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on port 8000")
        return False

def test_login_page():
    """Test if login page loads"""
    try:
        response = requests.get('http://127.0.0.1:8000/accounts/login/')
        if response.status_code == 200:
            print("✅ Login page loads successfully")
            return True
        else:
            print(f"❌ Login page failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False

def test_signup_page():
    """Test if signup page loads"""
    try:
        response = requests.get('http://127.0.0.1:8000/accounts/signup/')
        if response.status_code == 200:
            print("✅ Signup page loads successfully")
            return True
        else:
            print(f"❌ Signup page failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False

def test_admin_page():
    """Test if admin page loads"""
    try:
        response = requests.get('http://127.0.0.1:8000/admin/')
        if response.status_code == 200 or response.status_code == 302:
            print("✅ Admin page loads successfully")
            return True
        else:
            print(f"❌ Admin page failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing VenueRate Authentication System")
    print("=" * 50)
    
    tests = [
        ("Homepage", test_homepage),
        ("Login Page", test_login_page),
        ("Signup Page", test_signup_page),
        ("Admin Page", test_admin_page),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Authentication system is working correctly.")
        print("\nNext steps:")
        print("1. Visit http://127.0.0.1:8000/ to see the homepage")
        print("2. Visit http://127.0.0.1:8000/accounts/signup/ to test signup")
        print("3. Visit http://127.0.0.1:8000/accounts/login/ to test login")
        print("4. Visit http://127.0.0.1:8000/admin/ to access admin panel")
    else:
        print("❌ Some tests failed. Please check the server logs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
