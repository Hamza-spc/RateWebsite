#!/usr/bin/env python3
"""
PostgreSQL Setup Script for VenueRate
This script helps you set up PostgreSQL database for the VenueRate application.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_postgresql_installed():
    """Check if PostgreSQL is installed"""
    try:
        subprocess.run(['psql', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_postgresql():
    """Install PostgreSQL using Homebrew (macOS)"""
    if sys.platform == "darwin":  # macOS
        print("🍺 Installing PostgreSQL using Homebrew...")
        return run_command("brew install postgresql@15", "Installing PostgreSQL")
    else:
        print("❌ This script is designed for macOS. Please install PostgreSQL manually for your OS.")
        return False

def start_postgresql():
    """Start PostgreSQL service"""
    if sys.platform == "darwin":  # macOS
        return run_command("brew services start postgresql@15", "Starting PostgreSQL service")
    else:
        print("⚠️  Please start PostgreSQL service manually")
        return True

def create_database_and_user():
    """Create database and user for VenueRate"""
    print("\n📝 Please provide the following information:")
    db_name = input("Database name (default: venuerate_db): ").strip() or "venuerate_db"
    db_user = input("Database user (default: venuerate_user): ").strip() or "venuerate_user"
    db_password = input("Database password: ").strip()
    
    if not db_password:
        print("❌ Password is required!")
        return False
    
    # Create user
    create_user_cmd = f"psql postgres -c \"CREATE USER {db_user} WITH PASSWORD '{db_password}';\""
    if not run_command(create_user_cmd, f"Creating user {db_user}"):
        print("⚠️  User might already exist, continuing...")
    
    # Create database
    create_db_cmd = f"psql postgres -c \"CREATE DATABASE {db_name} OWNER {db_user};\""
    if not run_command(create_db_cmd, f"Creating database {db_name}"):
        print("⚠️  Database might already exist, continuing...")
    
    # Grant privileges
    grant_cmd = f"psql postgres -c \"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};\""
    run_command(grant_cmd, f"Granting privileges to {db_user}")
    
    # Create .env file
    env_content = f"""# Database Configuration
DB_NAME={db_name}
DB_USER={db_user}
DB_PASSWORD={db_password}
DB_HOST=localhost
DB_PORT=5432

# Django Secret Key (generate a new one for production)
SECRET_KEY=django-insecure-change-this-in-production

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Google OAuth (for production)
GOOGLE_OAUTH2_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-google-client-secret

# Debug mode (set to False in production)
DEBUG=True
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created with your database configuration")
    return True

def main():
    """Main setup function"""
    print("🚀 VenueRate PostgreSQL Setup")
    print("=" * 40)
    
    # Check if PostgreSQL is installed
    if not check_postgresql_installed():
        print("❌ PostgreSQL is not installed")
        if input("Would you like to install it? (y/n): ").lower() == 'y':
            if not install_postgresql():
                print("❌ Failed to install PostgreSQL")
                return
        else:
            print("❌ Please install PostgreSQL manually and run this script again")
            return
    
    # Start PostgreSQL
    if not start_postgresql():
        print("❌ Failed to start PostgreSQL")
        return
    
    # Create database and user
    if not create_database_and_user():
        print("❌ Failed to create database and user")
        return
    
    print("\n🎉 PostgreSQL setup completed successfully!")
    print("\nNext steps:")
    print("1. Run: python manage.py migrate --settings=venue_rating_system.settings_production")
    print("2. Run: python manage.py collectstatic --settings=venue_rating_system.settings_production")
    print("3. Create a superuser: python manage.py createsuperuser --settings=venue_rating_system.settings_production")
    print("4. Run the server: python manage.py runserver --settings=venue_rating_system.settings_production")

if __name__ == "__main__":
    main()
