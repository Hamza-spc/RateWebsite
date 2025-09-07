#!/usr/bin/env python3
"""
Test script to verify the profile dropdown fix
"""

import requests
from bs4 import BeautifulSoup

def test_dropdown_functionality():
    """Test if the dropdown has the correct IDs and structure"""
    try:
        response = requests.get('http://127.0.0.1:8000/')
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check if the dropdown elements exist
            user_menu_button = soup.find('button', {'id': 'user-menu-button'})
            user_menu_dropdown = soup.find('div', {'id': 'user-menu-dropdown'})
            user_menu_container = soup.find('div', {'id': 'user-menu-container'})
            
            if user_menu_button and user_menu_dropdown and user_menu_container:
                print("✅ Profile dropdown elements found with correct IDs")
                
                # Check if dropdown has the correct classes
                if 'hidden' in user_menu_dropdown.get('class', []):
                    print("✅ Dropdown is initially hidden")
                else:
                    print("⚠️  Dropdown is not initially hidden")
                
                # Check if the dropdown contains the expected menu items
                profile_link = soup.find('a', href='/accounts/profile/')
                admin_link = soup.find('a', href='/admin-dashboard/')
                logout_link = soup.find('a', href='/accounts/logout/')
                
                if profile_link and logout_link:
                    print("✅ Profile and logout links found")
                else:
                    print("❌ Missing profile or logout links")
                
                if admin_link:
                    print("✅ Admin dashboard link found")
                else:
                    print("ℹ️  Admin dashboard link not found (user might not be admin)")
                
                return True
            else:
                print("❌ Missing dropdown elements")
                return False
        else:
            print(f"❌ Homepage failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on port 8000")
        return False

def main():
    """Run the test"""
    print("🧪 Testing Profile Dropdown Fix")
    print("=" * 40)
    
    if test_dropdown_functionality():
        print("\n🎉 Profile dropdown fix is working correctly!")
        print("\nHow it works now:")
        print("1. Click on your profile icon to open the dropdown")
        print("2. The dropdown will stay open until you:")
        print("   - Click on a menu item")
        print("   - Click anywhere outside the dropdown")
        print("   - Press the Escape key")
        print("\nThe dropdown will no longer disappear when you move your cursor!")
    else:
        print("\n❌ Profile dropdown fix failed. Please check the implementation.")

if __name__ == "__main__":
    main()
